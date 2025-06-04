from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'

    from .routes.auth_routes import auth_bp
    from .routes.contract_routes import contract_bp
    from .routes.dashboard_routes import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(contract_bp)
    app.register_blueprint(dashboard_bp)

    return app
