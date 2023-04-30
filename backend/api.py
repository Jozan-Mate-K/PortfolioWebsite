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

##THESE SHOULD BE HANDLED BY A DB
@app.route('/login', methods=['POST'])
def login():
    with open("./database/users.txt") as f:
        for line in f.readlines():
            split = line.strip().split(':')
            if request.json["username"] == split[0] and request.json["password"] == split[1]:
                f.close()
                return {'data': 'success', 'token': split[4] }
        
        f.close()

    return {"data": "fail"}

@app.route('/checkToken', methods=['POST'])
def checkToken():
    with open("./database/users.txt") as f:
        for line in f.readlines():
            split = line.strip().split(':')
            if request.json["username"] == split[0] and request.json["token"] == split[4]:
                f.close()
                return {'data': 'success'}
        
        f.close()

    return {"data": "fail"}

def newSID(line,newLine):
    #I need to re-create every sid at midnight
    split = line.strip().split(':')
    newLine = split[0]
    for i in range(1,len(split)):
        newLine += ":" + split[i]


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
                'post': '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',
                'id': "0"
            },
            {
                'user': "Blabla",
                'date': "2010.02.28",
                'title': "I wish i had a dog",
                'post': 'a3dcb4d229de6fde0db5686dee47145d',
                'id': "1"
            },
            {
                'user': "Stanley",
                'date': "2001.01.01",
                'title': "Happy new year!",
                'post': 'vIewoZJcb1UWL0nYszS9ms12Qg/oqs2K/tM03JLBoohtyFQ9t4GMDns6qFrKRTqthve26552dZcU7I/UTin0XT6wQnH16IseOO4JPGtPQh7/jXb+CI4Tt6t9SXTMO+4aldUskNZ+XYhulEW4pRiVzuO+r4x+TMUorXa8JaNO8EBlH3cHFT7s2+yq/GfL2lvbB6BYDAjbz4x4FDwIfINAlK7/fEl2ZYHg+8TMFoltNyfPGD8H5GkajFi3vTjlBYLrQaaWmsZYoHmTAn4YrBzBSvFzXeVyxkmftlCnXE6uKVVDz/QuLKaiTH8Valv/dsYFTXGE7COwE8BNynIryXwSxtC24BuEMri18xk4kIYH4H5t2jrRbVKE37WXXas41uZQwPKmJaBtvxdULG3I1/icc1HuOiyYDHnzAkomVVhjW5K+5f0ER7yB1AGbfmhOD2DmWGnFrxduhqLSxzC7taP7s01QlnzBx3PQmuJbnHIB+gRw/H0gbzhPhDB7HEhaMXTIZRCYnk96qpFmz/EILWQpKiGmbeKH4lflw5XYwpftXv+R8IWyjPgUVPOn4LgsFQVOunGQU+RlYsIV/EA1myAJBTdjY4yO/+5taMoG+SrQbA2kz4Iv3e8n2pqNiNEWKmX2MPOnGDLXRQ9f01YGaObHA+kiXG1HeZkCNo7eP7JpQBKwuXoIaMFCH3hf6nEZFcfe5rXVFuuDMp6PXmchl8U/kKs65hoy81Nfl4N+8LJrfKg=',
                'id': "2"
            },
            {
                'user': "Elmo",
                'date': "2001.09.11",
                'title': "How tf does elmo fly a plane?",
                'post': 'bIrzbt1Ue5JZhrtw7cK5pilTRyvkAIeYawPKHTnTl5EOF3AOopJUtjQutewN0SHEWSvHFeBFmz7TzQF8uWWyk2i8x9bwPhPLGq9rgMvJb8gOF4ZdRneJqFZK6AdMHpDPvGTb66a8zQAuAQBX+I7/M0BFIuLusoDbkrBAE9gBw0/i5xtKNNrxwzmKZ0YxFvDGLXSIWLmisJQ2/WcGU66/OM+HZgEU5VwOICDpYFOhD2QGB86IEQzf5kW7ywtZzxkA8skoSWAxr3ugUxC4383EVe47fsZXgSpz/Oj1Bk8U/dwu8iyBNC/0WlX/U0gj+V4Hq16Kpb+sCf6RzppQAkqdJFa0PII5Ljy8JR1LSJtVehhJ0v0aFoaOFL52H//f3TCOH6lTpXpsd+YcCN1CouBw6CdV2sWezrj7Acfgb1poKQSmZx0fKeGIkQWECzuzmT2cbvLdTXxMEO9X/EcIAPpCWBaakwyl5qf8KxR4zDUkHz6QwhceHtruR9sOzdbGqLov1vstjKQf6T7eOAGvN+Vfl/vfvSu3p+lmSf8m+XLgxkzjE3qs5L9zh7yiSUJmx0FXths97UOrB6sb2RgJYrLQGzyDBWkZUoFSCJY3kt0OUMjFKEpt0Xr4tmxArOTXVFcyYM4S+2QUfCzdshpbU94CtPav6fJV3xT3grql6P/IVSEtcSK32eBMVKuwkG1WtbwtYzb8V40oQZpLddXhUryMwfccB5KxAY8gE7ArLC0OYqxIu4IQuPvF9sxWPcQQzGIZAIEjyuiA7r7PKcfO8L80HouzgZMgr8ZS1gEk2LkJa2twLli2HxkHhEXGIpHNX+XGElkSh4jBwmrGCGe3/jE2dPmRM7SuJJG8qJP9S4PlitoWZIVUVJ0mmQxS7Gg8ZYq1iuWFRecC2+JHdNolulQwP0sNyjqAtcaGKA+VTrx4OpD5TxicC6GyZJBKN6cYKl2dAz4bUiaQy5wKdGY1GLSGsh19VQcgQll4SdPs7fX4X+9p+u5zngstERzNqdR7CXK46heZlUMAqtz0iHCv5MRBTI0BtOSTIQF5iuGNp7CAQBLsmASpG5GDix1UrBhHx8BdwZKQxtOd3Zw+Hhe3yoIU1jGEm3UbCv97IntIv9C4UdyqaxEnmrr7WnQSgghBd65Q6ihS+ZU5Mse4IOtZjro9ECj8CW4EAzsCPi1+OHJFD8kYhBwk6se2uOnLpXgXC5rC6hf9x0RMArkZYc40TYnGcL33K2lIH9PZJNGqnAvd3SHAGO97XOiNvOL8Bfk+ckbrl1szccbLuNLZgpS9s1eiLpmJTKuoRmG6cfYt60bK9SJ32pYgnPShBFzeJ/G/0v1T46YIxJfdoWsF34mOXfPRvDWtlprDpjEqDahRV8qK8bG6+hs4jKjdgS1GSNAC3nIH39cRD/Dyl4sMi8mSIrVlZ9tKGcJA+52ytm/zV0Rt+8JGZ5JsaDUz0idG1gAtuKe2uvSz3tua+kW0guRi19/bvbX/iiQCXXtghjk99wGiwMsJ92QE+okA1+Bbe2Gb9zWZlEwePHuxEPOzxRSISEQPrWJ/YYO+7RFFs85i+ZAlMjEA8yJJYVpsuSZbRmA5l7aLJKdt9eoAF7Pdbiy48wAAruIqfNtZVGwS9kAktfZ1r4eyOBSIqKKdCwpmu+0AV9MnYdB79qe6l5qCg4+HzE9q5La0ql7o4hqpKLYXnNx/jco8+ODGeYltFfcb7Neug2lII5xZ',
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

@app.route('/getPostsOfUser', methods=['POST'])
def postsOfUser():
    userPosts = {'data':[]}
    for i in forumPostData['data']:
        if i['user'] == request.json['user']:
            userPosts['data'].append(i) 
    return userPosts

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
