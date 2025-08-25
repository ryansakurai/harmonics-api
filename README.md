# 🎧 Harmonics API 🎧

API for a music catalog with social media and recommendation features.

### Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
    - [Artists](#artists)
    - [Releases](#releases)
    - [Users](#users)
    - [Recommendations](#recommendations)
- [Databases](#databases)
    - [MongoDB Schemas](#mongodb-schemas)
    - [Neo4j Schemas](#neo4j-schemas)
    - [Data Population](#data-population)
- [Authors](#authors)

## Features

- **Music Catalog**: Browse artist and release information
- **User Management**: Register users, manage profiles and view social overview
- **Social Features**: Connect with friends, follow artists and rate releases
- **Recommendation Engine**: Get artist, release and friend suggestions based on user data

## Tech Stack

- **Language**: Python
- **Backend**: Flask
- **Databases**: 
    - MongoDB
    - Neo4j

## Project Structure

```
harmonics-api/
├── src/harmonics_api/         # API source code
│   ├── main.py                # Flask application entry point
│   ├── configs/               # Database connections and errors
│   ├── routes/                # API endpoints
│   │   ├── artists.py         # Artist-related endpoints
│   │   ├── releases.py        # Release-related endpoints
│   │   ├── users.py           # User-related endpoints
│   │   └── recs.py            # Recommendation endpoints
│   └── utils/                 # Utility functions
├── data/                      # Database dumps
└── scripts/                   # Data population scripts
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ryansakurai/harmonics-api.git
   cd harmonics-api
   ```

2. **Install the package**:
   ```bash
   pip install -e .
   ```

3. **Install population dependencies** (optional, for data generation):

   ```bash
   pip install -e .[population]
   ```

4. **Set up environment variables**:

   Create a `.env` file in the root directory:

   ```env
   MONGODB_URI=your_mongodb_connection_string
   NEO4J_USERNAME=your_neo4j_username
   NEO4J_PASSWORD=your_neo4j_password

   # Population-specific
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. **Running the API**:

```bash
harmonics-api
```

## API Endpoints

### Artists

- `GET /v1/artists/<artist_id>` - Get artist details
- `GET /v1/artists/<artist_id>/tracks` - Get artist tracks

### Releases

- `GET /v1/releases/<release_id>` - Get release details
- `GET /v1/releases/<release_id>/ratings` - Get all ratings for a release

### Users

- `GET /v1/users/<username>` - Get user profile
- `POST /v1/users/` - Register a new user
- `PATCH /v1/users/<username>` - Update user data
- `DELETE /v1/users/<username>` - Delete user account
- `GET /v1/users/<username>/friends` - Get user's friends
- `POST /v1/users/<username>/friends` - Add a friend
- `DELETE /v1/users/<username>/friends/<friend_username>` - Remove a friend
- `GET /v1/users/<username>/ratings` - Get user's ratings
- `POST /v1/users/<username>/ratings` - Rate a release
- `DELETE /v1/users/<username>/ratings/<release_id>` - Remove a rating
- `GET /v1/users/<username>/follows` - Get artists followed by user
- `POST /v1/users/<username>/follows` - Follow an artist
- `DELETE /v1/users/<username>/follows/<artist_id>` - Unfollow an artist

### Recommendations

- `GET /v1/recs/<username>/artists` - Get artist recommendations by genre
- `GET /v1/recs/<username>/releases` - Get release recommendations by friends' reviews
- `GET /v1/recs/<username>/friends?by=<method>` - Get friend recommendations (method: "genre" or "reviews")

## Databases

### MongoDB Schemas

**Artists**:

```json
{
  "_id": "string",
  "name": "string",
  "genres": ["string"],
  "bio": "string",
  "qt_followers": "int32",
  "releases": [
    {
      "id": "string",
      "name": "string",
      "release_date": "string",
      "tracks": [
        {
          "track_number": "number",
          "name": "string",
          "duration": "int32"
        }
      ],
      "ratings": [
        {
          "username": "string",
          "rating": "int32"
        }
      ]
    }
  ]
}
```

**Users**:

```json
{
  "_id": "objectid",
  "username": "string",
  "password": "string",
  "name": "string?",
  "bio": "string?",
  "friends": ["string"],
  "ratings": [
    {
      "id": "string",
      "artist": "string",
      "name": "string",
      "rating": "int32"
    }
  ],
  "follows": [
    {
      "id": "string",
      "name": "string"
    }
  ]
}
```

### Neo4j Schemas

- **Nodes**:
    - `User { "username": "String" }`
    - `Artist { "id": "String", "popularity": "Integer" }`
    - `Genre { "name": "String" }`
    - `Release { "id": "String" }`
- **Relationships**: 
    - `User -[:FOLLOWS]-> Artist`
    - `User -[:RATED {"rating": "Integer"}]-> Release`
    - `User -[:FRIENDS_WITH]-> User`
    - `Artist -[:BELONGS_TO]-> Genre`
    - `Artist -[:RELEASED]-> Release`

### Data Population

The project includes a data population script at [scripts/population.ipynb](scripts/population.ipynb).

## Authors

- [Caike dos Santos](https://github.com/CaikeSantos)
- [Ryan Sakurai](https://github.com/ryansakurai)
- [Vinicius Castro](https://github.com/vinciuscastro)
