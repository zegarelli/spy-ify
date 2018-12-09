import sqlite3


dj = sqlite3.connect('db.sqlite3')
c = dj.cursor()


c.execute("""SELECT       song_id,
             COUNT(song_id) AS value_occurrence
    FROM     spytify_play
    WHERE user_id = 1
    GROUP BY song_id
    ORDER BY value_occurrence DESC
    LIMIT    60;""")

# c.execute("""SELECT * FROM 'spytify_play' WHERE user_id = 1""")

top_songs = c.fetchall()
for song, plays in top_songs:
    c.execute("SELECT song_name from 'spytify_song' WHERE song_id = '{}'".format(song))
    # print(song)
    try:
        print('{}: {}'.format(c.fetchone()[0], song[-1]))
    except:
        pass

dj.close()