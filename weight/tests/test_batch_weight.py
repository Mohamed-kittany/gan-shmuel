import pytest
from flask import Flask
from io import BytesIO
from unittest.mock import MagicMock, patch
from routes.batch_weight import bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(bp)
    client = app.test_client()
    yield client

@pytest.fixture
def mock_db():
    with patch('routes.batch_weight.get_db') as mock_get_db:
        mock_db_instance = MagicMock()
        mock_cursor = MagicMock()
        mock_db_instance.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db_instance
        yield mock_db_instance, mock_cursor

def test_batch_weight_no_file(client):
    response = client.post('/batch-weight', data={})
    assert response.status_code == 400
    data = response.get_json()
    if data is None:
        print("Response text:", response.data.decode())  # Debugging line
    else:
        assert 'error' in data
        assert data['error'] == "No file uploaded"


def test_batch_weight_file_uploaded(client, mock_db):
    mock_db_instance, mock_cursor = mock_db
    file_data = BytesIO(b"container_1,100,kg\n")
    
    response = client.post('/batch-weight', content_type='multipart/form-data', data={
        'file': (file_data, 'weights.csv')
    })
    
    # Note: Adjust the status code if you expect something different
    assert response.status_code == 201
    data = response.get_json()
    assert 'status' in data
    assert data['status'] == "success"

if __name__ == '__main__':
    pytest.main()
