#!/usr/bin/env python3
import base64
import hashlib
import os
import re
import json
import requests
from dotenv import load_dotenv
from requests.auth import AuthBase, HTTPBasicAuth
from requests_oauthlib import OAuth2Session

load_dotenv()

client_id = os.getenv('client-id')
client_secret = os.getenv('client-secret')
redirect_uri = os.getenv('redirect-uri')

# Set the scopes
scopes = ["bookmark.read", "tweet.read", "users.read", "offline.access"]

# Create a code verifier
code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

# Create a code challenge
code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")

# Start an OAuth 2.0 session
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)

# Create an authorize URL
auth_url = "https://twitter.com/i/oauth2/authorize"
authorization_url, state = oauth.authorization_url(
    auth_url, code_challenge=code_challenge, code_challenge_method="S256"
)

# Visit the URL to authorize your App to make requests on behalf of a user
print(
    "Visit the following URL to authorize your App on behalf of your Twitter handle in a browser:"
)
print(authorization_url)

# Paste in your authorize URL to complete the request
authorization_response = input(
    "Paste in the full URL after you've authorized your App:\n"
)

# Fetch your access token
token_url = "https://api.twitter.com/2/oauth2/token"

auth = HTTPBasicAuth(client_id, client_secret)

token = oauth.fetch_token(
    token_url=token_url,
    authorization_response=authorization_response,
    auth=auth,
    client_id=client_id,
    include_client_id=True,
    code_verifier=code_verifier,
)

# Your access token
access = ("access_token=%s" % token["access_token"])

with open(".auth-token","w") as f:
    f.write(access)
