# -*- coding: utf-8 -*-
"""
    Author: KaiyanZhang
    Date：  2019/4/30 14:30 
    Description: 
"""
import json
import base64
import requests

def read(file):
    with open(file, "rb") as f:
        audio = base64.b64encode(f.read())
    # bytes => str
    audio_ = audio.decode("ascii")
    return audio_

def enroll():
    """"""
    username = "1006"
    files = ["audios/%s_enroll_%d.wav" % (username, idx + 1) for idx in range(3)]
    data = {
        "username": username,
        "audios": [read(file) for file in files]
    }
    resp = requests.post("http://39.105.35.211:11111/test_enroll", json=json.dumps(data))
    print(resp.text)

def login():
    username = "1006"
    data = {
        "username": username,
        "audio": read("audios/%s_login.wav" % username)
    }
    # resp = requests.post("http://39.105.35.211:11111/test_login", json=json.dumps(data))
    # print(resp.text)


if __name__ == '__main__':
    #enroll()
    login()