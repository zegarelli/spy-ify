import sqlite3
import datetime
import time

import spotipy
import spotipy.util as util

if __name__ == '__main__':
    # first = input("What is the user's first name?")
    # last = input("What is the user's last name?")
    # email = input("What is the user's Spotify Email address?")
    # DOB = input("What is the user's Date of Birth? DD/MM/YYYY")
    first = 'jackson'
    last = 'braatz'
    email = 'xbraatz@yahoo.com'
    DOB = '26/06/1995'
    DOB = time.mktime(datetime.datetime.strptime(DOB, "%d/%m/%Y").timetuple())
    conn = sqlite3.connect('spotify_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY id DESC")
    user_list = c.fetchone()
    new_id = user_list[4] + 1

    c.execute("INSERT INTO users VALUES (?,?,?,?,?)",
              (first,
               last,
               email,
               DOB,
               new_id))
    conn.commit()
    conn.close()

    client_id = 'd85350c3c35449d987db695a8e5a819b'
    client_secret = '516a6cd7008b4c3f8aa41d800a2415a0'
    redirect_uri = 'http://localhost:8888/callback'
    scopes = 'user-read-currently-playing user-library-read user-read-recently-played user-read-playback-state'
    token = util.prompt_for_user_token(email, scope=scopes, client_id=client_id,
                                       client_secret=client_secret, redirect_uri=redirect_uri)
    sp = spotipy.Spotify(auth=token)
    currently_playing = sp.current_playback()
    print(currently_playing)