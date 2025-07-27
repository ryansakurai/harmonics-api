"""
Module for the 'recs/' route.
"""
import random
from flask import Blueprint, jsonify, request
from configs import mongodb, neo4j
from configs.errors import Error
from utils import helper

bp = Blueprint("recs", __name__)

@bp.route("/<username>/artists", methods = ["GET"])
def get_artist_recs_by_genre(username):
    """
    Endpoint for getting artist recommendations by genre.
    """
    if not helper.exists("user", username):
        return Error.USER_NOT_FOUND.get_response(username = username)

    genre_result = neo4j.driver.execute_query(
        """
        MATCH (:User {username: $username})-[:FOLLOWS]->(a:Artist)-[:BELONGS_TO]->(g:Genre)
        WITH g.name AS genre, count(DISTINCT a) AS follows_count
        ORDER BY follows_count DESC
        LIMIT 1
        RETURN genre
        """,
        username=username,
    )

    if not genre_result.records:
        return Error.NO_GENRE_DATA_FOUND.get_response(username=username)

    most_common_genre = genre_result.records[0]["genre"]

    records, _, _ = neo4j.driver.execute_query(
        """
        MATCH (a:Artist)-[:BELONGS_TO]->(g:Genre {name: $genre})
        WHERE NOT EXISTS {
            MATCH (u:User {username: $username})-[:FOLLOWS]->(a)
        }
        ORDER BY a.popularity DESC
        LIMIT 10
        RETURN a.id AS id
        """,
        genre=most_common_genre,
        username=username,
    )
    if not records:
        return Error.ARTIST_RECS_NOT_FOUND.get_response(
            username=username,
            genre=most_common_genre,
        )

    selected_artist_id = random.choice(records)["id"]

    artist = mongodb.db.artists.find_one(
        {
            "_id": selected_artist_id,
        },
        {
            "_id": False,
            "id": "$_id",
            "name": True,
            "bio": True,
        }
    )

    response = {
        "artist": {
            "id": artist["id"],
            "name": artist["name"],
            "bio": artist["bio"],
        },
        "by": {
            "genre": most_common_genre,
        }
    }

    return jsonify(response), 200

@bp.route("/<username>/releases/friends", methods = ["GET"])
def get_release_recs_by_friends(username):
    """
    Endpoint for getting release recommendations by friends' positive reviews.
    """
    if not helper.exists("user", username):
        return Error.USER_NOT_FOUND.get_response(username=username)

    friends_rating = neo4j.driver.execute_query(
        """
        MATCH (u:User {username: $username})-[:FRIENDS_WITH]-(friend:User)-[r:RATED]->(rel:Release)
        WHERE r.rating >= 6
        RETURN friend.username AS friend_username, rel.id AS release_id, r.rating AS rating
        ORDER BY r.rating DESC
        LIMIT 10
        """,
        username = username
    )

    results = []
    for record in friends_rating.records:
        results.append({
            "friend_username": record["friend_username"],
            "release_id": record["release_id"],
            "rating": record["rating"]
        })
    if not results:
        return Error.NO_FRIENDS_RATINGS_FOUND.get_response()

    result = random.choice(results)

    release_cursor = mongodb.db.artists.aggregate([
        {
            "$match": {
                "releases.id": result["release_id"],
            },
        },
        {
            "$unwind": "$releases",
        },
        {
            "$match": {
                "releases.id": result["release_id"],
            },
        },
        {
            "$project": {
                "_id": False,
                "id": "$releases.id",
                "name": "$releases.name",
                "artist": "$name",
            },
        },
    ])

    release_results = tuple(release_cursor)

    response = {
        "release": {
            "id": release_results[0]["id"],
            "name": release_results[0]["name"],
            "artist": release_results[0]["artist"]
        },
        "by": {
            "username": result["friend_username"],
            "rating": result["rating"]
        }
    }

    return jsonify(response), 200

@bp.route("/<username>/friends", methods = ["GET"])
def get_friend_recs(username):
    """
    Endpoint for getting friend recommendations.
    """
    by = request.args.get("by", type = str)
    if not by:
        return Error.NO_QUERY_PARAMETER.get_response(
            parameter="by",
        )

    valid_methods = ["genre", "reviews"]
    if by not in valid_methods:
        return Error.INVALID_REC_METHOD.get_response(
            method=by,
        )

    if not helper.exists("user", username):
        return Error.USER_NOT_FOUND.get_response(username=username)

    if by == "genre":
        return get_friend_recs_by_genre(username)
    return get_friend_recs_by_reviews(username)

