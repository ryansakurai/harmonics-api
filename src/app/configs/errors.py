"""
Module for application error definitions.
"""
from enum import Enum
from typing import Tuple
from flask import jsonify, Response

class Error(Enum):
    """
    Enumeration of application error codes with their details.
    """
    # Entity not found errors
    ARTIST_NOT_FOUND = {
        "code": "ArtistNotFound",
        "message": "Artist with ID '{id}' not found.",
        "status_code": 404
    }
    GENRE_NOT_FOUND = {
        "code": "GenreNotFound",
        "message": "No artists found for the genre '{genre}'.",
        "status_code": 404
    }
    RELEASE_NOT_FOUND = {
        "code": "ReleaseNotFound",
        "message": "Release with ID '{id}' not found.",
        "status_code": 404
    }
    USER_NOT_FOUND = {
        "code": "UserNotFound",
        "message": "User with username '{username}' not found.",
        "status_code": 404
    }
    RATING_NOT_FOUND = {
        "code": "RatingNotFound",
        "message": (
            "Rating of release with ID '{release_id}' "
            "by user with username '{username}' not found."
        ),
        "status_code": 404
    }
    FOLLOW_NOT_FOUND = {
        "code": "FollowNotFound",
        "message": (
            "Follow of artist with ID '{artist_id}' "
            "by user with username '{username}' not found."
        ),
        "status_code": 404
    }
    FRIENDSHIP_NOT_FOUND = {
        "code": "FriendshipNotFound",
        "message": (
            "Friendship between user with username '{username1}' "
            "and user with username '{username2}' not found."
        ),
        "status_code": 404
    }

    # Recommendations not found errors
    ARTIST_RECS_NOT_FOUND = {
        "code": "ArtistRecsNotFound",
        "message": (
            "No recommendations for the user with username '{username}'."
        ),
        "status_code": 404
    }
    NO_FRIEND_RECS_FOUND = {
        "code": "NoFriendRecsFound",
        "message": "No friend recommendations found for user '{username}' in genre '{genre}'",
        "status_code": 404,
    }

    # Entity already exists errors
    USER_ALREADY_EXISTS = {
        "code": "UserAlreadyExists",
        "message": "A user with the username '{username}' already exists.",
        "status_code": 409
    }
    RATING_ALREADY_EXISTS = {
        "code": "RatingAlreadyExists",
        "message": (
            "The user with username '{username}' already rated "
            "the release with ID '{release_id}'."
        ),
        "status_code": 409
    }
    FOLLOW_ALREADY_EXISTS = {
        "code": "FollowAlreadyExists",
        "message": (
            "The user with username '{username}' already follows "
            "the artist with ID '{artist_id}'."
        ),
        "status_code": 409
    }
    FRIENDSHIP_ALREADY_EXISTS = {
        "code": "FriendshipAlreadyExists",
        "message": (
            "The user with username '{username1}' is already friends "
            "with the user with username '{username2}'."
        ),
        "status_code": 409
    }

    # Validation errors
    PROPERTY_NOT_PROVIDED = {
        "code": "PropertyNotProvided",
        "message": "'{property}' was not provided.",
        "status_code": 422
    }
    NO_VALID_FIELDS = {
        "code": "NoValidFields",
        "message": "No valid fields to update or remove.",
        "status_code": 422
    }
    NO_QUERY_PARAMETER = {
        "vode": "NoQueryParameter",
        "message": "Missing required query parameter '{parameter}'.",
        "status_code": 400,
    }
    INVALID_REC_METHOD = {
        "code": "InvalidRecMethod",
        "message": "Invalid recommendation method '{method}'.",
        "status_code": 400,
    }

    NO_GENRE_DATA_FOUND = {
        "code": "NoGenreDataFound",
        "message": (
            "No genre data was found for the user with username '{username}'."
        ),
        "status_code": 404
    }

    NO_RATINGS_FOUND = {
        "code": "NoRatingsFound",
        "message": (
            "No ratings greater than 6 were found for the user with username '{username}'."
        ),
        "status_code": 404
    }     

    NO_FRIENDS_RATINGS_FOUND = {
        "code": "NoFriendsRatingsFound",
        "message": "No ratings > 6 found for any friends.",
        "status_code": 404
    }

    @property
    def code(self) -> str:
        """Get the error code."""
        return self.value["code"]

    @property
    def message_template(self) -> str:
        """Get the message template."""
        return self.value["message"]

    @property
    def status_code(self) -> int:
        """Get the HTTP status code."""
        return self.value["status_code"]

    def get_response(self, **kwargs) -> Tuple[Response, int]:
        """Format the error message with provided parameters."""
        return (
            jsonify({
                "code": self.code,
                "message": self.message_template.format(**kwargs),
            }),
            self.status_code,
        )
