# To make this script work, first open up node.js command prompt and cd to:
#     C:\Users\Martin\Google Drive\Python\Spotify\njtest
# then call:
#     node server.js
# then run this script

import spotipy
import spotipy.util as util
import datetime
import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import calendar

import sqlite3

def get_sheet(sheet_name):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    new_sheet = client.open("Spotify_Tracking").worksheet(sheet_name)
    return new_sheet


def add_to_sheet(user_id, sp, currently_playing, unique_songs, unique_artists, unique_albums):
    track_name = currently_playing['item']['name']
    artist = currently_playing['item']['artists'][0]['name']
    artist_id = currently_playing['item']['artists'][0]['id']
    album_id = currently_playing['item']['album']['id']
    now = datetime.datetime.now()
    sheet = get_sheet('All_Plays')
    date = '{}/{}/{}'.format(str(now.month), str(now.day), str(now.year))
    minute = str(now.minute)
    if int(minute) < 10:
        minute = '0' + minute
    time_of_day = '{}:{}'.format(str(now.hour), minute)
    device = currently_playing['device']['name']
    duration = currently_playing['item']['duration_ms']/1000
    id = currently_playing['item']['id']
    day_of_week = calendar.day_name[now.weekday()]
    sheet.insert_row([day_of_week, date, time_of_day, artist, track_name, device, duration, id, user_id], 2)

    timestamp = '{} {} {}'.format(day_of_week, date, time_of_day)
    c.execute("INSERT INTO plays VALUES (?,?,?,?)", (timestamp, user_id, id, device)) # Time, User, Song ID, Device
    conn.commit()

    add_song_to_database(sp, id, unique_songs, artist_id, album_id)
    add_artist_to_database(sp, artist_id, unique_artists)
    add_album_to_database(sp, album_id, unique_albums)


def add_song_to_database(sp, id, unique_songs, artist_id, album_id):
    if not unique_songs:
        unique_songs = get_sheet('Unique_Songs')
        records = unique_songs.get_all_records()
    if not id_in_database(id, records):
        f = sp.audio_features(id)[0]
        t = sp.track(id)
        if not f:
            f={}
            f['danceability']=''
            f['energy']=''
            f['key']=''
            f['loudness']=''
            f['mode']=''
            f['speechiness']=''
            f['acousticness']=''
            f['instrumentalness']=''
            f['liveness']=''
            f['valence']=''
            f['tempo']=''
            f['type']=''
            f['duration_ms']=''
            f['time_signature']=''
        unique_songs.insert_row([id, f['danceability'], f['energy'], f['key'], f['loudness'], f['mode'], f['speechiness'],
                           f['acousticness'], f['instrumentalness'], f['liveness'], f['valence'], f['tempo'], f['type'],
                           f['duration_ms'], f['time_signature'], artist_id, album_id, t['name'], t['popularity']], 2)
        c.execute("INSERT INTO songs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
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

def add_artist_to_database(sp, id, unique_artists):
    if not unique_artists:
        unique_artists = get_sheet('Unique_Artists')
        records = unique_artists.get_all_records()
    if not id_in_database(id, records):
        f = sp.artist(id)
        genres = ''
        for genre in f['genres']:
            genres += genre + ', '
        unique_artists.insert_row([id, f['name'], genres[:-2], f['followers']['total'], f['popularity']], 2)
        c.execute("INSERT INTO artists VALUES (?,?,?,?,?)",
                  (id,
                   f['name'],
                   genres[:-2],
                   f['followers']['total'],
                   f['popularity']))
        conn.commit()


def add_album_to_database(sp, id, unique_album):
    if not unique_album:
        unique_album = get_sheet('Unique_Albums')
        records = unique_album.get_all_records()
    if not id_in_database(id, records):
        f = sp.album(id)
        genres = ''
        for genre in f['genres']:
            genres += genre + ', '
        unique_album.insert_row([id, f['name'], f['artists'][0]['id'], f['label'], f['popularity'],
                                 f['album_type'], f['release_date'], genres[:-2], f['uri']], 2)
        c.execute("INSERT INTO albums VALUES (?,?,?,?,?,?,?)",
                  (id,
                   f['name'],
                   f['artists'][0]['id'],
                   f['label'],
                   f['popularity'],
                   f['album_type'],
                   f['release_date'],
                   ))
        conn.commit()

def id_in_database(id, database):
    for item in database:
        if item['ID'] == id:
            return item
    return None

def mprint(text):
    print(text)
    with open('Error_log.txt','a') as f:
        f.write(str(text))
        f.write('\n')

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
            # try:
            token = util.prompt_for_user_token(self.email, scope=scopes, client_id=client_id,
                                               client_secret=client_secret, redirect_uri=redirect_uri)
            sp = spotipy.Spotify(auth=token)
            currently_playing = sp.current_playback()
            if currently_playing and currently_playing['is_playing']:
                seconds_remaining = (currently_playing['item']['duration_ms'] - currently_playing['progress_ms']) / 1000
                add_to_sheet(self.id, sp, currently_playing, unique_songs, unique_artists, unique_albums)
                self.next_ping = time.time() + seconds_remaining + 1
                mprint('{}, {}: {}'.format(self.last, self.first, self.email))
                mprint('    {} - {}'.format(currently_playing['item']['name'], currently_playing['item']['artists'][0]['name']))
                mprint('    Next ping at {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + seconds_remaining))))
                mprint('')
            else:
                self.next_ping = time.time() + 60
                mprint('{}, {}: {}'.format(self.last, self.first, self.email))
                mprint('    Not Currently Playing, Waiting 60 Seconds To Try again.')
                mprint('    Next ping at {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 60))))
                mprint('')
            # except Exception as e:
            #     mprint('Ping ERROR:')
            #     mprint(e.args[0])
            #     main()
            
def main():
    while True:
        users.sort(key=lambda x: x.next_ping)
        user = users[0]
        sleep_time = user.next_ping - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        user.ping()

if __name__ == '__main__':
    unique_songs = None
    unique_artists = None
    unique_albums = None

    conn = sqlite3.connect('spotify_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    user_list = c.fetchall()
    users = []
    for user in user_list:
        users.append(User(user))
    
    while True:
        try:
            main()
        except Exception as e:
            time.sleep(10)
            mprint('Main Except:' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            mprint('  ' + str(e))
            main()
        

    conn.close()