def get_friend_recs_by_genre(username):
    """
    Endpoint for getting friend recommendations by genre affinity.
    """
    genre_result = neo4j.driver.execute_query(
        """
        MATCH (:User {username: $username})-[:FOLLOWS]->(a:Artist)-[:BELONGS_TO]->(g:Genre)
        WITH g.name AS genre, count(DISTINCT a) AS follows_count
        ORDER BY follows_count DESC
        LIMIT 1
        RETURN genre
        """,
        username=username,
    )

    if not genre_result.records:
        return Error.NO_GENRE_DATA_FOUND.get_response(username = username)

    most_common_genre = genre_result.records[0]["genre"]

    recs_result = neo4j.driver.execute_query(
        """
        MATCH (u:User)-[:FOLLOWS]->(a:Artist)-[:BELONGS_TO]->(g:Genre {name: $genre})
        WHERE NOT EXISTS {
            MATCH (:User {username: $username})-[:FRIENDS_WITH]-(u)
        }
        WITH u, count(a) AS follows_count
        ORDER BY follows_count DESC
        LIMIT 10
        RETURN u.username AS recommended_user
        """,
        genre=most_common_genre,
        username=username,
    )

    if not recs_result.records:
        return Error.NO_FRIEND_RECS_FOUND.get_response(username=username, genre=most_common_genre)

    selected_username = random.choice(recs_result.records)["recommended_user"]

    user_details = mongodb.db.users.find_one(
        {
            "username": selected_username,
        },
        {
            "_id": False,
            "username": True,
            "name": {
                "$ifNull": ["$name", None],
            },
            "bio": {
                "$ifNull": ["$bio", None],
            },
        }
    )

    response = {
        "user": {
            "username": user_details["username"],
            "name": user_details["name"],
            "bio": user_details["bio"]
        },
        "by": {
            "genre": most_common_genre
        }
    }

    return jsonify(response), 200

def get_friend_recs_by_reviews(username):
    """
    Endpoint for getting friend recommendations by review similarity.
    """
    # Get user's highest rated releases
    reviews = neo4j.driver.execute_query(
        """
        MATCH (u:User {username: $username})-[r:RATED]->(rel:Release)
        WHERE r.rating >= 6
        RETURN rel.id AS release_id, r.rating AS rating
        ORDER BY r.rating DESC
        """,
        username = username
    )

    rated_releases = []
    for record in reviews.records:
        rated_releases.append(record["release_id"])

    if not rated_releases:
        return Error.NO_RATINGS_FOUND.get_response(username = username)

    selected_release = random.choice(rated_releases)

    rated_reviews = neo4j.driver.execute_query(
        """
        MATCH (u:User)-[r:RATED]->(rel:Release)
        WHERE rel.id = $release_id
        AND r.rating >= 6
        AND NOT EXISTS {
            MATCH (:User {username: $username})-[:FRIENDS_WITH]-(u)
        }
        AND u.username <> $username
        RETURN u.username AS username, r.rating AS rating
        ORDER BY r.rating DESC
        LIMIT 10
        """,
        release_id=selected_release,
        username=username
    )

    if not rated_reviews.records:
        return Error.NO_FRIEND_RECS_FOUND.get_response(
            username = username,
            release_id = selected_release,
        )

    recommended_user = random.choice(rated_reviews.records)
    selected_username = recommended_user["username"]
    friend_rating = recommended_user["rating"]

    user_details = mongodb.db.users.find_one(
        {
            "username": selected_username,
        },
        {
            "_id": False,
            "username": True,
            "name": {
                "$ifNull": ["$name", None],
            },
            "bio": {
                "$ifNull": ["$bio", None],
            },
        },
    )

    if not user_details:
        return Error.USER_NOT_FOUND.get_response(username=selected_username)

    release_cursor = mongodb.db.artists.aggregate([
        {
            "$match": {
                "releases.id": selected_release,
            },
        },
        {
            "$unwind": "$releases",
        },
        {
            "$match": {
                "releases.id": selected_release,
            },
        },
        {
            "$project": {
                "_id": False,
                "id": "$releases.id",
                "name": "$releases.name",
                "artist": "$name",
            },
        },
    ])

    release_results = tuple(release_cursor)

    response = {
        "user": {
            "username": user_details["username"],
            "name": user_details["name"],
            "bio": user_details["bio"]
        },
        "by": {
            "id": release_results[0]["id"],
            "name": release_results[0]["name"],
            "artist": release_results[0]["artist"],
            "rating": friend_rating
        }
    }

    return jsonify(response), 200
