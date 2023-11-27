from flask import Flask

app = Flask(__name__)

from listen_later.routes import item, collection, tag

if __name__ == "__main__":
    app.run()