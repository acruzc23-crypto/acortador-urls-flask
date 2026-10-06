"""Acceso a datos con SQLite."""
import sqlite3

from flask import current_app, g

ESQUEMA = """
CREATE TABLE IF NOT EXISTS enlaces (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo      TEXT    NOT NULL UNIQUE,
    url         TEXT    NOT NULL,
    visitas     INTEGER NOT NULL DEFAULT 0,
    creado_en   TEXT    NOT NULL DEFAULT (datetime('now'))
);
"""


def obtener_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def cerrar_db(_=None) -> None:
    conexion = g.pop("db", None)
    if conexion is not None:
        conexion.close()


def crear_tablas() -> None:
    obtener_db().executescript(ESQUEMA)


def init_app(app) -> None:
    app.teardown_appcontext(cerrar_db)
