import requests

#used for refreshing Spotify token
def refresh(refresh_token,client_b64_string):

        query = "https://accounts.spotify.com/api/token"

        request_body = {'grant_type': "refresh_token", 'refresh_token': refresh_token}

        headers = {"Authorization" : "Basic " + client_b64_string}

        response = requests.post(query, data = request_body, headers = headers)

        response_json = response.json()

        return response_json['access_token']