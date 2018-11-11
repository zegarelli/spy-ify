import spotipy
import spotipy.util as util
import spotipy.oauth2

import sqlite3
import time

class User:
    def __init__(self, data):
        self.first = data[0]
        self.last = data[1]
        self.email = data[2]
        self.DOB = data[3]
        self.id = data[4]
        self.next_ping = 0

    def ping(self):
        if self.next_ping < time.time():
            redirect_uri = 'http://localhost:8888/callback'
            client_id = 'd85350c3c35449d987db695a8e5a819b'
            client_secret = '516a6cd7008b4c3f8aa41d800a2415a0'
            scopes = 'user-read-currently-playing user-library-read user-read-recently-played user-read-playback-state'
            token = util.prompt_for_user_token(self.email, scope=scopes, client_id=client_id,
                                               client_secret=client_secret, redirect_uri=redirect_uri)
            sp = spotipy.Spotify(auth=token)
            currently_playing = sp.currently_playing()
            if currently_playing and currently_playing['is_playing']:
                seconds_remaining = (currently_playing['item']['duration_ms'] - currently_playing['progress_ms']) / 1000
                self.next_ping = time.time() + seconds_remaining + 1
                print('{}, {}: {}'.format(self.last, self.first, self.email))
                print('    {} - {}'.format(currently_playing['item']['name'], currently_playing['item']['artists'][0]['name']))
                print('    Next ping at {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + seconds_remaining))))
                print()
            else:
                self.next_ping = time.time() + 60
                print('{}, {}: {}'.format(self.last, self.first, self.email))
                print('    Not Currently Playing, Waiting 60 Seconds To Try again.')
                print('    Next ping at {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 60))))
                print()





if __name__ == '__main__':
    conn = sqlite3.connect('spotify_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    user_list = c.fetchall()
    users = []
    for user in user_list:
        users.append(User(user))
    conn.close()

    while True:
        users.sort(key=lambda x: x.next_ping)
        user = users[0]
        sleep_time = user.next_ping - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        user.ping()
