# /billing/app/tests/test_truck.py
from billing import client

def test_post_truck_success(client):
    """Test successful truck creation."""
    data = {"id": "T-004", "provider_id": 1}
    route = "/api/truck"
    headers = {"Content-Type": "application/json"}

    # Send POST request
    response = client.post(route, json=data, headers=headers)

    # Assert success response
    assert response.status_code == 201


# def test_post_truck_missing_truck_id(client):
#     """Test missing truck ID in the payload."""
#     data = {"provider_id": 1}  # Missing "id"
#     route = "/api/truck"
#     headers = {"Content-Type": "application/json"}

#     # Send POST request
#     response = client.post(route, json=data, headers=headers)

#     # Assert bad request response
#     assert response.status_code == 400
#     assert response.json == {"error": "Truck id is required"}


# def test_post_truck_missing_provider_id(client):
#     """Test missing provider ID in the payload."""
#     data = {"id": "T-005"}  # Missing "provider_id"
#     route = "/api/truck"
#     headers = {"Content-Type": "application/json"}

#     # Send POST request
#     response = client.post(route, json=data, headers=headers)

#     # Assert bad request response
#     assert response.status_code == 400
#     assert response.json == {"error": "Provider id is required"}


# def test_post_truck_conflict_truck_id(client):
#     """Test conflict if truck ID already exists."""
#     data = {"id": "T-001", "provider_id": 1}  # T-001 already exists
#     route = "/api/truck"
#     headers = {"Content-Type": "application/json"}

#     # Send POST request
#     response = client.post(route, json=data, headers=headers)

#     # Assert conflict response
#     assert response.status_code == 409
#     assert response.json == {"error": "A truck with this id already exists."}


# def test_post_truck_invalid_provider_id(client):
#     """Test invalid provider ID during truck creation."""
#     data = {"id": "T-006", "provider_id": 999}  # Invalid provider ID
#     route = "/api/truck"
#     headers = {"Content-Type": "application/json"}

#     # Send POST request
#     response = client.post(route, json=data, headers=headers)

#     # Assert conflict response
#     assert response.status_code == 409
#     assert response.json == {"error": "There is no provider with the '999' id"}


# def test_put_truck_success(client):
#     """Test successful truck update."""
#     data = {"provider_id": 2}
#     route = "/api/truck/T-001"
#     headers = {"Content-Type": "application/json"}

#     # Send PUT request
#     response = client.put(route, json=data, headers=headers)

#     # Assert success response
#     assert response.status_code == 200
#     assert response.json == {"message": "Truck updated successfully"}


# def test_put_truck_missing_provider_id(client):
#     """Test missing provider ID during truck update."""
#     data = {}  # Missing "provider_id"
#     route = "/api/truck/T-001"
#     headers = {"Content-Type": "application/json"}

#     # Send PUT request
#     response = client.put(route, json=data, headers=headers)

#     # Assert bad request response
#     assert response.status_code == 400
#     assert response.json == {"error": "Provider id is required"}


# def test_put_truck_invalid_truck_id(client):
#     """Test updating a non-existent truck ID."""
#     data = {"provider_id": 1}
#     route = "/api/truck/T-999"  # Invalid truck ID
#     headers = {"Content-Type": "application/json"}

#     # Send PUT request
#     response = client.put(route, json=data, headers=headers)

#     # Assert not found response
#     assert response.status_code == 404
#     assert response.json == {"error": "A truck with this id dosnt exists."}

# def test_put_truck_invalid_provider_id(client):
#     """Test invalid provider ID during truck update."""
#     data = {"provider_id": 999}  # Invalid provider ID
#     route = "/api/truck/T-001"
#     headers = {"Content-Type": "application/json"}

#     # Send PUT request
#     response = client.put(route, json=data, headers=headers)

#     # Assert conflict response
#     assert response.status_code == 404
#     assert response.json == {"error": "There is no provider with the '999' id"}
