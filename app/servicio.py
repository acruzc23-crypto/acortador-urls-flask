"""Lógica de negocio del acortador, independiente de HTTP."""
import secrets
import sqlite3
import string
from urllib.parse import urlparse

from .db import obtener_db

ALFABETO = string.ascii_letters + string.digits
LONGITUD_CODIGO = 6


class ErrorValidacion(ValueError):
    """Datos de entrada inválidos."""


def validar_url(url: str) -> str:
    url = (url or "").strip()
    partes = urlparse(url)
    if partes.scheme not in ("http", "https") or not partes.netloc:
        raise ErrorValidacion("La URL debe empezar con http:// o https:// y tener un dominio válido")
    if len(url) > 2048:
        raise ErrorValidacion("La URL es demasiado larga")
    return url


def validar_alias(alias: str) -> str:
    alias = alias.strip()
    if not (3 <= len(alias) <= 30) or any(c not in ALFABETO + "-_" for c in alias):
        raise ErrorValidacion("El alias debe tener 3-30 caracteres: letras, números, - o _")
    return alias


def generar_codigo(longitud: int = LONGITUD_CODIGO) -> str:
    return "".join(secrets.choice(ALFABETO) for _ in range(longitud))


def acortar(url: str, alias: str | None = None) -> dict:
    url = validar_url(url)
    db = obtener_db()

    # Si la URL ya existe sin alias personalizado, reutilizamos el código
    if not alias:
        fila = db.execute("SELECT * FROM enlaces WHERE url = ? ORDER BY id LIMIT 1", (url,)).fetchone()
        if fila:
            return dict(fila)

    codigo = validar_alias(alias) if alias else generar_codigo()
    for _ in range(5):
        try:
            db.execute("INSERT INTO enlaces (codigo, url) VALUES (?, ?)", (codigo, url))
            db.commit()
            break
        except sqlite3.IntegrityError:
            if alias:
                raise ErrorValidacion("Ese alias ya está en uso") from None
            codigo = generar_codigo()
    else:  # pragma: no cover - extremadamente improbable
        raise RuntimeError("No se pudo generar un código único")
    return dict(db.execute("SELECT * FROM enlaces WHERE codigo = ?", (codigo,)).fetchone())


def resolver(codigo: str) -> str | None:
    db = obtener_db()
    fila = db.execute("SELECT url FROM enlaces WHERE codigo = ?", (codigo,)).fetchone()
    if fila is None:
        return None
    db.execute("UPDATE enlaces SET visitas = visitas + 1 WHERE codigo = ?", (codigo,))
    db.commit()
    return fila["url"]


def estadisticas(codigo: str) -> dict | None:
    fila = obtener_db().execute("SELECT * FROM enlaces WHERE codigo = ?", (codigo,)).fetchone()
    return dict(fila) if fila else None


def recientes(limite: int = 10) -> list[dict]:
    filas = obtener_db().execute("SELECT * FROM enlaces ORDER BY id DESC LIMIT ?", (limite,)).fetchall()
    return [dict(f) for f in filas]
