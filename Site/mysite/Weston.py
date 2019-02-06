import spotify_api.spotipy
import time

redirect_uri = 'http://192.168.1.132/home.html'
client_id = 'd85350c3c35449d987db695a8e5a819b'
client_secret = '516a6cd7008b4c3f8aa41d800a2415a0'
# scopes = 'user-read-currently-playing user-library-read user-read-recently-played user-read-playback-state user-modify-playback-state'
scopes = 'user-read-currently-playing user-read-recently-played user-read-playback-state user-modify-playback-state'

token = spotify_api.spotipy.util.prompt_for_user_token('prepxc@gmail.com', scope=scopes, client_id=client_id,
                                               client_secret=client_secret, redirect_uri=redirect_uri)
sp = spotify_api.spotipy.Spotify(auth=token)

# token2 = util.prompt_for_user_token('westonw94@gmail.com', scope=scopes, client_id=client_id,
                                               # client_secret=client_secret, redirect_uri=redirect_uri)
# sp2 = spotipy.Spotify(auth=token2)

track = 'spotify:track:2SIgTrGrUzm9k5oOElXRJY'
# print(sp2.devices())
# t1 = sp.start_playback(uris=[track])
# t = sp2.start_playback(device_id='83b65776bfdac8e14834d291fa9b6471039cc92a', uris=[track])


sp_prog = sp.current_playback()['progress_ms']
# sp2_prog = sp2.current_playback()['progress_ms']

# time.sleep(3)
#
# sp.seek_track(sp2_prog)
# sp2.seek_track(sp_prog)
# print(sp_prog)
# print(sp2_prog)



