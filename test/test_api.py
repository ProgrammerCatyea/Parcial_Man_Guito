from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_flujo_basico():
    r = client.post("/api/miembros/", json={"nombre":"Ana Ruiz","rol_general":"PM","estado":"activo"})
    assert r.status_code == 201
    m = r.json()

    r = client.post("/api/proyectos/", json={
        "nombre":"Proyecto Alfa","descripcion":"Core API","presupuesto":10000,
        "estado":"en_progreso","gerente_id": m["id"]
    })
    assert r.status_code == 201
    p = r.json()

    r = client.post("/api/asignaciones/", json={
        "miembro_id": m["id"], "proyecto_id": p["id"], "rol_en_proyecto":"lider"
    })
    assert r.status_code == 201

    r = client.delete(f"/api/miembros/{m['id']}")
    assert r.status_code == 409
