"""
Server for the music catalog API
"""
from flask import Flask
from configs import mongodb, neo4j
from routes import artists, releases, users, recs

app = Flask("Music Catalog API")
app.json.sort_keys = False
app.url_map.strict_slashes = False


app.register_blueprint(artists.bp, url_prefix = "/v1/artists")
app.register_blueprint(releases.bp, url_prefix = "/v1/releases")
app.register_blueprint(users.bp, url_prefix = "/v1/users")
app.register_blueprint(recs.bp, url_prefix = "/v1/recs")

if __name__=="__main__":
    app.run(debug = True)

    mongodb.client.close()
    neo4j.driver.close()
