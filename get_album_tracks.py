import requests
#return name:uri of each song
def get_album_tracks(album_id_list, token):

    tracks = {}

    for album_id in album_id_list:

        query = 'https://api.spotify.com/v1/albums/{}/tracks?limit=50'.format(album_id)

        response = requests.get(query,headers = {"Content-Type": "application/json", 
        
        "Authorization": f"Bearer {token}"})

        if str(response) == '<Response [200]>' or '<Response [201]>':

            response_json = response.json()

            items = response_json['items']

            for i in items:

                tracks[i['name']] = i['uri']

        else:
        
            raise Exception('Error in get_album_tracks')
    
    print('Getting artist tracks...')

    return tracks