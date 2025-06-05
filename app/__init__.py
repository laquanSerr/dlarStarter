from flask import Flask
from app.extensions import db
from app.models import User, Company, Contract

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Register blueprints here
    from app.routes.auth_routes import auth_blueprint
    from app.routes.contract_routes import contract_blueprint
    from app.routes.dashboard_routes import dashboard_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(contract_blueprint)
    app.register_blueprint(dashboard_blueprint)

    return app
