def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth_routes import auth_blueprint
    from app.routes.contract_routes import contracts_blueprint
    from app.routes.dashboard_routes import dashboard_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(contracts_blueprint)
    app.register_blueprint(dashboard_blueprint)

    return app
