from tests import client 

## to run a specific pytest use the following command: "pytest path_to_testFile::func_name"


#template:
# def test_health_check(client):
#     response = client.get('/api/health')
#     assert response.status_code == 200
#     #assert response.data.decode() == 'ok'  




def test_post_provider_success(client):
    """Test successful provider creation."""
    # Define the input data
    data = {"name": "test2"}
    route = '/api/provider'
    headers = {"Content-Type": "application/json"}
    
    # Send POST request
    response = client.post(route, json=data, headers=headers)
    
    # Assert success response
    assert response.status_code == 201
    assert "id" in response.json  # Ensure an ID is returned


# def test_post_provider_missing_name(client):
#     """Test missing provider name in the payload."""
#     data = {}  # No name provided
#     route = '/api/provider'
#     headers = {"Content-Type": "application/json"}
    
#     # Send POST request
#     response = client.post(route, json=data, headers=headers)
    
#     # Assert bad request response
#     assert response.status_code == 400
#     assert response.json == {"error": "Provider name is required"}


# def test_post_provider_conflict(client):
#     """Test conflict error when creating a provider."""
#     # First, create a provider to cause a conflict
#     data = {"name": "test2"}
#     route = '/api/provider'
#     headers = {"Content-Type": "application/json"}
    
#     # Send initial POST request to create the provider
#     response = client.post(route, json=data, headers=headers)
#     assert response.status_code == 201

#     # Send the same request again to trigger a conflict
#     response = client.post(route, json=data, headers=headers)
#     assert response.status_code == 409
#     assert response.json == {"error": "A provider with this name already exists."}


# def test_put_provider_success(client):
#     """Test successful provider update."""
#     # Input data
#     provider_id = 1
#     data = {"name": "Updated Name"}
#     route = f'/api/provider/{provider_id}'
#     headers = {"Content-Type": "application/json"}

#     # Send PUT request
#     response = client.put(route, json=data, headers=headers)

#     # Assert success response
#     assert response.status_code == 200
#     assert response.json == {"message": "Provider updated successfully"}


# def test_put_provider_missing_name(client):
#     """Test missing provider name in the payload."""
#     provider_id = 1
#     data = {}  # No name provided
#     route = f'/api/provider/{provider_id}'
#     headers = {"Content-Type": "application/json"}

#     # Send PUT request
#     response = client.put(route, json=data, headers=headers)

#     # Assert bad request response
#     assert response.status_code == 400
#     assert response.json == {"error": "Provider name is required"}


# def test_put_provider_not_found(client):
#     """Test updating a non-existent provider."""
#     provider_id = 999  # Non-existent provider ID
#     data = {"name": "Updated Name"}
#     route = f'/api/provider/{provider_id}'
#     headers = {"Content-Type": "application/json"}

#     # Send PUT request
#     response = client.put(route, json=data, headers=headers)

#     # Assert not found response
#     assert response.status_code == 404
#     assert "error" in response.json




