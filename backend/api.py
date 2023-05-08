from flask import Flask, render_template, request, url_for, redirect
from flask_cors import CORS
from Crypto.Cipher import AES
from Crypto import Random
import random
import string
import base64
import rsa

import os
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.sql import text, insert, table


def pad(txt: str):
    return txt.encode('utf-8') + b'\0' * (AES.block_size - len(txt) % AES.block_size)

#adminPass = "b454e3f209198b6c2c9d6ce0e2838ea2%A"


app = Flask(__name__)

engine = create_engine('mysql+mysqldb://admin:b454e3f209198b6c2c9d6ce0e2838ea2%A@192.168.0.200:3306/HomeProject')


CORS(app)

# THESE SHOULD BE HANDLED BY A DB


@app.route('/login', methods=['POST']) #yess
def login():
    with engine.connect() as conn:
        q= text("SELECT hashedPass,token FROM users WHERE username = '" + request.json["username"] +"'")
        rs = conn.execute(q).fetchone()
        if rs != None and request.json["password"] == rs.hashedPass:
            return {'data': 'success', 'token': rs.token}
        
    return {"data": "fail"}


@app.route('/adminLogin', methods=['GET','POST']) #yess
def adminLogin():
    if request.method == 'GET':
        return render_template('AdminLogin.html')
    else:
        with engine.connect() as conn:
            q= text("SELECT hashedPass,token, isAdmin FROM users WHERE username = '" + request.json["username"] +"'")
            rs = conn.execute(q).fetchone()
            if rs != None and rs.isAdmin and request.json["password"] == rs.hashedPass:
                return {'data': 'success', 'token': rs.token}
            
        return {"data": "fail"}


@app.route('/checkToken', methods=['POST']) #yess
def checkToken():
    with engine.connect() as conn:
        q= text("SELECT * FROM users WHERE username = '" + request.json["username"] +"'")
        rs = conn.execute(q).fetchone()
        if  request.json["token"] == rs.token:
            return {'data': 'success'}
        
    return {"data": "fail"}


def newSID(line, newLine): #I need to call this every midnight
    with engine.connect() as conn:
        q= text("SELECT * FROM users ")
        rs = conn.execute(q)
        for row in rs:
            newToken = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))
            q= text("UPDATE users SET token = '" + newToken +"' WHERE username = '" + row.username +"'")
            conn.execute(q)
            conn.commit()

@app.route('/postContents', methods=['POST']) #yessss
def forumEndpoint():
    with engine.connect() as conn:
        q= text("SELECT contents FROM posts WHERE postId = '"+ str(request.json['id'])+"'")
        rs = conn.execute(q).fetchone()
        return {'data': rs.contents}


@app.route('/getPosts', methods=['POST']) #yess
def postsEndpoint():
    with engine.connect() as conn:
        q= text("SELECT * FROM users WHERE token = '" + request.json["token"] +"'")
        rs = conn.execute(q).fetchone()
        if  request.json["token"] != rs.token:
            return {'data': 'fail'}
        
    with engine.connect() as conn:
        q= text("SELECT * FROM posts ORDER BY postDate DESC")
        rs = conn.execute(q)
        forumPostData = []
        for row in rs:
            
            forumPostData.append({
                'id': row.postId,
                'user': row.username,
                'date': row.postDate.strftime('%Y/%b/%d'),
                'title': row.title,
                'post': row.contents
            })

        return forumPostData    


@app.route('/getPostsOfUser', methods=['POST']) #yess
def postsOfUser():
    with engine.connect() as conn:
        q= text("SELECT * FROM posts WHERE username = '" + request.json["user"] +"' ORDER BY postDate DESC")
        rs = conn.execute(q)
        forumPostData = []
        for row in rs:
            forumPostData.append({
                'id': row.postId,
                'user': row.username,
                'date': row.postDate.strftime('%Y/%b/%d'),
                'title': row.title,
                'post': row.contents
            })

        return forumPostData    


@app.route('/post', methods=['POST']) #yess
def postEndpoint():
    with engine.connect() as conn:
        q= text("INSERT INTO posts(username, postDate, title, contents) VALUES('"+ request.json['username'] + "', '"+ request.json['postDate'] + "', '" + request.json['title'] + "', '" + request.json['contents'] + "'); ")
        conn.execute(q)
        conn.commit()
    return {'data': "success"}

