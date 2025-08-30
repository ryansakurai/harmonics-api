"""
Module for the 'users/' route.
"""
import hashlib
from flask import Blueprint, jsonify, request
from harmonics_api.configs import mongodb, neo4j
from harmonics_api.configs.errors import Error
from harmonics_api.utils import helper

bp = Blueprint("users", __name__)

@bp.route("/<username>", methods = ["GET"])
def get_user(username):
    """
    Endpoint for getting the user resource by username.
    """
    user_cursor = mongodb.db.users.aggregate([
        {
            "$match": {
                "username": username,
            },
        },
        {
            "$project": {
                "_id": False,
                "username": True,
                "name": {
                    "$ifNull": ["$name", None],
                },
                "bio": {
                    "$ifNull": ["$bio", None],
                },
                "qt_friends": {
                    "$size": "$friends",
                },
                "qt_ratings": {
                    "$size": "$ratings",
                },
                "qt_follows": {
                    "$size": "$follows",
                },
            },
        },
    ])

    user_results = tuple(user_cursor)
    if not user_results:
        body, code = Error.USER_NOT_FOUND.response(username = username)
        return jsonify(body), code

    return jsonify(user_results[0]), 200

@bp.route("/<username>/friends", methods = ["GET"])
def get_user_friends(username):
    """
    Endpoint for getting all friends of a user.
    """
    user_cursor = mongodb.db.users.aggregate([
        {
            "$match": {
                "username": username,
            }
        },
        {
            "$project": {
                "_id": False,
                "username": True,
                "items": "$friends",
            },
        },
    ])

    user_results = tuple(user_cursor)
    if not user_results:
        body, code = Error.USER_NOT_FOUND.response(username = username)
        return jsonify(body), code

    return jsonify(user_results[0]), 200

@bp.route("/<username>/ratings", methods = ["GET"])
def get_user_ratings(username):
    """
    Endpoint for getting all ratings of a user.
    """
    user_cursor = mongodb.db.users.aggregate([
        {
            "$match": {
                "username": username,
            }
        },
        {
            "$project": {
                "_id": False,
                "username": True,
                "items": "$ratings",
            },
        },
    ])

    user_results = tuple(user_cursor)
    if not user_results:
        body, code = Error.USER_NOT_FOUND.response(username = username)
        return jsonify(body), code

    return jsonify(user_results[0]), 200

@bp.route("/<username>/follows", methods = ["GET"])
def get_user_follows(username):
    """
    Endpoint for getting all artists followed by a user.
    """
    user_cursor = mongodb.db.users.aggregate([
        {
            "$match": {
                "username": username,
            }
        },
        {
            "$project": {
                "_id": False,
                "username": True,
                "items": "$follows",
            },
        },
    ])

    user_results = tuple(user_cursor)
    if not user_results:
        body, code = Error.USER_NOT_FOUND.response(username = username)
        return jsonify(body), code

    return jsonify(user_results[0]), 200

@bp.route("/", methods = ["POST"])
def register_user():
    """
    Endpoint for registering a new user.
    """
    body = request.get_json()
    if not body or "username" not in body:
        body, code = Error.PROPERTY_NOT_PROVIDED.response(property = "username")
        return jsonify(body), code
    if "password" not in body:
        body, code = Error.PROPERTY_NOT_PROVIDED.response(property = "password")
        return jsonify(body), code

    username = body["username"]
    password = body["password"]
    name = body.get("name")
    bio = body.get("bio")

    if helper.exists("user", username):
        body, code = Error.USER_ALREADY_EXISTS.response(username = username)
        return jsonify(body), code

    user = {}
    user["username"] = username
    user["password"] = hashlib.sha256(password.encode("utf-8")).hexdigest()
    if name:
        user["name"] = name
    if bio:
        user["bio"] = bio
    user["friends"] = []
    user["ratings"] = []
    user["follows"] = []

    mongodb.db.users.insert_one(user)

    neo4j.driver.execute_query(
        """
        MERGE (u:User {username: $username})
        """,
        username = username
    )

    return jsonify(), 201

