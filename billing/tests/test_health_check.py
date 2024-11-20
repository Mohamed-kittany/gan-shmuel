#/billing/app/tests/test_health_check.py
from billing.tests import client 
## to run a specific pytest use the following command: "pytest path_to_testFile::func_name"

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    #assert response.data.decode() == 'ok'  