from spotify_api import top_all_time


def get_top_all_time(email, token):
    return top_all_time.get_all(email, token)

