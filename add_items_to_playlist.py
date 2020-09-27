import json
import requests
from math import floor

def add_items_to_playlist(play_list_id, list_of_song_uris_to_add, token):
    
    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(play_list_id)

    #takes care of doing multiple requests for long playlists

    print('Adding items to new playlist....')

    if len(list_of_song_uris_to_add) > 100:

        length = (len(list_of_song_uris_to_add)/100)

        length = floor(length)+1

        for i in range(length):

            s = i*100

            l = i*100 +100

            short_song_list = list_of_song_uris_to_add[s:l]

            request_body = json.dumps({"uris": short_song_list})

            response = requests.post(query, data = request_body, headers = 

            {"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

            if str(response) == '<Response [200]>' or '<Response [201]>':

                pass

            else:
                
                raise Exception('Error in add_items_to_playlist')
        
        print('Done! Enjoy!')

    else:
        request_body = json.dumps({"uris": list_of_song_uris_to_add})

        response = requests.post(query, data = request_body, headers =

        {"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

        if str(response) == '<Response [200]>' or '<Response [201]>':

            print('Done! Enjoy!')

        else:

            raise Exception('Error in add_items_to_playlist')
