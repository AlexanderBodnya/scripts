import sqlite3
import os

path = 'C:\\Users\\a.bodnya\\Desktop\\unloaded'
os.chdir(path)
listing = os.listdir(path)
master_base = listing.pop(0)
db = sqlite3.connect(master_base)
cur = db.cursor()

for base in listing:
    print(base)
    cur.execute('BEGIN TRANSACTION')
    cur.execute('ATTACH "{}" AS to_merge'.format(base))
    cur.execute('INSERT OR IGNORE INTO Users SELECT * FROM to_merge.Users')
    cur.execute('END TRANSACTION')
    cur.execute('DETACH to_merge')

    db.commit()