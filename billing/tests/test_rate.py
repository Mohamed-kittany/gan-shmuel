from tests import *
## to run a specific pytest use the following command: "pytest path_to_testFile::func_name"


# Template:
# def test_health_check(client):
#     response = client.get('/api/health')
#     assert response.status_code == 200
#     # assert response.data.decode() == 'ok'

# def test_post_rates_success(client, mock_excel_file):
#     """Test successful rates file upload."""
#     route = "/api/rates"
#     headers = {"Content-Type": "multipart/form-data"}
#     files = {"file": (mock_excel_file, "rates.xlsx")}

#     # Send POST request
#     response = client.post(route, data=files, headers=headers)

#     # Assert success response
#     assert response.status_code == 200
#     assert response.json == {"message": "Rates file processed and saved successfully"}


# def test_post_rates_no_file(client):
#     """Test missing file in the payload."""
#     route = "/api/rates"
#     headers = {"Content-Type": "multipart/form-data"}

#     # Send POST request without a file
#     response = client.post(route, data={}, headers=headers)

#     # Assert bad request response
#     assert response.status_code == 400
#     assert response.json == {"error": "No file provided"}


# def test_post_rates_invalid_columns(client, mock_excel_file_invalid_columns):
#     """Test file with missing required columns."""
#     route = "/api/rates"
#     headers = {"Content-Type": "multipart/form-data"}
#     files = {"file": (mock_excel_file_invalid_columns, "rates_invalid_columns.xlsx")}

#     # Send POST request
#     response = client.post(route, data=files, headers=headers)

#     # Assert bad request response
#     assert response.status_code == 400
#     assert "The uploaded file must contain" in response.json["error"]


# def test_post_rates_invalid_data(client, mock_excel_file_invalid_data):
#     """Test file with invalid data types."""
#     route = "/api/rates"
#     headers = {"Content-Type": "multipart/form-data"}
#     files = {"file": (mock_excel_file_invalid_data, "rates_invalid_data.xlsx")}

#     # Send POST request
#     response = client.post(route, data=files, headers=headers)

#     # Assert bad request response
#     assert response.status_code == 400
#     assert "All 'rate' values must be numeric" in response.json["error"]


# def test_get_rates_success(client):
#     """Test retrieving all rates."""
#     route = "/api/rates"

#     # Send GET request
#     response = client.get(route)

#     # Assert success response
#     assert response.status_code == 200
#     assert len(response.json) > 0
#     assert all(key in response.json[0] for key in ["product_id", "rate", "scope"])
