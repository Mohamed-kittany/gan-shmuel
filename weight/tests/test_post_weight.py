import pytest
from flask import Flask
from unittest.mock import MagicMock, patch
from routes.post_weight import bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(bp)
    client = app.test_client()
    yield client

@pytest.fixture
def mock_db():
    with patch('routes.post_weight.get_db') as mock_get_db:
        mock_db_instance = MagicMock()
        mock_cursor = MagicMock()
        mock_db_instance.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db_instance
        yield mock_db_instance, mock_cursor

def test_post_weight_out_no_previous_in_session(client, mock_db):
    mock_db_instance, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = None  # Simulate no previous 'in' session

    response = client.post('/weight', json={
        'direction': 'out',
        'truck': '123ABC',
        'containers': 'some_containers',
        'weight': 1800,
        'unit': 'kg',
        'force': False,
        'produce': 'some_produce'
    })

    print("Status Code:", response.status_code) 
    print("Response Data:", response.get_json())

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == "No previous 'in' session for truck"

def test_post_weight_force_condition(client, mock_db):
    mock_db_instance, mock_cursor = mock_db
    # Mock the queries for existing transaction with direction 'in'
    mock_cursor.fetchone.return_value = {'id': 1}

    response = client.post('/weight', json={
        'direction': 'in',
        'truck': '123ABC',
        'containers': 'some_containers',
        'weight': 2000,
        'unit': 'kg',
        'force': False,
        'produce': 'some_produce'
    })
    print("Status Code:", response.status_code) 
    print("Response Data:", response.get_json())
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == "in already exists for this truck"


if __name__ == '__main__':
    pytest.main()

#================================




