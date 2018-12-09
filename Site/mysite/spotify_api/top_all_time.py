import spotify_api.spotipy as spotipy
import spotify_api.spotipy.util as util


def artists(email, term):
    """ Get a user's top artists

        Parameters:
            - email - the user's email address
            - time_range - Over what time frame are the affinities computed
              Valid-values: short_term, medium_term, long_term
    """
    redirect_uri = 'http://localhost:8888/callback'
    client_id = 'd85350c3c35449d987db695a8e5a819b'
    client_secret = '516a6cd7008b4c3f8aa41d800a2415a0'
    scopes = 'user-read-currently-playing user-library-read user-read-recently-played user-read-playback-state'
    token = util.prompt_for_user_token(email, scope=scopes, client_id=client_id,
                                       client_secret=client_secret, redirect_uri=redirect_uri,
                                       cache_path=r'spotify_api/token_cache/')
    sp = spotipy.Spotify(auth=token)
    return sp.current_user_top_artists(time_range=term, limit=50)


def tracks(email, term):
    """ Get the current user's top artists

            Parameters:
                - email - the user's email address
                - time_range - Over what time frame are the affinities computed
                  Valid-values: short_term, medium_term, long_term
    """
    redirect_uri = 'http://localhost:8888/callback'
    client_id = 'd85350c3c35449d987db695a8e5a819b'
    client_secret = '516a6cd7008b4c3f8aa41d800a2415a0'
    scopes = 'user-read-currently-playing user-library-read user-read-recently-played user-read-playback-state'
    token = util.prompt_for_user_token(email, scope=scopes, client_id=client_id,
                                       client_secret=client_secret, redirect_uri=redirect_uri,
                                       cache_path=r'spotify_api/token_cache/')
    sp = spotipy.Spotify(auth=token)
    return sp.current_user_top_tracks(time_range=term, limit=50)


def get_all(email):
    """ Get the current user's top artists and top tracks for all time_ranges

            Parameters:
                - email - the user's email address
                - time_range - Over what time frame are the affinities computed
                  Valid-values: short_term, medium_term, long_term
    """
    context = {}
    for term in ['short_term', 'medium_term', 'long_term']:
        top_tracks = []
        for item in tracks(email, term=term)['items']:
            top_tracks.append(item['name'])
        context['top_tracks_{}'.format(term)] = top_tracks

        top_artists = []
        for item in artists(email, term=term)['items']:
            top_artists.append(item['name'])
        context['top_artists_{}'.format(term)] = top_artists
    return context


if __name__=='__main__':
    print('In top_all_time.py')

