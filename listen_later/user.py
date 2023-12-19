from listen_later.constants import USERS, TEST_USER
from listen_later.app import db

# TODO: replace test user id w/ one fetched by authorization handler
user_ref = db.collection(USERS).document(TEST_USER)
