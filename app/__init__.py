from flask import Flask
from app.routes import contracts

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"  # Or load from .env

    app.register_blueprint(contracts.bp)

    return app

