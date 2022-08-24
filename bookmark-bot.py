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
import sqlite3

def setup_db(con):
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS bookmarks(tweet_id TEXT, bookmark TEXT)")
    return cur

def connect_db():
    con = sqlite3.connect("bookmarks.db")
    cur = setup_db(con)
    return con, cur

def save(con,cur, data):
    cur.execute("SELECT COUNT(*) FROM bookmarks WHERE tweet_id = ?", (data['id'],))
    
    if cur.fetchall()[0][0] >= 1:
        print("not saving dupe entry..")
        return
    else:
        print("adding entry..")
        cur.execute("INSERT INTO bookmarks(tweet_id, bookmark) VALUES(?,?)", (data['id'],data['text'],))
        con.commit()

def dump(cur):
    rows = cur.execute("SELECT rowId, tweet_id, bookmark FROM bookmarks").fetchall()
    print(rows)

def main():
    dotenv_path = Path('.auth-token')
    load_dotenv(dotenv_path=dotenv_path)
    access = os.getenv('access_token')

    # TODO: exit if no access token found

    # setup the database connection
    con,cur = connect_db()

    # TODO: move these to a class

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

    for bookmark in response.json()['data']:
        save(con,cur, bookmark)
    
    # TODO: display bookmarks nicely. 
    # for now, just dump the contents of the db
    print("=========")
    dump(cur)

    con.close()


if __name__ == "__main__":
    main()
