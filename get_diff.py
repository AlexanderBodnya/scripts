import sqlite3
import os

def init_db(cur):
    cur.execute(
        'CREATE TABLE IF NOT EXISTS Users (user_id INTEGER, treat TEXT, treat_rus TEXT, first_name TEXT, last_name TEXT, lang TEXT, first_name_rus TEXT, middle_name_rus TEXT, last_name_rus TEXT, guid TEXT, photo TEXT)')

    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS `IX_guid` ON `Users` ( `guid` )")


path1 = 'C:\\Users\\a.bodnya\\.PyCharmCE2018.1\\config\\scratches\\whole_db.db'
path2 = 'C:\\Users\\a.bodnya\\Desktop\\unloaded\\final_base.db'
path3 = 'C:\\Users\\a.bodnya\\Desktop\\unloaded\\diff.db'
db1 = sqlite3.connect(path1)
db2 = sqlite3.connect(path2)
db3 = sqlite3.connect(path3)
cur1 = db1.cursor()
cur2 = db2.cursor()
cur3 = db3.cursor()
init_db(cur3)


cur1.execute('SELECT guid from Users')
guids_all = cur1.fetchall()

print(guids_all)




