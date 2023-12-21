from listen_later.constants import USERS, TEST_USER
from listen_later.app import db

# TODO: after implementing user authentication:
#       - replace TEST_USER with the user id fetched by the authentication handler
#       - upon user creation, set their id, user_name, date_created, etc. fields
#         and initialize their all_collection with id, collection_name, and date_added fields
user_ref = db.collection(USERS).document(TEST_USER)
