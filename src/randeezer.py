from src.common import writelines, uniq_randomize_list
from logging import warning


def randeezer(deezer_client, playlist_name_predicate, new_playlist_prefix,
              track_infos_filepath='track_infos.txt', do_delete_old_playlists=False):
    track_ids = deezer_client.get_track_ids_for_playlists(playlist_name_predicate)
    if not track_ids:
        warning('There are no tracks in playlists that match your predicate.')
        return

    randomized_ids = uniq_randomize_list(track_ids)

    deezer_client.create_playlists(new_playlist_prefix, randomized_ids)

    tracks = deezer_client.get_tracks(randomized_ids)
    writelines(track_infos_filepath, [str(track) for track in tracks])



