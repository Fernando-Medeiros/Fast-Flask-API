from .controllers import user_controller


def register_routes(app) -> None:
    routes = [
        user_controller.user
    ]

    for router in routes:
        app.register_blueprint(router)