@bp.route("/<username>", methods = ["DELETE"])
def delete_user(username):
    """
    Endpoint for deleting a user account.
    """
    user = mongodb.db.users.find_one(
        {
            "username": username,
        },
        {
            "friends": True,
            "ratings": True,
            "follows": True,
        },
    )
    if not user:
        body, code = Error.USER_NOT_FOUND.response(username = username)
        return jsonify(body), code

    for friend in user["friends"]:
        mongodb.db.users.update_one(
            {
                "username": friend,
            },
            {
                "$pull": {
                    "friends": username,
                },
            },
        )

    for rating in user["ratings"]:
        mongodb.db.artists.update_one(
            {
                "releases.id": rating["id"],
            },
            {
                "$pull": {
                    "releases.$.ratings": {
                        "username": username,
                    },
                },
            },
        )

    for follow in user["follows"]:
        mongodb.db.artists.update_one(
            {
                "_id": follow["id"],
            },
            {
                "$inc": {
                    "qt_followers": -1,
                },
            },
        )

    mongodb.db.users.delete_one(
        {
            "username": username,
        },
    )

    neo4j.driver.execute_query(
        """
        MATCH (u:User {username: $username})
        DETACH DELETE u
        """,
        username = username,
    )

    return jsonify(), 200

@bp.route("/<username>", methods = ["PATCH"])
def update_user(username):
    """
    Endpoint for updating user data (password, name, bio).
    """
    body = request.get_json()

    if not helper.exists("user", username):
        body, code = Error.USER_NOT_FOUND.response(username = username)
        return jsonify(body), code

    update_ops = {}
    unset_ops = {}

    if "password" in body:
        password = body["password"]
        update_ops["password"] = hashlib.sha256(password.encode("utf-8")).hexdigest()

    if "name" in body:
        name = body["name"]
        if name:
            update_ops["name"] = name
        else:
            unset_ops["name"] = True

    if "bio" in body:
        bio = body["bio"]
        if bio:
            update_ops["bio"] = bio
        else:
            unset_ops["bio"] = True

    if not update_ops and not unset_ops:
        body, code = Error.NO_VALID_FIELDS.response()
        return jsonify(body), code

    update_doc = {}
    if update_ops:
        update_doc["$set"] = update_ops
    if unset_ops:
        update_doc["$unset"] = unset_ops

    mongodb.db.users.update_one(
        {
            "username": username,
        },
        update_doc,
    )

    return jsonify(), 200

@bp.route("/<username>/ratings", methods = ["POST"])
def rate_release(username):
    """
    Endpoint for adding a rating to a user and release.
    """
    body = request.get_json()
    if not body or "id" not in body:
        body, code = Error.PROPERTY_NOT_PROVIDED.response(property = "id")
        return jsonify(body), code
    if "rating" not in body:
        body, code = Error.PROPERTY_NOT_PROVIDED.response(property = "rating")
        return jsonify(body), code

    release_id = body["id"]
    rating = body["rating"]

    if not helper.exists("user", username):
        body, code = Error.USER_NOT_FOUND.response(username = username)
        return jsonify(body), code

    release_cursor = mongodb.db.artists.aggregate([
        {
            "$match": {
                "releases.id": release_id,
            },
        },
        {
            "$unwind": "$releases",
        },
        {
            "$match": {
                "releases.id": release_id,
            },
        },
        {
            "$project": {
                "_id": False,
                "id": "$releases.id",
                "artist": "$name",
                "name": "$releases.name",
            }
        }
    ])

    release_results = tuple(release_cursor)
    if not release_results:
        body, code = Error.RELEASE_NOT_FOUND.response(id = release_id)
        return jsonify(body), code

    release: dict = release_results[0]

    if helper.exists("rating", username, release_id):
        body, code = Error.RATING_ALREADY_EXISTS.response(
            username = username,
            release_id = release_id,
        )
        return jsonify(body), code

    mongodb.db.users.update_one(
        {
            "username": username,
        },
        {
            "$push": {
                "ratings": {
                    "id": release["id"],
                    "artist": release["artist"],
                    "name": release["name"],
                    "rating": rating,
                },
            },
        },
    )

    mongodb.db.artists.update_one(
        {
            "releases.id": release_id,
        },
        {
            "$push": {
                "releases.$.ratings": {
                    "username": username,
                    "rating": rating
                }
            }
        }
    )

    neo4j.driver.execute_query(
        """
        MATCH (r:Release {id: $release_id})
        MATCH (u:User {username: $username})
        MERGE (u)-[rel:RATED]->(r)
        ON CREATE SET rel.rating = $rating
        """,
        release_id = release["id"],
        username = username,
        rating = rating,
    )

    return jsonify(), 201

