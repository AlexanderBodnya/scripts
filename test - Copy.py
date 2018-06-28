import datetime
import json
import sqlite3
from base64 import b64encode, b64decode
from collections import Counter
import requests

def get_user(user_id):
    url = "https://sberphoto.acs.sisnw.ru/sber_photo/main"
    userpass = b64encode(b"expo_acs:xTriYS2v").decode("ascii")
    headers = {'content-type': 'application/json',
               'Authorization': 'Basic %s' % userpass
               }
    payload = {
        "method": "getUser",
        "params": {"id": user_id},
        "jsonrpc": "2.0",
        "id": 1,
    }

    data = json.dumps(payload)
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    print(data)
    return response

def get_photos(guid):
    url = "https://sberphoto.acs.sisnw.ru/sber_photo/main"

    userpass = b64encode(b"expo_acs:xTriYS2v").decode("ascii")
    headers = {'content-type': 'application/json',
               'Authorization': 'Basic %s' % userpass
               }
    payload = {
        "method": "getPhotos",
        "params": {"guids": guid},
        "jsonrpc": "2.0",
        "id": 1,
    }
    print(json.dumps(payload))
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    print(response['result'])
    with open("test.jpg", 'wb') as f:
        f.write(b64decode(response['result'][guid[0]]))
    return response

def request_persons():
    url = "https://sberphoto.acs.sisnw.ru/sber_photo/main"
    now = datetime.datetime.now() - datetime.timedelta(minutes=5)
    to_date = '{}.{}.{} {}:{}:{}'.format(now.day, now.month, now.year, now.hour, now.minute, now.second)
    userpass = b64encode(b"expo_acs:xTriYS2v").decode("ascii")
    headers = {'content-type': 'application/json',
               'Authorization': 'Basic %s' % userpass
               }
    payload = {
        "method": "getUsers",
        "params": {"updDateFrom": "23.01.2017 09:30:00", "updDateTo": to_date},
        "jsonrpc": "2.0",
        "id": 1,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    # print(json.dumps(response))
    return response

data = request_persons()['result']
mem=0
smi=0
teh=0
guids = []
for person in data:
    if person['OBJ_TYPE_CODE'] == 'members':
        mem+=1
    if person['OBJ_TYPE_CODE'] == 'smi':
        smi += 1
    if person['OBJ_TYPE_CODE'] == 'teh_per':
        teh += 1
    guids.append(person['PHOTO'])


print('SMI - {}, MEMBERS - {}, TECH - {}'.format(smi,mem,teh))

print(get_user('1493948'))

get_photos(['1BC3C9ABB145443D98429D289B550B47'] )