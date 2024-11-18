# from tests import client 

## to run a specific pytest use the following command: "pytest path_to_testFile::func_name"


# #template:
# # def test_health_check(client):
# #     response = client.get('/api/health')
# #     assert response.status_code == 200
# #     #assert response.data.decode() == 'ok'  

# def test_get_provider(client):
#     data = {
#         "name" : "test2",
#         "id" : 125
#     }
#     route = '/api/provider'
#     headers={"Content-Type": "application/json"}
#     response = client.post(route,json=data,headers=headers)

#     assert response.status_code == 201