@bp.route("/<username>/ratings/<release_id>", methods = ["DELETE"])
def unrate_release(username, release_id):
    """
    Endpoint for removing a rating from a user and release.
    """
    if not helper.exists("user", username):
        body, code = Error.USER_NOT_FOUND.response(username = username)
        return jsonify(body), code
    if not helper.exists("release", release_id):
        body, code = Error.RELEASE_NOT_FOUND.response(id = release_id)
        return jsonify(body), code
    if not helper.exists("rating", username, release_id):
        body, code = Error.RATING_NOT_FOUND.response(
            release_id = release_id,
            username = username,
        )
        return jsonify(body), code

    mongodb.db.users.update_one(
        {
            "username": username,
        },
        {
            "$pull": {
                "ratings": {
                    "id": release_id,
                },
            },
        },
    )

    mongodb.db.artists.update_one(
        {
            "releases.id": release_id,
        },
        {
            "$pull": {
                "releases.$.ratings": {
                    "username": username,
                },
            },
        },
    )

    neo4j.driver.execute_query(
        """
        MATCH (u:User {username: $username})-[r:RATED]->(rel:Release {id: $release_id})
        DELETE r
        """,
        username = username,
        release_id = release_id,
    )

    return jsonify(), 200

@bp.route("/<username>/follows", methods = ["POST"])
def follow_artist(username):
    """
    Endpoint for following an artist.
    """
    body = request.get_json()
    if not body or "id" not in body:
        body, code = Error.PROPERTY_NOT_PROVIDED.response(property = "id")
        return jsonify(body), code
    artist_id = body["id"]

    if not helper.exists("user", username):
        body, code = Error.USER_NOT_FOUND.response(username = username)
        return jsonify(body), code

    artist = mongodb.db.artists.find_one(
        {
            "_id": artist_id,
        },
        {
            "_id": True,
            "name": True,
        },
    )
    if not artist:
        body, code = Error.ARTIST_NOT_FOUND.response(id = artist_id)
        return jsonify(body), code

    if helper.exists("follow", username, artist_id):
        body, code = Error.FOLLOW_ALREADY_EXISTS.response(
            username = username,
            artist_id = artist_id,
        )
        return jsonify(body), code

    mongodb.db.users.update_one(
        {
            "username": username,
        },
        {
            "$push": {
                "follows": {
                    "id": artist_id,
                    "name": artist["name"],
                },
            },
        },
    )

    mongodb.db.artists.update_one(
        {
            "_id": artist_id,
        },
        {
            "$inc": {
                "qt_followers": 1,
            },
        },
    )

    neo4j.driver.execute_query(
        """
        MATCH (u:User {username: $username})
        MATCH (a:Artist {id: $artist_id})
        MERGE (u)-[:FOLLOWS]->(a)
        """,
        artist_id = artist_id,
        username = username,
    )

    return jsonify(), 201

