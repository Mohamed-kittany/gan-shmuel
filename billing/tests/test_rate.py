import os

def test_process_rates_file_success(client):
    """Test successful upload and processing of a valid rates file."""
    # Create a dummy rates file
    file_content = b"Product,Rate,Scope\nApple,100,ALL\nOrange,200,Provider1"
    file_name = "rates.xlsx"
    file_path = os.path.join(os.getcwd(), "tests", file_name)

    with open(file_path, "wb") as f:
        f.write(file_content)

    # Simulate POST /rates with a valid file
    with open(file_path, "rb") as test_file:
        response = client.post('/rates', data={'file': (test_file, file_name)})

    assert response.status_code == 200
    assert response.json["message"] == "Rates file processed and saved successfully"

    # Cleanup
    os.remove(file_path)

def test_download_rates_file_not_found(client):
    """Test download rates file when file does not exist."""
    response = client.get('/rates')
    assert response.status_code == 404
    assert response.json["error"] == "Rates file not found"

def test_update_rate_success(client):
    """Test updating a rate successfully."""
    # Add a mock rate to the database first (mock ORM or actual DB setup required)
    # For now, assume rate with ID 1 exists
    response = client.put('/rates/1', json={"Rate": 150})
    assert response.status_code == 200
    assert response.json["Rate"] == 150
