import requests
import json
from time import sleep
#return name:uri of each song
def get_album_tracks_and_append_to_dict(artist, album_id_list, artist_dict, token):

    for album_id in album_id_list:

        query = 'https://api.spotify.com/v1/albums/{}/tracks?limit=50'.format(album_id)

        response = requests.get(query, headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

        response_json = response.json()

        sleep(0.05)
        try:
            if response.ok:

                for song in response_json['items']:

                    artist_dict[artist].append(song['uri'])
            elif response_json['error']['message'] != 'API rate limit exceeded':
            
                print(response_json)

                raise Exception('API rate limit exceeded in get_album_tracks')

            else:
                print(str(response_json))
                raise Exception('unkown error in get_album_tracks')
        except KeyError:

            print(str(response_json))

            raise KeyError
