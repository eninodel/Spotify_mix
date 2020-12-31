import requests
from collections import defaultdict

""" Used to get all the albums of a certain artist from Spotify

This is used to get all the albums from each artist in a dictionary. This is the 
first stage in getting the discography for each artist in order to thoroughly 
mix each playlist. By getting each album for each artist, the program will have 
a large set of songs to choose from for each artist. This is especially 
important for playlists that have multiple songs by the same artist. 

Ex:

    user_artists'_albums = get_artist_albums(artist_list, token)
"""

def get_artist_albums(artist_list, token):

    artist_dict = defaultdict(list)
    for artist in artist_list:
        #requests all the albums and singles for an artist
        query = "https://api.spotify.com/v1/artists/{}/albums?include_groups=album,single&limit=50".format(artist)
        response = requests.get(query, headers = {
                                            "Content-Type": "application/json", 
                                            "Authorization": f"Bearer {token}",
                                            })
        try:
            json_items = response.json()
            item = json_items['items']
            for i in item:
                album_id = i['id']
                artist_dict[artist].append(album_id)
        except IndexError:
            print(response.json())
            print('Index Error in get_artist_albums')
    print('Getting artist albums...')
    return artist_dict