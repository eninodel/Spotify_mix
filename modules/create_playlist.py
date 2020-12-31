import requests
import json

""" Used to create a new empty playlist ready to accept 'mixed' songs.

This function simply creates a new playlist for the program to access
later when adding the 'mixed' songs. Returns a playlist id.

Ex:
    
    create_playlist(base_playlist_name,username,token)
"""

def create_playlist(base_playlist_name,username,token):

    query = "https://api.spotify.com/v1/users/{}/playlists".format(username)
    request_body = json.dumps({
                            'name': '{} mix'.format(base_playlist_name), 
                            "public":False, 
                            "description" : "{} mix".format(base_playlist_name),
                            })
    response = requests.post(query, 
                            data = request_body, 
                            headers = {
                                    "Content-Type": "application/json", 
                                    "Authorization": "Bearer {}".format(token),
                                    })
    playlist_id = response.json()['uri']
    new_playlist_id = playlist_id[-22:]
    print('Creating new playlist...')
    return new_playlist_id