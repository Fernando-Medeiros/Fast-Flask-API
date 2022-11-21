from flask import Flask

from .routes import register_routes


def app():
    app = Flask(__name__)
    register_routes(app)
    return app