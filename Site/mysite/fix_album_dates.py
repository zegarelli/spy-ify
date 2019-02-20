import sqlite3

dj = sqlite3.connect('db.sqlite3')
c = dj.cursor()

# albums = c.execute("""SELECT * FROM spytify_album WHERE album_id = '4k1GJg2poyo6hwWLqJn9C2'""").fetchall()
albums = c.execute("""SELECT album_id, release_date FROM spytify_album""").fetchall()
count = 0
for n, album in enumerate(albums):
    if len(str(album[1])) == 4:
        date = str(album[1]) + '-01-01'

        c.execute("""UPDATE spytify_album 
                                SET
                                release_date = ?
                                WHERE album_id = ?""",
                  (date, album[0]))
        count += 1
    elif len(str(album[1])) == 7:
        date = str(album[1]) + '-01'

        c.execute("""UPDATE spytify_album 
                                SET
                                release_date = ?
                                WHERE album_id = ?""",
                  (date, album[0]))

        count += 1
    if n % 100 == 0:
        print(n, count)
print(count)
dj.commit()
dj.close()
