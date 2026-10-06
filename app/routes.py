"""Rutas web (HTML) y API REST (JSON)."""
from flask import Blueprint, abort, current_app, jsonify, redirect, render_template, request

from . import servicio
from .servicio import ErrorValidacion

bp = Blueprint("acortador", __name__)


def url_corta(codigo: str) -> str:
    base = current_app.config.get("BASE_URL") or request.host_url.rstrip("/")
    return f"{base}/{codigo}"


def a_json(enlace: dict) -> dict:
    return {**enlace, "url_corta": url_corta(enlace["codigo"])}


# ---------- Interfaz web ----------
@bp.get("/")
def inicio():
    return render_template("index.html", recientes=servicio.recientes(), url_corta=url_corta)


@bp.post("/")
def crear_desde_formulario():
    try:
        enlace = servicio.acortar(request.form.get("url", ""), request.form.get("alias") or None)
    except ErrorValidacion as e:
        return render_template("index.html", error=str(e), recientes=servicio.recientes(), url_corta=url_corta), 400
    return render_template("index.html", creado=a_json(enlace), recientes=servicio.recientes(), url_corta=url_corta), 201


@bp.get("/<codigo>")
def redirigir(codigo):
    destino = servicio.resolver(codigo)
    if destino is None:
        abort(404)
    return redirect(destino, code=302)


# ---------- API REST ----------
@bp.post("/api/enlaces")
def api_crear():
    datos = request.get_json(silent=True) or {}
    try:
        enlace = servicio.acortar(datos.get("url", ""), datos.get("alias"))
    except ErrorValidacion as e:
        return jsonify(error=str(e)), 400
    return jsonify(a_json(enlace)), 201


@bp.get("/api/enlaces/<codigo>")
def api_estadisticas(codigo):
    enlace = servicio.estadisticas(codigo)
    if enlace is None:
        return jsonify(error="Enlace no encontrado"), 404
    return jsonify(a_json(enlace))


@bp.get("/api/salud")
def salud():
    return jsonify(estado="ok")


@bp.app_errorhandler(404)
def no_encontrado(_):
    if request.path.startswith("/api/"):
        return jsonify(error="Recurso no encontrado"), 404
    return render_template("404.html"), 404
