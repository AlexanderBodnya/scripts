import datetime
import json
import sqlite3
from base64 import b64encode, b64decode

import requests


def request_persons():
    url = "https://sberphoto.acs.sisnw.ru/sber_photo/main"
    now = datetime.datetime.now() - datetime.timedelta(minutes=15)
    past_time = now - datetime.timedelta(hours=1)
    from_date = '{}.{}.{} {}:{}:{}'.format(past_time.day, past_time.month, past_time.year, past_time.hour, past_time.minute, past_time.second)
    to_date = '{}.{}.{} {}:{}:{}'.format(now.day, now.month, now.year, now.hour, now.minute, now.second)
    userpass = b64encode(b"expo_acs:xTriYS2v").decode("ascii")
    headers = {'content-type': 'application/json',
               'Authorization': 'Basic %s' % userpass
               }
    payload = {
        "method": "getUsers",
        "params": {"updDateFrom": from_date, "updDateTo": to_date},
        "jsonrpc": "2.0",
        "id": 1,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print(json.dumps(response))
    return response


def get_photos(guids):
    url = "https://sberphoto.acs.sisnw.ru/sber_photo/main"

    userpass = b64encode(b"expo_acs:xTriYS2v").decode("ascii")
    headers = {'content-type': 'application/json',
               'Authorization': 'Basic %s' % userpass
               }
    payload = {
        "method": "getPhotos",
        "params": {"guids": guids},
        "jsonrpc": "2.0",
        "id": 1,
    }
    print(json.dumps(payload))
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    return response




def init_db(cur):
    cur.execute(
        'CREATE TABLE IF NOT EXISTS Users (user_id INTEGER, treat TEXT, treat_rus TEXT, first_name TEXT, last_name TEXT, lang TEXT, first_name_rus TEXT, middle_name_rus TEXT, last_name_rus TEXT, guid TEXT, photo TEXT)')

    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS `IX_guid` ON `Users` ( `guid` )")



def safe_insert_user(cur, user_id, treat, first_name, last_name, lang, guid, treat_rus, first_name_rus,
                        middle_name_rus, last_name_rus):
    cur.execute('SELECT * FROM Users WHERE user_id=?', (user_id,))
    check = cur.fetchall()
    if check == []:
        cur.execute(
            'INSERT  INTO Users (user_id, treat, treat_rus, first_name, last_name, first_name_rus, middle_name_rus, last_name_rus, lang, guid) VALUES (?,?,?,?,?,?,?,?,?,?)',
            (user_id, treat, treat_rus, first_name, last_name, first_name_rus, middle_name_rus, last_name_rus, lang, guid,))
    else:
        print('User exists!')



if __name__ == "__main__":

    now = datetime.datetime.now()
    past_time = now - datetime.timedelta(minutes=60)
    from_date = '{}_{}_{}-{}_{}_{}'.format(past_time.day, past_time.month, past_time.year, past_time.hour,
                                           past_time.minute, past_time.second)
    to_date = '{}_{}_{}-{}_{}_{}'.format(now.day, now.month, now.year, now.hour, now.minute, now.second)
    database = 'C:\\Users\\a.bodnya\\.PyCharmCE2018.1\\config\\scratches\\test_diff.db'
    database2 = 'C:\\Users\\a.bodnya\\Desktop\\unloaded\\whole_db.db'
    db = sqlite3.connect(database)
    db2 = sqlite3.connect(database2)
    cur = db.cursor()
    cur2 = db2.cursor()
    init_db(cur)
    db.commit()
    # resp = request_persons()['result']
    # print(len(resp))
    # for item in resp:
    #     last_name = item['LN_ON_BADGE']
    #     first_name = item['FN_ON_BADGE']
    #     first_name_rus = item['FN_RUS']
    #     middle_name_rus = item['MN_RUS']
    #     last_name_rus = item['LN_RUS']
    #     guid = item['PHOTO']
    #     user_id = item['OBJ_ID']
    #     lang = item['LANG_CORRESPONDENCE_ENG']
    #     treat = item['TREATMENT_ENG']
    #     treat_rus = item['TREATMENT_RUS']
    #
    #     safe_insert_user(cur, user_id, treat, first_name, last_name, lang, guid, treat_rus, first_name_rus,
    #                             middle_name_rus, last_name_rus)
    #
    #     db.commit()
    #
    # cur.execute("SELECT guid FROM Users WHERE photo IS NULL ")
    guids = []
    list =[]
    with open('C:\\Users\\a.bodnya\\Desktop\\unloaded\\guids.csv', 'r') as f:
        guids = f.readlines()
    print(guids)
    for guid in guids:
        guid = guid.strip('\n')
        cur2.execute('SELECT * FROM Users WHERE guid=?', (guid,))
        data_to_insert = cur2.fetchone()
        print(data_to_insert)
        cur.execute('INSERT OR IGNORE INTO Users (user_id, treat, treat_rus, first_name, last_name, lang, first_name_rus, middle_name_rus, last_name_rus, guid, photo) VALUES (?,?,?,?,?,?,?,?,?,?,?)', data_to_insert)
    # while True:
    #     #
    #     # data2 = cur.fetchmany(size=100)
    #     # if not data2:
    #     #     break
    #     # guids = []
    #     # for guid in data2:
    #     #     guids.append(guid[0])
    #     print(list)
    #     result = get_photos(list)["result"]
    #     for guid in list:
    #         cur2.execute('UPDATE Users SET photo=? WHERE guid=?', (result[guid], guid))
    #     list = []
    #
    #
    cur.execute("UPDATE Users SET treat_rus=replace(treat_rus, '_Г-', '_г-') WHERE treat_rus LIKE '%\_Г-%'")
    db.commit()