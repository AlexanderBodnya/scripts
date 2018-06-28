import json
import sqlite3
from base64 import b64encode, b64decode
import os

#os.path.exists(pathname)

def save_photo(cur, guid):
    dir1 = 'test'
    dir2 = 'test2'
    cur.execute("SELECT * FROM Users WHERE guid=?",(guid))
    data = cur.fetchall()
    for item in data:
        print(item)
        try:
            lang = item[5][0:2]
        except TypeError:
            lang = 'En'

        if lang != 'En' and lang != 'Ru':
            lang = 'En'
        if lang == 'En':
            filename1 = '.\\{}\\#_{}_{}_{}_{}.jpg'.format(dir1,lang, item[1], item[3], item[4])
            filename2 = '.\\{}\\#_{}_{}_{}_{}.jpg'.format(dir2, lang, item[1], item[3], item[4])

            if os.path.exists(filename1):
                photo = ''
                with open( filename1, 'rb') as f1:
                    photo = b64encode( f1.read() )
                    f1.close()
                if photo == item[9]:
                    continue
                else:
                    with open(filename2, 'wb') as f2:
                        try:
                            f2.write(b64decode(item[9]))
                        except:
                            print('Error! ' + item[8])
                        f2.close()
            with open(filename1, 'wb') as f:
                try:
                    f.write(b64decode(item[9]))
                except:
                    print('Error! '+item[8])
                f.close()
        elif lang =='Ru':
            if os.path.exists(filename1):
                photo = ''
                with open( filename1, 'rb') as f1:
                    photo = b64encode( f1.read() )
                    f1.close()
                if photo == item[9]:
                    continue
                else:
                    with open(filename2, 'wb') as f2:
                        try:
                            f2.write(b64decode(item[9]))
                        except:
                            print('Error! ' + item[8])
                        f2.close()
            with open(filename1, 'wb') as f:
                try:
                    f.write(b64decode(item[9]))
                except:
                    print('Error! '+item[8])
                f.close()

if __name__ == "__main__":
    db = sqlite3.connect('C:\\Users\\a.bodnya\\.PyCharmCE2018.1\\config\\scratches\\test.csv')
    cur = db.cursor()
    cur.execute('SELECT * FROM Users')
    dir1 = 'test'
    dir2 = 'test2'
    while True:
        item = cur.fetchone()
        if not item:
            break
        try:
            lang = item[5][0:2]
        except TypeError:
            lang = 'En'
        if lang != 'En' and lang != 'Ru':
            lang = 'En'
        if lang == 'En':
            if lang == 'En':
                filename1 = '.\\{}\\#_{}_{}_{}_{}.jpg'.format(dir1, lang, item[1], item[3], item[4])
                filename2 = '.\\{}\\#_{}_{}_{}_{}.jpg'.format(dir2, lang, item[1], item[3], item[4])

                if os.path.exists(filename1):
                    photo = ''
                    with open(filename1, 'rb') as f1:
                        photo = b64encode(f1.read())
                        f1.close()
                    if photo == item[9]:
                        continue
                    else:
                        with open(filename2, 'wb') as f2:
                            try:
                                f2.write(b64decode(item[9]))
                            except:
                                print('Error! ' + item[8])
                            f2.close()
                with open(filename1, 'wb') as f:
                    try:
                        f.write(b64decode(item[9]))
                    except:
                        print('Error! ' + item[8])
                    f.close()
        elif lang == 'Ru':

            if item[7] == None:
                replacement = ''
            else:
                replacement = item[7]
            filename1 = '.\\{}\\#_{}_{}_{}_{}.jpg'.format(dir1,lang, item[2], item[6], replacement)
            filename2 = '.\\{}\\#_{}_{}_{}_{}.jpg'.format(dir2,lang, item[2], item[6], replacement)
            if os.path.exists(filename1):
                photo = ''
                with open(filename1, 'rb') as f1:
                    photo = b64encode(f1.read())
                    f1.close()
                if photo == item[9]:
                    continue
                else:
                    with open(filename2, 'wb') as f2:
                        try:
                            f2.write(b64decode(item[9]))
                        except:
                            print('Error! ' + item[8])
                        f2.close()
            with open(filename1, 'wb') as f:
                try:
                    f.write(b64decode(item[9]))
                except:
                    print('Error! ' + item[8])
                f.close()        # else:
        #     with open('.\\test\\#_{}_{}_{}_{}.jpg'.format(lang, item[0], item[3], item[4]), 'wb') as f:
        #         try:
        #             f.write(b64decode(item[9]))
        #         except:
        #             print('Error! ' + item[8])
        #             pass
        #         f.close()
