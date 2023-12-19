#!/bin/sh
export FLASK_APP=./listen_later/app.py
pipenv run flask --debug run
