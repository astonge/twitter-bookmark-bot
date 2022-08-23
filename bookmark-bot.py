#!/usr/bin/env python3
import base64
import hashlib
import os
import re
import json
import requests
from dotenv import load_dotenv
from pathlib import Path
from requests.auth import AuthBase, HTTPBasicAuth
from requests_oauthlib import OAuth2Session


dotenv_path = Path('.auth-token')
load_dotenv(dotenv_path=dotenv_path)
access = os.getenv('access_token')

# Make a request to the users/me endpoint to get your user ID
user_me = requests.request(
    "GET",
    "https://api.twitter.com/2/users/me",
    headers={"Authorization": "Bearer {}".format(access)},
).json()
user_id = user_me["data"]["id"]

# Make a request to the bookmarks url
url = "https://api.twitter.com/2/users/{}/bookmarks".format(user_id)
headers = {
    "Authorization": "Bearer {}".format(access),
    "User-Agent": "BookmarksSampleCode",
}
response = requests.request("GET", url, headers=headers)
if response.status_code != 200:
    raise Exception(
        "Request returned an error: {} {}".format(response.status_code, response.text)
    )
#print("Response code: {}".format(response.status_code))
json_response = response.json()
#print(json.dumps(json_response, indent=4, sort_keys=True))
for bookmark in json_response['data']:
    print(bookmark['text'])
    print("---")


