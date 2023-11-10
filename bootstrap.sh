#!/bin/sh
export FLASK_APP=./listen_later/index.py
pipenv run flask --debug run