import pytest
from flask import Flask
from unittest.mock import MagicMock, patch
from routes.get_item import bp
import datetime

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(bp)
    client = app.test_client()
    yield client

@pytest.fixture
def mock_db():
    with patch('routes.get_item.get_db') as mock_get_db:
        mock_db_instance = MagicMock()
        mock_cursor = MagicMock()
        mock_db_instance.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db_instance
        yield mock_db_instance, mock_cursor

def test_get_item_not_found(client, mock_db):
    mock_db_instance, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = None  # Simulate item not found

    response = client.get('/item/123')
    
    # Print response details for debugging
    print("Status Code:", response.status_code)
    print("Response Data:", response.get_json())

    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == "Item not found"

def test_get_item_found_no_sessions(client, mock_db):
    mock_db_instance, mock_cursor = mock_db
    # Simulate item found with weight
    mock_cursor.fetchone.side_effect = [{'weight': 100}, []]

    response = client.get('/item/123')
    
    # Print response details for debugging
    print("Status Code:", response.status_code)
    print("Response Data:", response.get_json())

    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data
    assert data['id'] == '123'
    assert 'tara' in data
    assert data['tara'] == 100
    assert 'sessions' in data
    assert data['sessions'] == []

def test_get_item_found_with_sessions(client, mock_db):
    mock_db_instance, mock_cursor = mock_db
    # Simulate item found with weight and sessions
    mock_cursor.fetchone.side_effect = [{'weight': 100}, None]  # First fetchone() for weight, returns a weight
    mock_cursor.fetchall.return_value = [{'id': 1}, {'id': 2}]  # fetchall() for sessions, returns a list of sessions
    
    response = client.get('/item/123')
    
    # Print response details for debugging
    print("Status Code:", response.status_code)
    print("Response Data:", response.get_json())

    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data
    assert data['id'] == '123'
    assert 'tara' in data
    assert data['tara'] == 100
    assert 'sessions' in data
    assert data['sessions'] == [1, 2]

if __name__ == '__main__':
    pytest.main()
