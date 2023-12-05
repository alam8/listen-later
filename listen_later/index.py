from flask import Flask
import firebase_admin
from firebase_admin import firestore

app = Flask(__name__)
fb_app = firebase_admin.initialize_app()
db = firestore.client()

from listen_later.routes import item, collection, tag

if __name__ == "__main__":
    app.run()