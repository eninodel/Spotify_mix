import requests
#returns a dictionary with a users playlist name as keys and ids as values
def get_user_playlists(username, token):

    query = "https://api.spotify.com/v1/users/{}/playlists?limit=50".format(username)

    response = requests.get(query, headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    if str(response) == '<Response [200]>' or '<Response [201]>':

        response_json = response.json()

        playlists = response_json['items']

        print('Please choose one of the following playlists to mix!')

        playlist_dictionary = {}

        for i in playlists:

            playlist_dictionary[i['name']] = i['id']
        
        return playlist_dictionary
    
    else:
        raise Exception('Error in get_user_playlists')