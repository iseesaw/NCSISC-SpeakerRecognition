import json
from flask import Flask
from flask import request
from utils_login import user_login
from utils_enroll import user_enroll
from utils_enroll import enroll_generate
from utils_login import login_generate
import pymysql

app = Flask(__name__)


@app.route('/enroll_account', methods=["POST"])
def enroll_account():
    # 连接数据库
    db = pymysql.connect("localhost", "root", "123456", "server_database")
    # 使用cursor()获取操作游标
    cursor = db.cursor()
    # 解析json文件
    data = request.json
    msgtype = data['msgType']
    packageIndex = data['packageIndex']
    md5 = data['md5']
    content = data['content']
    telephone = data['telephone']
    # 对数据包生成时间的验证
    cursor.execute("select * from react_time where telephone = " + telephone + ";")
    rs = cursor.fetchone()
    if rs:
        prev_time = rs[2]
        if prev_time >= packageIndex:
            db.close()
            return -1
        else:
            print("注册账户流程：访问时间更新")
            sqlstate = "update react_time set time = ? where telephone = ?;"
            cursor.execute(sqlstate, (packageIndex, telephone))
            db.commit()
    else:
        print("注册账户流程：访问时间首次接收")
        sqlstate = "insert into react_time(telephone, time) values(?,?);"
        cursor.execute(sqlstate, (telephone, packageIndex))
    password = content['password']
    read_number = content['read_number']
    sqlstate = "select * from user_infos where telephone = ?;"
    cursor.execute(sqlstate, telephone)
    result = cursor.fetchone()
    if result:
        print("注册账户流程：注册账户已存在")
        # 关闭数据库连接
        db.close()
        return 5
    else:
        print("注册账户流程：账户合法，无重复注册现象")
        sqlstate = "insert into user_infos(telephone, password, read_number) " \
                   "values(?,?,?);"
        cursor.execute(sqlstate, (telephone, password))
        db.commit()
        print("注册账户流程：账户信息成功写入数据库")
        # 关闭数据库连接
        db.close()
        return 6


@app.route('/enroll_model', methods=["POST"])
def enroll_model():
    # 连接数据库
    db = pymysql.connect("localhost", "root", "123456", "server_database")
    # 使用cursor()获取操作游标
    cursor = db.cursor()
    # 解析json文件
    data = request.json
    msgtype = data['msgType']
    packageIndex = data['packageIndex']
    md5 = data['md5']
    content = data['content']
    telephone = data['telephone']
    # 对数据包生成时间的验证
    cursor.execute("select * from react_time where telephone = " + telephone + ";")
    rs = cursor.fetchone()
    if rs:
        prev_time = rs[2]
        if prev_time >= packageIndex:
            db.close()
            return 15
        else:
            print("注册模型流程：访问时间更新")
            sqlstate = "update react_time set time = ? where telephone = ?;"
            cursor.execute(sqlstate, (packageIndex, telephone))
            db.commit()
    else:
        print("注册模型流程：访问时间首次接收")
        sqlstate = "insert into react_time(telephone, time) values(?,?);"
        cursor.execute(sqlstate, (telephone, packageIndex))
    with open("/root/ASR/audios/" + telephone + "_enroll_1.wav", "wb") as f1:
        f1.write(content['voice1'])
    with open("/root/ASR/audios/" + telephone + "_enroll_2.wav", "wb") as f2:
        f2.write(content['voice2'])
    with open("/root/ASR/audios/" + telephone + "_enroll_3.wav", "wb") as f3:
        f3.write(content['voice3'])
    result = enroll_generate(telephone)
    print("注册模型阶段：返回结果: " + result)
    if result == "Yes":
        print("注册模型阶段：注册成功")
        # 关闭数据库连接
        db.close()
        return 7
    else:
        print("注册模型阶段：注册失败")
        # 关闭数据库连接
        db.close()
        return 8


@app.route('/login_account', methods=["POST"])
def login_account():
    # 连接数据库
    db = pymysql.connect("localhost", "root", "123456", "server_database")
    # 使用cursor()获取操作游标
    cursor = db.cursor()
    # 解析json文件
    data = request.json
    msgtype = data['msgType']
    packageIndex = data['packageIndex']
    md5 = data['md5']
    content = data['content']
    telephone = data['telephone']
    # 对数据包生成时间的验证
    cursor.execute("select * from react_time where telephone = " + telephone + ";")
    rs = cursor.fetchone()
    if rs:
        prev_time = rs[2]
        if prev_time >= packageIndex:
            db.close()
            return 15
        else:
            print("登录账号流程：访问时间更新")
            sqlstate = "update react_time set time = ? where telephone = ?;"
            cursor.execute(sqlstate, (packageIndex, telephone))
            db.commit()
    else:
        print("登录账号流程：访问时间首次接收")
        sqlstate = "insert into react_time(telephone, time) values(?,?);"
        cursor.execute(sqlstate, (telephone, packageIndex))
    password = content['password']
    sqlstate = "select * from user_infos where telephone = ?;"
    rs = cursor.execute(sqlstate, telephone)
    if not rs:
        print("账户登录流程：用户未注册")
        db.close()
        return 9
    else:
        sqlstate = "SELECT * from user_infos WHERE telephone= ?;"
        cursor.execute(sqlstate, telephone)
        rs = cursor.fetchone()
        if rs:
            passwd = rs['password']
            if passwd == password:
                return str(11) + " " + rs['read_number']
            db.close()
            return 10

import base64
def saveAudio(filename, audio):
    s = audio.encode('ascii')
    with open("/root/ASR/audios/%s.wav" % filename, "wb") as f1:
        f1.write(base64.b64decode(s))


@app.route('/test_enroll', methods=["POST"])
def test_enroll():
    data = request.json
    data = json.loads(data)
    username = data["username"]
    for idx, audio in enumerate(data["audios"]):
        saveAudio("%s_enroll_%d" % (username, idx + 1), audio)
    result = user_enroll(username)
    print(username)
    return result


@app.route('/test_login', methods=["POST"])
def test_login():
    data = request.json
    data = json.loads(data)
    username = data["username"]
    saveAudio("%s_login" % username, data["audio"])
    result = user_login(username)
    return result


@app.route('/login_model', methods=["POST"])
def login_model():
    # 连接数据库
    db = pymysql.connect("localhost", "root", "123456", "server_database")
    # 使用cursor()获取操作游标
    cursor = db.cursor()
    # 解析json文件
    data = request.json
    msgtype = data['msgType']
    packageIndex = data['packageIndex']
    md5 = data['md5']
    content = data['content']
    telephone = data['telephone']
    # 对数据包生成时间的验证
    cursor.execute("select * from react_time where telephone = " + telephone + ";")
    rs = cursor.fetchone()
    if rs:
        prev_time = rs[2]
        if prev_time >= packageIndex:
            db.close()
            return 15
        else:
            print("登录模型流程：访问时间更新")
            sqlstate = "update react_time set time = ? where telephone = ?;"
            cursor.execute(sqlstate, (packageIndex, telephone))
            db.commit()
    else:
        print("登录模型流程：访问时间首次接收")
        sqlstate = "insert into react_time(telephone, time) values(?,?);"
        cursor.execute(sqlstate, (telephone, packageIndex))
    voice = content['voice1']
    with open("/root/ASR/audios/" + telephone + "_login.wav", "wb") as f1:
        f1.write(content['voice1'])
    result = login_generate(telephone)
    print("登录模型流程：输出登录结果")
    if "Yes" in result:
        return 13
    else:
        return 12


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=11111,threaded=True)
