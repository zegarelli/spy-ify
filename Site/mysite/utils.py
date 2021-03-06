from spotify_api import top_all_time
import sqlite3
import time

import spotify_api.spotipy.oauth2 as oauth2

def _is_token_expired(token):
    """
    Function to check if the spotify token will be expired in the next minute

    :param token: <dict> that contains the 'expired_at' key.
    :return:
    """
    now = int(time.time())
    return token['expires_at'] - now < 60


def update_token_db(user, token):
    """
    Function to update the user's token info in the database

    :param user:
    :param token:
    :return: None
    """
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    data = token
    c.execute("""UPDATE spytify_usertoken 
                    SET
                    access_token = ? , token_type = ? , expires_in = ? , scope = ? , expires_at = ? , refresh_token = ?
                    WHERE user_id = ?""",
              (data['access_token'], data['token_type'], data['expires_in'], data['scope'],
               data['expires_at'], data['refresh_token'], user.pk))
    conn.commit()
    conn.close()


def get_top_all_time(user, token):
    """
    A function to get a user's top all time plays, and artists.

    :param user:
    :param token:
    :return: <dict> of user's top tracks and top artists
    """
    if _is_token_expired(token):
        redirect_uri = 'http://spyify.duckdns.org/spytify'
        client_id = 'd85350c3c35449d987db695a8e5a819b'
        client_secret = '516a6cd7008b4c3f8aa41d800a2415a0'
        scopes = 'user-read-currently-playing user-library-read user-read-recently-played user-read-playback-state'
        oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scopes)
        token = oauth.refresh_access_token(token['refresh_token'])
        update_token_db(user, token)
    return top_all_time.get_all(user.email, token['access_token'])

def substr_in_list_of_strs(sub_string, strings):
    for n, item in enumerate(strings):
        if sub_string in item:
            return n, True
    return False, False