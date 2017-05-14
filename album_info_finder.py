import requests
import json
import logging
from ngram import NGram
import re


parenthetical_nonsense_regex = re.compile("([^\(]+)")


def get_album_infos(album_texts):
    # album_list_file = 'all_music.txt'

    albums = []
    for album_text in album_texts:
        try:
            # TODO: jlevine - Sometimes it wants quotes around the artist/album in the search query, sometimes not... Weird.
            artist, album_title = extract_album_info(album_text)
            response = requests.get('https://api.deezer.com/search/album', params={
                'q': 'artist:"{}" album:"{}"'.format(artist, album_title)
            })

            formatted_response = json.loads(response.text)['data']


            search_artist_name = artist.replace("\\", "")
            search_album_title = album_title.replace("\\", "")
            filtered = [format_album(album) for album in formatted_response if is_album_name_the_same(album['title'], search_album_title)]

            if not filtered:
                # Try without parenthetical nonsense
                filtered = [format_album(album) for album in formatted_response if
                            is_album_the_same_without_parenthetical_nonsense(album['title'], album_title)]

                if not filtered:
                    # Try without apostrophes
                    filtered = [format_album(album) for album in formatted_response
                                if is_album_the_same_without_parenthetical_nonsense(album['title'].replace("'", ''), album_title.replace("'", ''))]

                    if not filtered:
                        log(artist, album_title, formatted_response)
                        continue
            albums.append(filtered[0])
        except Exception as e:
            logging.error('General Album Failure: {} | {}'.format(album_text, e))
    return albums


def log(artist, album_title, formatted_response):
    logging.warning('Album Not Found: {} | {}'.format(artist, album_title))
    if formatted_response:
        logging.warning(
            'Closest Match: {} | {}'.format(formatted_response[0]['artist']['name'], formatted_response[0]['title']))
    else:
        logging.warning('Closest Match: None')


def strip_parenthetical_nonsense(s):
    return parenthetical_nonsense_regex.match(s).group(0).strip()


def format_album(album):
    return {
        'album_id': album['id'],
        'album_title': album['title'],
        'artist_id': album['artist']['id'],
        'artist': album['artist']['name']
    }


# TODO: jlevine - Maybe rather than do NGram comparison, just take a hunk out of the artist and album title and make sure those strings are "in" the target string.
def is_album_name_the_same(s1, s2):
    return NGram.compare(s1.lower(), s2.lower()) > 0.8


def is_album_the_same_without_parenthetical_nonsense(s1, s2):
    s1_without = strip_parenthetical_nonsense(s1)
    s2_without = strip_parenthetical_nonsense(s2)
    return is_album_name_the_same(s1_without, s2_without)


def extract_album_info(album_text):
    escaped_album_text = album_text.replace("'", "\\'")
    album_text_parts = escaped_album_text.split('/')
    if len(album_text_parts) == 3:
        return album_text_parts[1].strip(), album_text_parts[2].strip()
    return None


if __name__ == '__main__':
    album_list_file = 'all_music.txt'

    with open(album_list_file, 'r') as albums_file:
        albums = get_album_infos(list(albums_file))

    with open('album-info.json', 'w') as album_info_file:
        album_info_file.write(json.dumps(albums))
