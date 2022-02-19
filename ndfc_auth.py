#!/usr/bin/python
def auth(nd_ip, nd_user, nd_pass):
    import requests
    import json
    import urllib3
    urllib3.disable_warnings()
    url = f"https://{nd_ip}/login"
    payload={"userName": nd_user,
             "userPasswd": nd_pass,
             "domain": "DefaultAuth"}
    headers = {
              'Content-Type': 'application/json',
              } 

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)
    output = json.loads(response.text)
    auth_token = 'Bearer '+ output["jwttoken"]
    return auth_token
