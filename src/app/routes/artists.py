"""
Module for the 'artists/' route.
"""
from flask import Blueprint, jsonify
from configs import mongodb
from configs.errors import Error

bp = Blueprint("artists", __name__)

@bp.route("/<artist_id>", methods = ["GET"])
def get_artist(artist_id):
    """
    Endpoint for getting the artist resource by artist ID.
    """
    artist_cursor = mongodb.db.artists.aggregate([
        {
            "$match": {
                "_id": artist_id
            }
        },
        {
            "$addFields": {
                "allRatings": {
                    "$reduce": {
                        "input": "$releases",
                        "initialValue": [],
                        "in": {
                            "$concatArrays": [
                                "$$value",
                                "$$this.ratings"
                            ]
                        }
                    }
                },
                "mappedReleases": {
                    "$map": {
                        "input": "$releases",
                        "as": "release",
                        "in": {
                            "id": "$$release.id",
                            "name": "$$release.name",
                            "release_year": {
                                "$year": {
                                    "$dateFromString": {
                                        "dateString": "$$release.release_date"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        {
            "$project": {
                "_id": False,
                "id": "$_id",
                "name": True,
                "genres": True,
                "bio": True,
                "qt_followers": True,
                "average_rating": {
                    "$cond": {
                        "if": {
                            "$gt": [{"$size": "$allRatings"}, 0],
                        },
                        "then": {
                            "$avg": "$allRatings.rating"
                        },
                        "else": None
                    }
                },
                "releases": "$mappedReleases"
            }
        }
    ])

    artists_retrieved = tuple(artist_cursor)
    if not artists_retrieved:
        return Error.ARTIST_NOT_FOUND.get_response(id = artist_id)

    return jsonify(artists_retrieved[0]), 200

@bp.route("/<artist_id>/tracks", methods = ["GET"])
def get_artist_tracks(artist_id):
    """
    Endpoint for getting all tracks from an artist in alphabetical order.
    """
    tracks_cursor = mongodb.db.artists.aggregate([
        {
            "$match": {
                "_id": artist_id,
            },
        },
        {
            "$unwind": "$releases",
        },
        {
            "$unwind": "$releases.tracks",
        },
        {
            "$group": {
                "_id": {
                    "artist_id": "$_id",
                    "artist_name": "$name",
                    "track_name": "$releases.tracks.name"
                },
                "releases": {
                    "$push": {
                        "id": "$releases.id",
                        "name": "$releases.name",
                    },
                },
            },
        },
        {
            "$group": {
                "_id": {
                    "id": "$_id.artist_id",
                    "name": "$_id.artist_name"
                },
                "items": {
                    "$push": {
                        "name": "$_id.track_name",
                        "releases": "$releases",
                    },
                },
            },
        },
        {
            "$project": {
                "_id": False,
                "artist": "$_id",
                "items": {
                    "$sortArray": {
                        "input": "$items",
                        "sortBy": {
                            "name": 1,
                        },
                    },
                },
            },
        },
    ])

    tracks_results = tuple(tracks_cursor)
    if not tracks_results:
        return Error.ARTIST_NOT_FOUND.get_response(id = artist_id)

    return jsonify(tracks_results[0]), 200
