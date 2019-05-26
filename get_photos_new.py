import json
import sqlite3
from base64 import b64encode, b64decode
import os

#os.path.exists(pathname)

if __name__ == "__main__":
    bases = os.listdir('C:\\Users\\a.bodnya\\.PyCharmCE2018.1\\config\\scratches\\')
    os.chdir('C:\\Users\\a.bodnya\\.PyCharmCE2018.1\\config\\scratches\\')
    for base in bases:
        database = os.path.abspath(base)
        print('Connecting to base {}'.format(database))

        db=[]
        try:
            db = sqlite3.connect(database)
        except:
            print("Failed to open DB")
        cur = db.cursor()
        cur.execute('SELECT * FROM Users')
        dir = 'C:\\Users\\a.bodnya\\Desktop\\temp_off\\'
        while True:
            item = cur.fetchone()
            if not item:
                print("Finish loop.")
                break
            try:
                lang = item[5][0:2]
            except TypeError:
                lang = 'En'
            if lang != 'En' and lang != 'Ru':
                lang = 'En'
            if lang == 'En':
                if item[1] == None:
                    who = ''
                else:
                    who = item[1]

                filename = '{}#_{}_{}_{}_{}_NNN{}NNN_.jpg'.format(dir, lang, who, item[3], item[4], item[0])

                with open(filename, 'wb') as f:
                    try:
                        f.write(b64decode(item[10]))
                    except:
                        print('Error! ' + str(item[9]))
                    f.close()
            elif lang == 'Ru':

                if item[7] == None:
                    replacement = ''
                else:
                    replacement = item[7]
                filename = '{}#_{}_{}_{}_{}_NNN{}NNN_.jpg'.format(dir,lang, item[2], item[6], replacement, item[0])

                with open(filename, 'wb') as f:
                    try:
                        f.write(b64decode(item[10]))
                    except:
                        print('Error! ' + str( item[9]))
                    f.close()