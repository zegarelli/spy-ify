columns = {
    'play': {
        'play_id': 'play_id',
        'time_stamp': 'time_stamp',
        'user_id': 'user_id',
        'song_id': 'song_id',
        'device': 'device',
        'context': 'context',
        'context_type': 'context_type',
    },
    'song': {
        'song_id' : 'song__song_id',
        'artist_id': 'song__artist_id',
        'album_id': 'song__album_id',
        'song_name': 'song__song_name',
        'song_popularity': 'song__song_popularity',
        'danceability': 'song__danceability',
        'energy': 'song__energy',
        'key': 'song__key',
        'loudness': 'song__loudness',
        'mode': 'song__mode',
        'speechiness': 'song__speechiness',
        'acousticness': 'song__acousticness',
        'instrumentalness': 'song__instrumentalness',
        'liveness': 'song__liveness',
        'valence': 'song__valence',
        'tempo': 'song__tempo',
        'type': 'song__type',
        'duration_ms': 'song__duration_ms',
        'time_signature': 'song__time_signature',
    },
    'album': {
        'album_id': 'song__album_id',
        'album_name': 'song__album_id__album_name',
        'artist_id': 'song__album_id__artist_id',
        'label': 'song__album_id__label',
        'album_popularity': 'song__album_id__album_popularity',
        'album_type': 'song__album_id__album_type',
        'release_date': 'song__album_id__release_date',
    },
    'artist': {
        'artist_id': 'song__artist_id',
        'artist_name': 'song__artist_id__artist_name',
        'genres': 'song__artist_id__genres',
        'followers': 'song__artist_id__followers',
        'artist_popularity': 'song__artist_id__artist_popularity',
    },
}

operators = {
    'IS': '__exact',
    '=': '__iexact',
    '>': '__gt',
    '>=': 'gte',
    '<': '__lt',
    '<=': 'lte',
    'CONTAINS': '__icontains',
    'IN': '__in',
    'STARTSWITH': '__istartswith',
    'ENDSWITH': '__iendswith',
}


def list_columns():
    l = []
    for table in columns:
        for column in columns[table]:
            l.append('{}.{}'.format(table, column))
    return sorted(l)


def list_operators():
    l = []
    for operator in operators:
        l.append(operator)
    return sorted(l)


def play_to_dict(play):
    play = {
        'play': play.__dict__,
        'song': play.song.__dict__,
        'artist': play.song.artist_id.__dict__,
        'album': play.song.album_id.__dict__,
    }

    return play


def search_columns(term):
    terms = term.split('.')
    if len(terms) == 2:
        if terms[0] in columns:
            if terms[1] in columns[terms[0]]:
                return columns[terms[0]][terms[1]]
    else:
        return None


def validate_val(new, partial_val=''):
    val = None
    if new[0] == '"' or new[0] == "'":
        partial_val += new
    elif partial_val != '':
        partial_val += ' ' + new
    else:
        val = new

    double = True
    single = True
    if not val:
        for char in partial_val:
            if char == '"':
                if double:
                    double = False
                else:
                    double = True
            elif char == "'":
                if single:
                    single = False
                else:
                    single = True
        if double and single:
            val = partial_val

    if val:
        val = val[1:][:-1]
    return val, partial_val


def convert(q):
    column = None
    column_valid = True
    operator = None
    operator_valid = True
    val = None
    partial_val = ''
    val_valid = False

    query = q.split(' ')

    filters = {}

    for item in query:
        if item == ' ':
            pass
        elif not column:
            val_valid = False
            column = search_columns(item)
            if not column:
                column_valid = False
                print('"{}" is not a valid column.'.format(column))
                break
        elif not operator:
            operator = operators.get(item)
            if not operator:
                operator_valid = False
                print('"{}" is not a valid operator.'.format(operator))
                break
        else:
            val, partial_val = validate_val(item, partial_val)

            if val:
                filters[column+operator] = val
                val_valid = True
                column = None
                operator = None
                val = None

    if val_valid:
        # For Debugging, Remove This
        for key, val in filters.items():
            print(key, ' : ', val)
        #not this
        return filters

    else:
        return None


if __name__ == "__main__":
    q = 'play.play_id < 100 song_id STARTSWITH m'
    print('Testing parsing: {}'.format(q))
    print(convert(q))

    print('')
    print('Testing List of Columns:')
    for item in list_columns():
        print('    '+item)

    print('')
    print('Testing List of Operators:')
    for item in list_operators():
        print('    '+item)








