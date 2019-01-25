import sqlite3
import datetime
import time
import calendar
import logging

import spotify_api.spotipy as spotipy
import spotify_api.spotipy.util as util
import spotify_api.spotipy.oauth2 as oauth2

logging.basicConfig(filename='watcher.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

def add_play_to_database(user_id, sp, currently_playing):
    artist_id = currently_playing['item']['artists'][0]['id']
    album_id = currently_playing['item']['album']['id']
    id = currently_playing['item']['id']
    device = currently_playing['device']['name']

    # format the timestamp
    now = datetime.datetime.now()
    date = '{}/{}/{}'.format(str(now.month), str(now.day), str(now.year))
    minute = str(now.minute)
    if int(minute) < 10:
        minute = '0' + minute
    time_of_day = '{}:{}'.format(str(now.hour), minute)
    day_of_week = calendar.day_name[now.weekday()]
    timestamp = '{} {} {}'.format(day_of_week, date, time_of_day)

    largest_id = c.execute("""SELECT MAX(play_id) from spytify_play""").fetchone()
    c.execute("""INSERT INTO spytify_play (play_id, time_stamp, user_id, song_id, device) VALUES (?,?,?,?,?)""",
              (largest_id[0] + 1, timestamp, user_id, id, device))
    conn.commit()

    add_song_to_database(sp, id, artist_id, album_id)
    add_artist_to_database(sp, artist_id)
    add_album_to_database(sp, album_id)


def add_song_to_database(sp, id, artist_id, album_id):
    if len(c.execute("SELECT * FROM spytify_song WHERE song_id=?", (id,)).fetchall()) == 0:
        f = sp.audio_features(id)[0]
        t = sp.track(id)
        if not f:
            f = {}
            f['danceability'] = ''
            f['energy'] = ''
            f['key'] = ''
            f['loudness'] = ''
            f['mode'] = ''
            f['speechiness'] = ''
            f['acousticness'] = ''
            f['instrumentalness'] = ''
            f['liveness'] = ''
            f['valence'] = ''
            f['tempo'] = ''
            f['type'] = ''
            f['duration_ms'] = ''
            f['time_signature'] = ''
        c.execute("""INSERT INTO spytify_song (song_id, artist_id_id, album_id_id, song_name, song_popularity,
                  danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness,
                  valence, tempo,type, duration_ms, time_signature) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (id,
                   artist_id,
                   album_id,
                   t['name'],
                   t['popularity'],
                   f['danceability'],
                   f['energy'],
                   f['key'],
                   f['loudness'],
                   f['mode'],
                   f['speechiness'],
                   f['acousticness'],
                   f['instrumentalness'],
                   f['liveness'],
                   f['valence'],
                   f['tempo'],
                   f['type'],
                   f['duration_ms'],
                   f['time_signature'],))
        conn.commit()


def add_artist_to_database(sp, id):
    if len(c.execute("SELECT * FROM spytify_artist WHERE artist_id=?", (id,)).fetchall()) == 0:
        f = sp.artist(id)
        genres = ''
        for genre in f['genres']:
            genres += genre + ', '
        c.execute("""INSERT INTO spytify_artist (artist_id,artist_name,genres,followers,artist_popularity) VALUES
                  (?,?,?,?,?)""",
                  (id,
                   f['name'],
                   genres[:-2],
                   f['followers']['total'],
                   f['popularity']))
        conn.commit()


def add_album_to_database(sp, id):
    if len(c.execute("SELECT * FROM spytify_album WHERE album_id=?", (id,)).fetchall()) == 0:
        f = sp.album(id)
        genres = ''
        for genre in f['genres']:
            genres += genre + ', '
        c.execute("""INSERT INTO spytify_album (album_id,album_name,artist_id_id,label,album_popularity,album_type,
        release_date) VALUES (?,?,?,?,?,?,?)""",
                  (id,
                   f['name'],
                   f['artists'][0]['id'],
                   f['label'],
                   f['popularity'],
                   f['album_type'],
                   f['release_date'],
                   ))
        conn.commit()


def mprint(text):
    print(text)
    with open('Error_log.txt', 'a') as f:
        f.write(str(text))
        f.write('\n')


class User:
    def __init__(self, data, tokens=None):
        self.first = data[5]
        self.last = data[10]
        self.email = data[6]
        self.id = data[0]
        self.next_ping = 0
        self.token = self.find_token(tokens)

    def ping(self):
        if self.next_ping < time.time():
            redirect_uri = 'http://spyify.duckdns.org/spytify'
            client_id = 'd85350c3c35449d987db695a8e5a819b'
            client_secret = '516a6cd7008b4c3f8aa41d800a2415a0'
            scopes = 'user-read-currently-playing user-library-read user-read-recently-played user-read-playback-state'

            if self._is_token_expired():
                oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scopes)
                self.token = oauth.refresh_access_token(self.token['refresh_token'])
                self.update_token_db()

            try:
                sp = spotipy.Spotify(auth=self.token['access_token'])

                currently_playing = sp.current_playback()
                if currently_playing and (currently_playing['is_playing'] and currently_playing['item']):
                    seconds_remaining = (currently_playing['item']['duration_ms'] - currently_playing['progress_ms']) / 1000
                    add_play_to_database(self.id, sp, currently_playing)
                    self.next_ping = time.time() + seconds_remaining + 10
                else:
                    self.next_ping = time.time() + 60

                mprint('{}, {}: {}'.format(self.last, self.first, self.email))
                mprint('    Next ping at {}'.format(
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + self.next_ping))))
            except Exception as e:
                logging.exception("Exception while making spotify object")
                self.next_ping = time.time() + 60

    def find_token(self, tokens):
        for token in tokens:
            if token['user_id'] == self.id:
                token_json = {}
                for key in token.keys():
                    token_json[key] = token[key]
                return token_json
        return None

    def _is_token_expired(self):
        now = int(time.time())
        return self.token['expires_at'] - now < 60

    def update_token_db(self):
        data = self.token

        c.execute("""UPDATE spytify_usertoken 
                        SET
                        access_token = ? , token_type = ? , expires_in = ? , scope = ? , expires_at = ? , refresh_token = ?
                        WHERE user_id = ?""",
                  (data['access_token'], data['token_type'], data['expires_in'], data['scope'],
                   data['expires_at'], data['refresh_token'], self.id))
        conn.commit()


def main(users_by_id, users):
    while True:
        # Check for new users
        user_list = c.execute("SELECT * FROM auth_user").fetchall()
        for user in user_list:
            if user[0] not in users_by_id:
                tokens = c.execute("SELECT * FROM spytify_usertoken").fetchall()
                new_user = User(user, tokens=tokens)
                if new_user.token:
                    users.append(new_user)
                    users_by_id[new_user.id] = new_user

        # Sort Users by who needs pinged next
        users.sort(key=lambda x: x.next_ping)
        user = users[0]
        sleep_time = user.next_ping - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        user.ping()


if __name__ == '__main__':
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    tokens = c.execute("SELECT * FROM spytify_usertoken").fetchall()
    user_list = c.execute("SELECT * FROM auth_user").fetchall()
    users = []
    users_by_id = {}

    for user in user_list:
        new_user = User(user, tokens=tokens)
        if new_user.token:
                users.append(new_user)
                users_by_id[new_user.id] = new_user

    while True:
        try:
            main(users_by_id, users)
        except Exception as e:
            logging.exception("Exception occurred in main")

    conn.close()
