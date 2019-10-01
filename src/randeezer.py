from src.common import writelines, uniq_randomize_list, readlines
from logging import warning


def randeezer(deezer_client, playlist_name_predicate, new_playlist_prefix,
              track_infos_file, do_delete_old_playlists=False):
    track_ids = deezer_client.get_track_ids_for_playlists(playlist_name_predicate)
    if not track_ids:
        warning('There are no tracks in playlists that match your predicate.')
        return

    # randomized_ids = [str(s).strip() for s in readlines('C:\\Users\\hodor\\Desktop\\all_music_ids.txt')]
    randomized_ids = [str(x) for x in uniq_randomize_list(track_ids)]
    all_randomized_ids_path = 'C:\\Users\\hodor\\Desktop\\test-20190930.txt'
    writelines(all_randomized_ids_path, randomized_ids)
    deezer_client.create_playlists(new_playlist_prefix, randomized_ids)

    tracks = deezer_client.get_tracks(randomized_ids, track_infos_file)
    writelines(track_infos_file, [str(track) for track in tracks])



