"""
Module for application error definitions.
"""
from enum import Enum
from typing import Dict, Tuple

class Error(Enum):
    """
    Enumeration of application error codes with their details.
    """
    # Entity not found errors
    ARTIST_NOT_FOUND = (
        {
            "code": "ArtistNotFound",
            "message": "Artist with ID '{id}' not found.",
        },
        404,
    )
    GENRE_NOT_FOUND = (
        {
            "code": "GenreNotFound",
            "message": "No artists found for the genre '{genre}'.",
        },
        404,
    )
    RELEASE_NOT_FOUND = (
        {
            "code": "ReleaseNotFound",
            "message": "Release with ID '{id}' not found.",
        },
        404,
    )
    USER_NOT_FOUND = (
        {
            "code": "UserNotFound",
            "message": "User with username '{username}' not found.",
        },
        404,
    )
    RATING_NOT_FOUND = (
        {
            "code": "RatingNotFound",
            "message": (
                "Rating of release with ID '{release_id}' "
                "by user with username '{username}' not found."
            ),
        },
        404,
    )
    FOLLOW_NOT_FOUND = (
        {
            "code": "FollowNotFound",
            "message": (
                "Follow of artist with ID '{artist_id}' "
                "by user with username '{username}' not found."
            ),
        },
        404,
    )
    FRIENDSHIP_NOT_FOUND = (
        {
            "code": "FriendshipNotFound",
            "message": (
                "Friendship between user with username '{username1}' "
                "and user with username '{username2}' not found."
            ),
        },
        404,
    )

    # Recommendations not found errors
    ARTIST_RECS_NOT_FOUND = (
        {
            "code": "ArtistRecsNotFound",
            "message": (
                "No recommendations for the user with username '{username}'."
            ),
        },
        404,
    )
    NO_FRIEND_RECS_FOUND = (
        {
            "code": "NoFriendRecsFound",
            "message": "No friend recommendations found for user '{username}' in genre '{genre}'",
        },
        404,
    )

    # Entity already exists errors
    USER_ALREADY_EXISTS = (
        {
            "code": "UserAlreadyExists",
            "message": "A user with the username '{username}' already exists.",
        },
        409,
    )
    RATING_ALREADY_EXISTS = (
        {
            "code": "RatingAlreadyExists",
            "message": (
                "The user with username '{username}' already rated "
                "the release with ID '{release_id}'."
            ),
        },
        409,
    )
    FOLLOW_ALREADY_EXISTS = (
        {
            "code": "FollowAlreadyExists",
            "message": (
                "The user with username '{username}' already follows "
                "the artist with ID '{artist_id}'."
            ),
        },
        409,
    )
    FRIENDSHIP_ALREADY_EXISTS = (
        {
            "code": "FriendshipAlreadyExists",
            "message": (
                "The user with username '{username1}' is already friends "
                "with the user with username '{username2}'."
            ),
        },
        409,
    )

    # Validation errors
    PROPERTY_NOT_PROVIDED = (
        {
            "code": "PropertyNotProvided",
            "message": "'{property}' was not provided.",
        },
        422,
    )
    NO_VALID_FIELDS = (
        {
            "code": "NoValidFields",
            "message": "No valid fields to update or remove.",
        },
        422,
    )
    NO_QUERY_PARAMETER = (
        {
            "code": "NoQueryParameter",
            "message": "Missing required query parameter '{parameter}'.",
        },
        400,
    )
    INVALID_REC_METHOD = (
        {
            "code": "InvalidRecMethod",
            "message": "Invalid recommendation method '{method}'.",
        },
        400,
    )

    NO_GENRE_DATA_FOUND = (
        {
            "code": "NoGenreDataFound",
            "message": (
                "No genre data was found for the user with username '{username}'."
            ),
        },
        404,
    )

    NO_RATINGS_FOUND = (
        {
            "code": "NoRatingsFound",
            "message": (
                "No ratings greater than 6 were found for the user with username '{username}'."
            ),
        },
        404,
    )

    NO_FRIENDS_RATINGS_FOUND = (
        {
            "code": "NoFriendsRatingsFound",
            "message": "No ratings > 6 found for any friends.",
        },
        404,
    )

    def response(self, **kwargs) -> Tuple[Dict[str, str], int]:
        """Format the error message with provided parameters."""
        body, status_code = self.value
        return (
            {
                "code": body["code"],
                "message": body["message"].format(**kwargs),
            },
            status_code,
        )
