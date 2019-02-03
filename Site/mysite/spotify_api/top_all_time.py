import spotify_api.spotipy as spotipy


def artists(email, token, term):
    """ Get a user's top artists

        Parameters:
            - email - the user's email address
            - time_range - Over what time frame are the affinities computed
              Valid-values: short_term, medium_term, long_term
    """
    sp = spotipy.Spotify(auth=token)
    return sp.current_user_top_artists(time_range=term, limit=50)


def tracks(email, token, term):
    """ Get the current user's top artists

            Parameters:
                - email - the user's email address
                - time_range - Over what time frame are the affinities computed
                  Valid-values: short_term, medium_term, long_term
    """
    sp = spotipy.Spotify(auth=token)
    return sp.current_user_top_tracks(time_range=term, limit=50)


def get_all(email, token):
    """ Get the current user's top artists and top tracks for all time_ranges

            Parameters:
                - email - the user's email address
                - time_range - Over what time frame are the affinities computed
                  Valid-values: short_term, medium_term, long_term
    """
    context = {}
    for term in ['short_term', 'medium_term', 'long_term']:
        top_tracks = []
        for item in tracks(email, token, term=term)['items']:
            top_tracks.append(item['name'])
        context['top_tracks_{}'.format(term)] = top_tracks

        top_artists = []
        for item in artists(email, token, term=term)['items']:
            top_artists.append(item['name'])
        context['top_artists_{}'.format(term)] = top_artists
    return context


if __name__=='__main__':
    print('In top_all_time.py')

