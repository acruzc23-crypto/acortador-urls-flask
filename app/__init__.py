"""Fábrica de la aplicación Flask (patrón Application Factory)."""
import os

from flask import Flask

from . import db
from .routes import bp


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.update(
        DATABASE=os.environ.get("DATABASE_PATH", os.path.join(app.instance_path, "urls.db")),
        BASE_URL=os.environ.get("BASE_URL", ""),
    )
    if config:
        app.config.update(config)

    os.makedirs(os.path.dirname(app.config["DATABASE"]) or ".", exist_ok=True)
    db.init_app(app)
    with app.app_context():
        db.crear_tablas()

    app.register_blueprint(bp)
    return app
