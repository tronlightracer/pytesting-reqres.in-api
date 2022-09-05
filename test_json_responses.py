from test3_api import requests_200
import json as jsn
def test_json_responses2():
    users_request = requests_200()[1].json()
    users_file = jsn.load(open("json_files/get_users.json", "r"))
    user_request = requests_200()[0].json()
    user_file = jsn.load(open("json_files/get_user.json"))
    # list_resource = requests_200()[2].json()
    # list_file = jsn.load(open("json_files/get_list_resource.json"))
    #resource_request = requests_200()[3].json()
    #resource_file = jsn.load(open("json_files/resource.json"))
    
    assert users_request == users_file
    assert user_request == user_file
    # assert list_resource == list_file
    #assert resource_request == resource_file

print(test_json_responses2())

