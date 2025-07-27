"""
Module for the helper functions of the app.
"""
from configs import mongodb, neo4j

def exists(entity: str, *identifiers: str) -> bool:
    """
    Check if an entity exists in the database.
    """
    match entity:
        case "user":
            return mongodb.db.users.find_one(
                {
                    "username": identifiers[0],
                },
                {
                    "_id": True,
                },
            ) is not None
        case "artist":
            return mongodb.db.artists.find_one(
                {
                    "_id": identifiers[0],
                },
                {
                    "_id": True,
                },
            ) is not None
        case "release":
            return mongodb.db.artists.find_one(
                {
                    "releases.id": identifiers[0],
                },
                {
                    "_id": True,
                },
            ) is not None
        case "rating":
            return neo4j.driver.execute_query(
                """
                RETURN EXISTS(
                    (:User {username: $username})-[:RATED]->(:Release {id: $release_id})
                ) AS exists
                """,
                username = identifiers[0],
                release_id = identifiers[1],
            )[0][0]["exists"]
        case "follow":
            return neo4j.driver.execute_query(
                """
                RETURN EXISTS(
                    (:User {username: $username})-[:FOLLOWS]->(:Artist {id: $artist_id})
                ) AS exists
                """,
                username = identifiers[0],
                artist_id = identifiers[1],
            )[0][0]["exists"]
        case "friendship":
            return neo4j.driver.execute_query(
                """
                RETURN EXISTS(
                    (:User {username: $username1})-[:FRIENDS_WITH]-(:User {username: $username2})
                ) AS exists
                """,
                username1 = identifiers[0],
                username2 = identifiers[1],
            )[0][0]["exists"]
        case "genre":
            return neo4j.driver.execute_query(
                """
                MATCH (g:Genre {name: $genre})
                RETURN COUNT(g) > 0 AS exists
                """,
                genre = identifiers[0],
            )[0][0]["exists"]
        case _:
            raise ValueError(f"Unknown entity type: {entity}")
