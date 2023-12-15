from flask import Flask
import firebase_admin
from firebase_admin import firestore
from listen_later.model.constants import USERS, TEST_USER

app = Flask(__name__)
fb_app = firebase_admin.initialize_app()
db = firestore.client()
# TODO: replace test user id w/ one fetched by authorization handler
user_ref = db.collection(USERS).document(TEST_USER)

def not_found_error(type, pk):
    return {"errors": f"{type}(id={pk}) could not be found"}, 404

from listen_later.routes import item, collection, tag, logic

if __name__ == "__main__":
    app.run()