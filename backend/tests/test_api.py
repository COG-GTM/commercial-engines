def _engine_by_serial(client, serial):
    engines = client.get("/api/v1/engines").json()
    return next(e for e in engines if e["serial"] == serial)


def test_health(client):
    assert client.get("/api/v1/health").json() == {"status": "ok"}


def test_list_engines_seeded(client):
    engines = client.get("/api/v1/engines").json()
    serials = {e["serial"] for e in engines}
    assert {"TF9-001234", "TF9-002000", "TF7X-000100"} <= serials
    assert all(e["family"].startswith("TF-") for e in engines)


def test_get_engine_detail(client):
    e = _engine_by_serial(client, "TF9-001234")
    detail = client.get(f"/api/v1/engines/{e['id']}").json()
    assert detail["operatorName"] == "Northwind Air"
    assert detail["csn"] > 0


def test_engine_sb_records(client):
    e = _engine_by_serial(client, "TF9-001234")
    records = client.get(f"/api/v1/engines/{e['id']}/sb-records").json()
    assert len(records) >= 1
    assert {"sbNumber", "status"} <= set(records[0])


def test_list_service_bulletins(client):
    sbs = client.get("/api/v1/service-bulletins").json()
    numbers = {s["sbNumber"] for s in sbs}
    assert "TF9-72-0031" in numbers
    tf9 = client.get("/api/v1/service-bulletins?family=TF-9").json()
    assert all(s["family"] == "TF-9" for s in tf9)


def test_get_service_bulletin(client):
    sbs = client.get("/api/v1/service-bulletins").json()
    sb = client.get(f"/api/v1/service-bulletins/{sbs[0]['id']}").json()
    assert sb["sbNumber"] == sbs[0]["sbNumber"]


def test_list_shop_visits(client):
    visits = client.get("/api/v1/shop-visits").json()
    assert len(visits) >= 1
    assert {"engineSerial", "status", "workscope"} <= set(visits[0])


def test_engine_shop_visits(client):
    e = _engine_by_serial(client, "TF9-001234")
    visits = client.get(f"/api/v1/engines/{e['id']}/shop-visits").json()
    assert all(v["engineSerial"] == "TF9-001234" for v in visits)


def test_release_shop_visit_transitions_to_released(client):
    visits = client.get("/api/v1/shop-visits").json()
    open_visit = next(v for v in visits if v["status"] != "RELEASED")
    resp = client.post(
        f"/api/v1/shop-visits/{open_visit['id']}/release", json={"releasedBy": "qa.tester"}
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "RELEASED"


def test_release_already_released_conflicts(client):
    visits = client.get("/api/v1/shop-visits").json()
    released = next((v for v in visits if v["status"] == "RELEASED"), None)
    assert released is not None
    resp = client.post(
        f"/api/v1/shop-visits/{released['id']}/release", json={"releasedBy": "qa.tester"}
    )
    assert resp.status_code == 409


def test_get_missing_engine_404(client):
    assert client.get("/api/v1/engines/999999").status_code == 404
