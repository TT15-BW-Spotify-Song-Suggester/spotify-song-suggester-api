from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_valid_input():
    """Return 200 Success when input is valid."""
    response = client.post(
        '/predict',
        json={
            'x1': "https://open.spotify.com/track/7q4JS8fcVlAVnkryc5aBWJ"
        }
    )
    body = response.json()
    assert response.status_code == 200


def test_invalid_input():
    """Return 422 Validation Error when x1 is negative."""
    response = client.post(
        '/predict',
        json={
            'x1': "https://open.spotify.com/track/7q4JS8fcVlAVnkryc5aBWJ"
        }
    )
    body = response.json()
    assert response.status_code == 422
    assert len('x1') == 53
