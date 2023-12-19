import firebase_admin
from firebase_admin import firestore
from flask import Flask

from listen_later.constants import USERS, TEST_USER

flask_app = Flask(__name__)
fb_app = firebase_admin.initialize_app()
db = firestore.client()

# TODO: replace test user id w/ one fetched by authorization handler
user_ref = db.collection(USERS).document(TEST_USER)

from listen_later.routes import item, collection, tag, logic

if __name__ == "__main__":
    flask_app.run()
