from flask import Flask, request
from flask_cors import CORS
from Crypto.Cipher import AES
from Crypto import Random
import random
import string
import base64
import rsa


def pad(txt: str):
    return txt.encode('utf-8') + b'\0' * (AES.block_size - len(txt) % AES.block_size)


app = Flask(__name__)
CORS(app)


@app.route('/login', methods=['POST'])
def login():
    with open("./database/users.txt") as f:
        for line in f.readlines():
            split = line.strip().split(':')
            if request.json["username"] == split[0] and request.json["password"] == split[1]:
                f.close()
                sid = ''
                for i in range(0, 8):
                    sid += random.choice(string.ascii_uppercase)

                return {'data': 'success', 'sid': sid}
        f.close()
    return {"data": "fail"}


@app.route('/invite', methods=['POST'])
def invite():
    with open('./database/users.txt', 'a') as f:
        # password = 'pass'
        f.write(
            f"\n{request.json['name']}:1a1dc91c907325c69271ddf0c944bc72:0:0:x")
        f.close()
    return {'result': 'success'}


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

forumPostData = {'data':[
            {
                'user': "Jason",
                'date': "2023.10.5",
                'title': "I love my wife",
                'post': 'dfjsljfjgdl hjgsdgtrnemu rhdsfijgof djhdgsofjsf eohfrhigh oudhorgpse',
                'id': "0"
            },
            {
                'user': "Blabla",
                'date': "2010.02.28",
                'title': "I wish i had a dog",
                'post': 'rhtroéudsh rfgoiehsukihfgr sdihgouhos jugoérjlithgk ngfldghf ohgdoduh dfjsljfjgdl ',
                'id': "1"
            },
            {
                'user': "Stanley",
                'date': "2001.01.01",
                'title': "Happy new year!",
                'post': 'hjgsdgtrnemu rhdsfijgof djhdgsofjsf eohfrhigh oudhorgpse rhtroéudsh rfgoiehsukihfgr sdihgouhos ',
                'id': "2"
            },
            {
                'user': "Elmo",
                'date': "2001.09.11",
                'title': "How tf does elmo fly a plane?",
                'post': 'oudhorgpse rhtroéudsh rfgoiehsukihfgr sdihgouhos jugoérjlithgk ngfldghf ohgdoduh dfjsljfjgdl hjgsdgtrnemu rhdsfijgof djhdgsofjsf eohfrhigh oudhorgpse rhtroéudsh rfgoiehsukihfgr sdihgouhos jugoérjlithgk ngfldghf ohgdoduh',
                'id': "3"
            }
        ]}

@app.route('/postContents', methods=['POST'])
def forumEndpoint():
    try:
        res = None
        for item in forumPostData['data']:
            if int(item['id']) == int(request.json['id']):
                res = item['post']
                break
        return {'data': res}
    except:
        return {'data': 'error'}

@app.route('/getPosts', methods=['GET'])
def postsEndpoint():
    return forumPostData

@app.route('/post', methods=['POST'])
def postEndpoint():
    try:
        dict = request.json
        dict['id'] = len(forumPostData['data'])
        forumPostData['data'].append(dict)
        return {'data': "success"}
    except:
        return {'data': 'error'}

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
