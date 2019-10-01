from src.common import writelines, uniq_randomize_list, readlines
from logging import warning


# TODO: jlevine - Implement deleting old playlists?
def randeezer(deezer_client, playlist_name_predicate, new_playlist_prefix,
              track_infos_file, do_delete_old_playlists=False):
    track_ids = deezer_client.get_track_ids_for_playlists(playlist_name_predicate)
    if not track_ids:
        warning('There are no tracks in playlists that match your predicate.')
        return

    # TODO: jlevine - We want to do this in case we get all the IDs from Deezer
    # but something fails. We don't want to have to get the IDs again if we'd already retrieved them.
    # We should be:
    # 1. Save the ids (by playlist or just new + like vs nope tracks?) after we retrieve them.
    #    It's doing this now, but the path where it saves it is hard-coded
    # 2. Allow for client to pass in this file of ids (or multiple files?) and go straight into
    #    randomizing them and creating the playlists.

    # This is the currently hard-coded grabbing of all the IDs from a file
    # This would need to be passed in or something, obviously.
    # randomized_ids = [str(s).strip() for s in readlines('C:\\Users\\hodor\\Desktop\\all_music_ids.txt')]
    randomized_ids = [str(x) for x in uniq_randomize_list(track_ids)]

    # This is where it saves the IDs to a file in case something goes awry.
    # We'd obviously want the client to be able to specify where to put it and not hard-code it.
    all_randomized_ids_path = 'C:\\Users\\hodor\\Desktop\\test-20190930.txt'
    writelines(all_randomized_ids_path, randomized_ids)
    deezer_client.create_playlists(new_playlist_prefix, randomized_ids)

    tracks = deezer_client.get_tracks(randomized_ids, track_infos_file)
    writelines(track_infos_file, [str(track) for track in tracks])



