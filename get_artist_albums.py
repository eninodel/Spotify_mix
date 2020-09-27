import requests
from collections import defaultdict

def get_artist_albums( artist_list, token):

    artist_dict = defaultdict(list)

    for artist in artist_list:
        #requests all the albums and singles for an artist
        query = "https://api.spotify.com/v1/artists/{}/albums?include_groups=album,single&limit=50".format(artist)

        response = requests.get(query, headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

        # print(response.json())


        try:
            item = response.json()['items']

            for i in item:

                album_id = i['id']

                artist_dict[artist].append(album_id)
            # item_type = item['album_type']


        except IndexError:
            print(response.json())
            print('Index Error in get_artist_albums')
        # except IndexError:
        #     while response_json['next'] is not None:

        #         response2 = requests.get(response_json['next'], headers = self.headers)

        #         response_json2 = response2.json()

        #         for i in response_json2['items']:

        #             self.song_list.append(i["track"]["uri"])

        #         response_json = response_json2
    print('Getting artist albums...')

    return artist_dict

# def find_duplicates(self):

#     for i,song in enumerate(self.similar_songs_list):
#         if song in self.song_list:


