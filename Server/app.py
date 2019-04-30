import json
from flask import Flask
from flask import request
from utils_login import user_login
from utils_enroll import user_enroll
app = Flask(__name__)


@app.route('/enroll', methods="POST")
def enroll():
    data = request.json

    #

    return 'Hello World!'


@app.route('/login', methods="POST")
def login():
    data = request.json
    result = {
        "code": 1,
        "score": 1,
    }
    return json.dumps(result)


if __name__ == '__main__':
    app.run()
