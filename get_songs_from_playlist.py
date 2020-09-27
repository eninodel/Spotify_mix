import requests
def get_songs(playlist_id, token, uri_only = False):

    query ="https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

    response = requests.get(query, headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    response_json = response.json()

    song_list = []

    if str(response) == '<Response [200]>' or '<Response [201]>':

        # print(response_json['items'][0]['track']['artists'][0]['id'])

        #appends each song to list

        # print(response_json)

        for i in response_json['items']:

            if uri_only == True:

                song_list.append(i["track"]["uri"])

            else:

                song_list.append(i['track'])

        #makes sure to get all the songs in a large playlist

        while response_json['next'] is not None:

            response2 = requests.get(response_json['next'], headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

            response_json2 = response2.json()

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

 