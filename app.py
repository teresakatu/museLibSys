import os

from dotenv import load_dotenv
from flask import Flask

import db
from routes import account, auth, library, main, playlists, songs, trending

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    db.init_app(app)
    for module in (auth, main, songs, library, playlists, trending, account):
        app.register_blueprint(module.bp)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
