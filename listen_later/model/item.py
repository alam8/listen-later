from collections import namedtuple
import datetime as dt
import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from marshmallow import fields, post_load, Schema
import requests

from listen_later.constants import *

CONTENT_URL_NETLOC = "open.spotify.com"
API_URL_BASE = "https://api.spotify.com/v1/"

load_dotenv()


def parse_content_link(content_link):
    parsed_url = urlparse(content_link)
    path = parsed_url.path.split("/")

    ContentValues = namedtuple("ContentValues", ["content_type", "content_id"])

    content_type = path[1]
    content_id = path[2]

    if parsed_url.netloc != CONTENT_URL_NETLOC:
        raise ValueError("Content link does not have expected domain 'open.spotify.com'.")

    return ContentValues(content_type, content_id)


class Item(object):
    def __init__(self, id, date_added, content_link, rating, listened):
        self.id = id or ""
        self.content_link = content_link
        self.rating = rating or None
        self.listened = listened or False
        self.date_added = date_added or dt.datetime.now()

        # TODO: use Spotify API to get name, artists, images, type, etc. from content_link
        #       and add validation for content_link, also those fields need to be updated if
        #       content_link is updated
        content_values = parse_content_link(self.content_link)
        access_response = requests.post("https://accounts.spotify.com/api/token",
                                     headers={"content-type": "application/x-www-form-urlencoded"},
                                     data={"grant_type": "client_credentials",
                                           "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
                                           "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET")}
                                     )
        access_response.raise_for_status()
        access_token = access_response.json()["access_token"]
        print(access_token)
        content_response = requests.get(API_URL_BASE + content_values.content_type + "s/" + content_values.content_id,
                                headers={"Authorization": "Bearer " + access_response})
        content_response.raise_for_status()
        print(content_response.json()["name"])
        self.item_type_id = None

    def __repr__(self):
        return f"{ITEM_TYPE}({ID}={self.id!r})".format(self=self)


class ItemSchema(Schema):
    id = fields.String(missing="")
    date_added = fields.DateTime(missing=dt.datetime.now())
    content_link = fields.String()
    rating = fields.Int(missing=None)
    listened = fields.Boolean(missing=False)

    @post_load
    def make_item(self, data, **kwargs):
        return Item(**data)


class ItemUpdateSchema(Schema):
    content_link = fields.String()
    rating = fields.Int()
    listened = fields.Boolean()
