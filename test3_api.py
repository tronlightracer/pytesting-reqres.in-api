import pytest
import requests
import json as jsn

"""
These tests test all of the api endpoints for 'reqres.in utilizing the python requests and pytest libraries'
"""

url = "https://reqres.in"
header1 = {"Content-Type": "application/json"}

def requests_200():
    get_user = requests.get(url + "/api/users/2")
    get_users = requests.get(url + "/api/users?page=2")
    get_list_resource = requests.get(url, "/api/unknown")
    get_resource = requests.get(url + "/api/unknown/2")
    get_resource_not_found = requests.get(url, "/api/unknown/23")
    get_delayed_response = requests.get(url + "/api/users?delay=3")

    post_register = requests.post(
        url + "/api/register",
        headers=header1,
        json={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
    )
    post_login = requests.post(
        url + "/api/login",
        headers=header1,
        json={
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        }
    )

    put_update = requests.put(
        url + "/api/users/2",
        headers=header1,
        json={
            "name": "morpheus",
            "job": "zion resident"
        }
    )

    patch_update = requests.patch(
        url + "/api/users/2",
        headers=header1,
        json={"name": "morpheus", "job": "zion resident"}
    )

    return [
        get_user,
        get_users,
        get_list_resource,
        get_resource,
        get_resource_not_found,
        get_delayed_response,
        post_register,
        post_login,
        put_update,
        patch_update]

def requests_201():
    create_user = requests.post(
        url + "/api/users",
        headers=header1,
        json={"name": "morpheus", "job": "leader"}
    )
    return create_user

def requests_204():
    delete_user = requests.delete(
        url + "/api/users/2",
        headers=header1
    )
    return delete_user

def requests_400():
    unsuccessful_register = requests.post(
        url + "/api/register",
        headers=header1,
        json={"email": "sydney@fife.com"}
    )

    unsuccessful_login = requests.post(
        url + "/api/login",
        headers=header1,
        json={"email": "peter@klaven"}
    )

    return [unsuccessful_register, unsuccessful_login]

@pytest.mark.parametrize("responses",[
    requests_200()[0],
    requests_200()[1],
    requests_200()[2],
    requests_200()[3],
    requests_200()[4],
    requests_200()[5],
    requests_200()[6],
    requests_200()[7],
    requests_200()[8],
    requests_200()[9]])
def test_200(responses):
    assert responses.status_code == 200
# def test_200(requests_200):
#     for status_code in requests_200:
#         assert status_code == 200


def test_201():
    assert requests_201().status_code == 201

def test_204():
    assert requests_204().status_code == 204

@pytest.mark.parametrize("responses", [requests_400()[0], requests_400()[1]])
def test_400(responses):
    assert responses.status_code == 400

def test_json_responses():
    users_request = requests_200()[1].json()
    users_file = jsn.load(open("json_files/get_users.json"))
    user_request = requests_200()[0].json()
    user_file = jsn.load(open("json_files/get_user.json"))
    # list_resource = requests_200()[2].json()
    # list_file = jsn.load(open("json_files/get_list_resource.json"))
    resource_request = requests_200()[3].json()
    resource_file = jsn.load(open("json_files/resource.json"))
    #resource_not_found_request = requests_200()[4].json() # json = {}
    get_delayed_request = requests_200()[4].json()
    delayed_response_file = jsn.load(open("json_files/delayed_response.json"))
    
    assert users_request == users_file
    assert user_request == user_file
    # assert list_resource == list_file
    assert resource_request == resource_file
    #assert resource_not_found_request == {}
    assert get_delayed_request == delayed_response_file

print(test_json_responses())
