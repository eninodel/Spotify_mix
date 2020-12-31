import requests

""" Returns a dictionary with the user's playlists

In order for a user to select the playlist to "mix" the function obtains and 
returns a dictionary with each playlist name as a key and the Spotify playlist 
id as the value for future use. The token in the function is the Spotify 
authentication token

Ex:

    user_playlists = get_user_playlists(username,token)
"""
33333333333333333333333333333333333333333333333333333333333333333333333333333333
def get_user_playlists(username, token):

    query = f"https://api.spotify.com/v1/users/{username}/playlists?limit=50"
    response = requests.get(query, headers={
                                            "Content-Type": "application/json", 
                                            "Authorization": f"Bearer {token}",
                                            })
    if response.ok:
        response_json = response.json()
        playlists = response_json['items']
        print('Please choose one of the following playlists to mix!')
        playlist_dictionary = {}
        for i in playlists:
            playlist_dictionary[i['name']] = i['id']
        return playlist_dictionary
    else:
        raise Exception('Error in get_user_playlists')