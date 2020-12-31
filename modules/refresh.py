import requests

""" Used to refresh the authentication token given by Spotify.

The authentication token given by Spotify only lasts an hour. 
Therefore, it is refreshed everytime the program is run.

Ex:

        auth_token = refresh(refresh_token, client_b64_string)  
"""

def refresh(refresh_token, client_b64_string):

    query = "https://accounts.spotify.com/api/token"
    request_body = {
            "grant_type": "refresh_token", 
            "refresh_token": refresh_token,
            }
    headers = {"Authorization": "Basic " + client_b64_string}
    response = requests.post(query, data=request_body, headers=headers)
    response_json = response.json()
    return response_json["access_token"]