@app.route('/invite', methods=['POST']) #yess
def invite():
    with engine.connect() as conn:
        newToken = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))
        q= text("INSERT INTO users(username, hashedPass, isAdmin, token) VALUES('"+ request.json['name'] + "', '1a1dc91c907325c69271ddf0c944bc72', false, '"+ newToken +"'); ")
        conn.execute(q)
        conn.commit()
    return {'data': "success"}


@app.route('/changepassword', methods=['POST'])
def changepassword():
    success = False
    with open('./database/users.txt', 'r') as f:
        lines = f.readlines()
        f.close()
    with open('./database/users.txt', 'w') as f:
        for line in lines:
            if request.json['name'] not in line:
                f.write(line)
            else:
                split = line.strip().split(':')
                if request.json['old_pass'] == split[1]:
                    f.write(
                        f"{request.json['name']}:{request.json['new_pass']}:{split[2]}:{split[3]}:{split[4]}")
                    success = True
                else:
                    f.write(line)

        f.close()
    if success:
        return {'result': 'success'}
    else:
        return {'result': 'fail'}


@app.route('/delete', methods=['POST'])
def delete():
    with open('./database/users.txt', 'r') as f:
        lines = f.readlines()
        f.close()
    with open('./database/users.txt', 'w') as f:
        for line in lines:
            if request.json['name'] not in line:
                f.write(line)
        f.close()
    return {'result': 'success'}


@app.route('/approve', methods=['POST'])
def approve():
    with open('./database/users.txt', 'r') as f:
        lines = f.readlines()
        f.close()
    with open('./database/users.txt', 'w') as f:
        for line in lines:
            if request.json['name'] not in line:
                f.write(line)
            else:
                split = line.strip().split(':')
                f.write(f"{split[0]}:{split[1]}:1:{split[3]}:{split[4]}")
        f.close()
    return {'result': 'success'}


@app.route('/promote', methods=['POST'])
def promote():
    with open('./database/users.txt', 'r') as f:
        lines = f.readlines()
        f.close()
    with open('./database/users.txt', 'w') as f:
        for line in lines:
            if request.json['name'] not in line:
                f.write(line)
            else:
                split = line.strip().split(':')
                f.write(f"{split[0]}:{split[1]}:{split[2]}:1:{split[4]}")
        f.close()
    return {'result': 'success'}


@app.route('/aes', methods=['POST'])
def aes_endpoint():
    if request.json['type'] == 'enc':
        try:
            iv = Random.new().read(AES.block_size)
            cypher = AES.new(pad(request.json['key']), AES.MODE_EAX, iv)
            encryption = iv + cypher.encrypt(pad(request.json['text']))
            return {'data': base64.b64encode(encryption).decode('utf-8')}
        except:
            return {'data': 'error'}
    elif request.json['type'] == 'dec':
        try:
            txt = base64.b64decode(request.json['text'])
            iv = txt[:AES.block_size]
            cypher = AES.new(pad(request.json['key']), AES.MODE_EAX, iv)
            return {'data': cypher.decrypt(txt[AES.block_size:]).rstrip(b'\0').decode('utf-8')}
        except:
            return {'data': 'error'}
    else:
        return {'data': 'bad type'}




@app.route('/rsa', methods=['GET', 'POST'])
def rsa_endpoint():
    if request.method == 'GET':
        pub_key, priv_key = rsa.newkeys(1024)
        return {'data': {
            'public_key': pub_key.save_pkcs1("PEM").decode('utf-8'),
            'private_key': priv_key.save_pkcs1("PEM").decode('utf-8')
        }}
    else:
        if request.json['type'] == 'enc':
            text: str = request.json['text']
            text = text.encode('utf-8')

            key: str = request.json['key']
            key = rsa.PublicKey.load_pkcs1(key.encode('utf-8'))

            cypher = base64.b64encode(rsa.encrypt(text, key)).decode('utf-8')
            return {'data': cypher}
        elif request.json['type'] == 'dec':
            text: str = request.json['text']
            text = base64.b64decode(text.encode('utf-8'))

            key: str = request.json['key']
            key = rsa.PrivateKey.load_pkcs1(key.encode('utf-8'))

            cypher = rsa.decrypt(text, key).decode('utf-8')
            return {'data': cypher}
        else:
            return {'data': 'bad type'}

app.run()
