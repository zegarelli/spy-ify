import sqlite3


dj = sqlite3.connect('db.sqlite3')
c = dj.cursor()


c.execute("ALTER TABLE spytify_user RENAME TO spytify_userprofile")

dj.close()