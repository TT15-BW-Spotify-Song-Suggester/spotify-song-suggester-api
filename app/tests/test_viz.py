from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_valid_input():
    """Return 200 Success for valid 2 character US state postal code."""
    response = client.get('/viz')
    assert response.status_code == 200
    assert 'danceability' in response.text


def test_invalid_input():
    """Return 404 if the endpoint isn't valid US state postal code."""
    response = client.get('/viz')
    body = response.json()
    assert response.status_code == 404
    assert body['detail'] == 'Song not found, check URL'
