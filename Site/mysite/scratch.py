import sqlite3

dj = sqlite3.connect('db.sqlite3')
c = dj.cursor()
c.execute("""UPDATE spytify_play 
                                SET
                                time_stamp = 'Saturday 1/24/2019 18:14'
                                WHERE play_id = '45601'""")

dj.commit()
dj.close()

