def randeezer(deezer_client, playlist_name_predicate, new_playlist_prefix, track_infos_filepath='track_infos.txt'):
    hey = deezer_client.get_playlists(playlist_name_predicate)
