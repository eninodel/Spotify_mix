import requests
import json
from time import sleep
from collections import defaultdict

""" Used to get each song of each album for each artist in the input dictionary.

This function is used to get every track for every album for each artist in the 
input dictionary. This completes the second part of getting the discography for
each artist in a playlist the user chooses to 'mix'

Ex:

    discographies = get_album_tracks_and_append_to_dict(artist_dict_with_albums, 
                                                                          token)
"""

def get_album_tracks_and_append_to_dict(artist_dict_with_albums, token):

    artist_dict_with_discography = defaultdict(list)
    for artist, album_list in artist_dict_with_albums.items():
        for album_id in album_list:
            query = f'https://api.spotify.com/v1/albums/{album_id}/tracks?limit=50'
            response = requests.get(query, headers = {
                                            "Content-Type": "application/json", 
                                            "Authorization": f"Bearer {token}"
                                            })
            response_json = response.json()
            sleep(0.05) #this is used to not overload the Spotify API.
            try:
                if response.ok:
                    for song in response_json['items']:
                        artist_dict_with_discography[artist].append(song['uri'])
                elif (response_json['error']['message'] == 
                      'API rate limit exceeded'):
                    print(response_json)
                    raise Exception('API rate limit' 
                                    'exceeded in get_album_tracks')
                else:
                    print(str(response_json))
                    raise Exception('unkown error in get_album_tracks')
            except KeyError:
                print(str(response_json))
                raise KeyError
    return artist_dict_with_discography