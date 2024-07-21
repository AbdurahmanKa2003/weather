import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_get_weather(client):
    rv = client.get('/weather?city=Berlin')
    assert rv.status_code == 200
    assert 'hourly' in rv.json
