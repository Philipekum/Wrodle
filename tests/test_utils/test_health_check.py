from tests.conftest import client


def test_healtcheck():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()
