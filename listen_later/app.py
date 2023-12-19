import firebase_admin
from firebase_admin import firestore
from flask import Flask

fb_app = firebase_admin.initialize_app()
db = firestore.client()


def create_app():
    flask_app = Flask(__name__)
    # flask_app.config.from_pyfile(config_filename)

    with flask_app.app_context():
        from listen_later.routes import item, collection, tag, logic

    return flask_app