@bp.route("/<username>/follows/<artist_id>", methods = ["DELETE"])
def unfollow_artist(username, artist_id):
    """
    Endpoint for unfollowing an artist.
    """
    if not helper.exists("user", username):
        body, code = Error.USER_NOT_FOUND.response(username = username)
        return jsonify(body), code
    if not helper.exists("artist", artist_id):
        body, code = Error.ARTIST_NOT_FOUND.response(id = artist_id)
        return jsonify(body), code
    if not helper.exists("follow", username, artist_id):
        body, code = Error.FOLLOW_NOT_FOUND.response(
            artist_id = artist_id,
            username = username,
        )
        return jsonify(body), code

    mongodb.db.users.update_one(
        {
            "username": username,
        },
        {
            "$pull": {
                "follows": {
                    "id": artist_id,
                },
            },
        },
    )

    mongodb.db.artists.update_one(
        {
            "_id": artist_id,
        },
        {
            "$inc": {
                "qt_followers": -1,
            },
        },
    )

    neo4j.driver.execute_query(
        """
        MATCH (u:User {username: $username})-[f:FOLLOWS]->(a:Artist {id: $artist_id})
        DELETE f
        """,
        username = username,
        artist_id = artist_id,
    )

    return jsonify(), 200

@bp.route("/<username>/friends", methods = ["POST"])
def befriend_user(username):
    """
    Endpoint for adding a friend.
    """
    body = request.get_json()
    if not body or "username" not in body:
        body, code = Error.PROPERTY_NOT_PROVIDED.response(property = "username")
        return jsonify(body), code

    friend_username = body["username"]
    if not helper.exists("user", username):
        body, code = Error.USER_NOT_FOUND.response(username = username)
        return jsonify(body), code
    if not helper.exists("user", friend_username):
        body, code = Error.USER_NOT_FOUND.response(username = friend_username)
        return jsonify(body), code
    if helper.exists("friendship", username, friend_username):
        body, code = Error.FRIENDSHIP_ALREADY_EXISTS.response(
            username1 = username,
            username2 = friend_username,
        )
        return jsonify(body), code

    mongodb.db.users.update_one(
        {
            "username": username,
        },
        {
            "$push": {
                "friends": friend_username,
            },
        },
    )

    mongodb.db.users.update_one(
        {
            "username": friend_username,
        },
        {
            "$push": {
                "friends": username,
            },
        },
    )

    neo4j.driver.execute_query(
        """
        MATCH (u1:User {username: $username})
        MATCH (u2:User {username: $friend_username})
        MERGE (u1)-[:FRIENDS_WITH]->(u2)
        MERGE (u1)<-[:FRIENDS_WITH]-(u2)
        """,
        username = username,
        friend_username = friend_username,
    )

    return jsonify(), 201

@bp.route("/<username>/friends/<friend_username>", methods = ["DELETE"])
def unfriend_user(username, friend_username):
    """
    Endpoint for removing a friend.
    """
    if not helper.exists("user", username):
        body, code = Error.USER_NOT_FOUND.response(username = username)
        return jsonify(body), code
    if not helper.exists("user", friend_username):
        body, code = Error.USER_NOT_FOUND.response(username = friend_username)
        return jsonify(body), code
    if not helper.exists("friendship", username, friend_username):
        body, code = Error.FRIENDSHIP_NOT_FOUND.response(
            username1 = username,
            username2 = friend_username,
        )
        return jsonify(body), code

    mongodb.db.users.update_one(
        {
            "username": username,
        },
        {
            "$pull": {
                "friends": friend_username,
            },
        },
    )

    mongodb.db.users.update_one(
        {
            "username": friend_username,
        },
        {
            "$pull": {
                "friends": username,
            },
        },
    )

    neo4j.driver.execute_query(
        """
        MATCH (u1:User {username: $username1})-[f1:FRIENDS_WITH]->(u2:User {username: $username2})
        MATCH (u1)<-[f2:FRIENDS_WITH]-(u2)
        DELETE f1, f2
        """,
        username1 = username,
        username2 = friend_username,
    )

    return jsonify(), 200
