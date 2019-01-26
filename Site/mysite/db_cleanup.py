import sqlite3


dj = sqlite3.connect('db.sqlite3')
c = dj.cursor()

users = c.execute("""SELECT id FROM auth_user""").fetchall()

for user in users:
    plays = c.execute("""SELECT       *
                    FROM     spytify_play
                    WHERE user_id = {}""".format(user[0])).fetchall()

    old_play = ''
    for play in plays:
        if play[3] == old_play:
            print('Deleting play ID#: {}'.format(play[0]))
            c.execute("""DELETE FROM spytify_play WHERE play_id = {}""".format(play[0]))
            dj.commit()
        old_play = play[3]

dj.close()