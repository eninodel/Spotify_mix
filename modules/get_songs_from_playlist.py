import requests

""" Used to obtain a list of the songs in the playlist the user chooses to 'mix'

This is used to get a list of all the songs in playlist. This function also has
the option to return a list of Spotify song uris or song titles only.

Ex:

    user_song_list = get_songs(playlist_id, token, uri_only = False)
"""

def get_songs(playlist_id, token, uri_only = False):

    query ="https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
    response = requests.get(query, headers = {
                                            "Content-Type": "application/json", 
                                            "Authorization": f"Bearer {token}",
                                            })
    if response.ok:
        response_json = response.json()
        song_list = []
        for i in response_json['items']:
            if uri_only == True:
                song_list.append(i["track"]["uri"])
            else:
                song_list.append(i['track'])
        #makes sure to get all the songs in a large playlist
        while response_json['next'] is not None:
            next_response = requests.get(response_json['next'], 
                                        headers = {
                                            "Content-Type": "application/json", 
                                            "Authorization": f"Bearer {token}",
                                            })
            response_json2 = next_response.json()
            for i in response_json2['items']:
                if uri_only == True:
                    song_list.append(i["track"]["uri"])
                else:
                    song_list.append(i['track'])
            response_json = response_json2
        print('Getting song ids...')
        song_list.reverse() 
        return song_list
    else:
        raise Exception('Error in get_songs_from_playlist')

 