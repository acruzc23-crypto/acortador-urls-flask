def test_salud(client):
    assert client.get("/api/salud").get_json() == {"estado": "ok"}


def test_crear_enlace(client):
    r = client.post("/api/enlaces", json={"url": "https://unemi.edu.ec"})
    assert r.status_code == 201
    datos = r.get_json()
    assert len(datos["codigo"]) == 6
    assert datos["url_corta"] == f"http://corto.test/{datos['codigo']}"


def test_misma_url_reutiliza_codigo(client):
    a = client.post("/api/enlaces", json={"url": "https://python.org"}).get_json()
    b = client.post("/api/enlaces", json={"url": "https://python.org"}).get_json()
    assert a["codigo"] == b["codigo"]


def test_alias_personalizado_y_duplicado(client):
    r = client.post("/api/enlaces", json={"url": "https://github.com", "alias": "mi-github"})
    assert r.get_json()["codigo"] == "mi-github"
    r2 = client.post("/api/enlaces", json={"url": "https://otro.com", "alias": "mi-github"})
    assert r2.status_code == 400
    assert "en uso" in r2.get_json()["error"]


def test_url_invalida(client):
    for mala in ["", "ftp://x.com", "no-es-url", "http://"]:
        r = client.post("/api/enlaces", json={"url": mala})
        assert r.status_code == 400


def test_alias_invalido(client):
    r = client.post("/api/enlaces", json={"url": "https://a.com", "alias": "a b"})
    assert r.status_code == 400


def test_redireccion_cuenta_visitas(client):
    codigo = client.post("/api/enlaces", json={"url": "https://flask.palletsprojects.com"}).get_json()["codigo"]
    r = client.get(f"/{codigo}")
    assert r.status_code == 302
    assert r.headers["Location"] == "https://flask.palletsprojects.com"
    client.get(f"/{codigo}")
    assert client.get(f"/api/enlaces/{codigo}").get_json()["visitas"] == 2


def test_codigo_inexistente(client):
    assert client.get("/noexiste").status_code == 404
    assert client.get("/api/enlaces/noexiste").status_code == 404
