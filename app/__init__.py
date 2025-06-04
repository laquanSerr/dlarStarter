from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecret'  # Use .env in real apps

    from app.routes.contracts import contracts_blueprint
    app.register_blueprint(contracts_blueprint)

    return app
