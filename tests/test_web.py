def test_pagina_inicio(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Acortador de URLs" in r.get_data(as_text=True)


def test_formulario_crea_enlace(client):
    r = client.post("/", data={"url": "https://example.com", "alias": "ejemplo"})
    assert r.status_code == 201
    assert "http://corto.test/ejemplo" in r.get_data(as_text=True)


def test_formulario_muestra_error(client):
    r = client.post("/", data={"url": "mal"})
    assert r.status_code == 400
    assert "http://" in r.get_data(as_text=True)
