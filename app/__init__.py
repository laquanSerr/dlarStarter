from flask import Flask
from app.extensions import db
from app.models import User, Company, Contract
from flask_login import LoginManager
import os

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "fallback-key-for-dev")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #Extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints here
    from app.routes.auth_routes import auth_blueprint
    from app.routes.contract_routes import contract_blueprint
    from app.routes.dashboard_routes import dashboard_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(contract_blueprint)
    app.register_blueprint(dashboard_blueprint)

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
