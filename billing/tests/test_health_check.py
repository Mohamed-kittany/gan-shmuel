#/billing/app/tests/test_health_check.py
from tests import client 

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    #assert response.data.decode() == 'ok'  