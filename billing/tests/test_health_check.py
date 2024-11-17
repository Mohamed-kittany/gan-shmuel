from flask import Flask
import pytest

app = Flask(__name__)

@app.route('/health', methods=['POST'])
def health():
    return 'ok', 200

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.post('/health')
    assert response.status_code == 200
    assert response.data.decode() == 'ok'
