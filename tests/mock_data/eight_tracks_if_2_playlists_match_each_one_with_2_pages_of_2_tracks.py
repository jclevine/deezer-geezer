two_moo_playlists = {
    'data': [
        {'id': '1', 'title': 'nope'},
        {'id': '2', 'title': 'moo-match'},
        {'id': '3', 'title': 'moo-too'},
    ]
}

moo_match_track_playlist_page_one = {
    'data': [
        {'id': 'moo-match-track-1'}, {'id': 'moo-match-track-2'}
    ],
    'next': 'http://api.deezer.com/playlist/2/tracks?access_token=access-token&expires=0&index=2'
}

moo_match_track_playlist_page_two = {
    'data': [
        {'id': 'moo-match-track-3'}, {'id': 'moo-match-track-4'}
    ]
}


moo_too_track_playlist_page_one = {
    'data': [
        {'id': 'moo-too-track-1'}, {'id': 'moo-too-track-2'}
    ],
    'next': 'http://api.deezer.com/playlist/3/tracks?access_token=access-token&expires=0&index=2'

}


moo_too_track_playlist_page_two = {
    'data': [
        {'id': 'moo-too-track-3'}, {'id': 'moo-too-track-4'}
    ]
}
