from Refresh import refresh
from Secrets import username, client_b64_string, refresh_token
from get_user_playlists import get_user_playlists
from get_songs_from_playlist import get_songs
from get_artist_albums import get_artist_albums
from create_playlist import create_playlist
from add_items_to_playlist import add_items_to_playlist
from collections import Counter
from collections import defaultdict
import requests
import random
from time import sleep

class Mixer:
    def __init__(self, username = username, client_b64_string = client_b64_string, refresh_token = refresh_token):
        self.token = refresh(refresh_token, client_b64_string)
        self.base_playlist_id = ''
        self.base_playlist_name = ''
        self.song_dict = {}
        self.artist_list = []
        self.artist_with_multiple_songs = []
        self.artist_dict = defaultdict(list)
        self.artist_dict_who_have_multiple_songs_in_playlist = defaultdict(list)
        self.artist_dict_who_have_one_song_in_playlist = defaultdict(list)
        self.artist_albums_dict = defaultdict(list)
        self.song_list = []
        self.single_artist_dict = {}

    def print_and_accept_user_playlist_choice(self):
        
        a = get_user_playlists(username,self.token)

        print("Please choose one of the following")

        for name in a:

            print(name)

        playlist = input('Type playlist name here: ')

        self.base_playlist_name = playlist

        self.base_playlist_id = a[playlist]

    def create_song_dict(self):
        
        song_list = get_songs(self.base_playlist_id, self.token)

        for song in song_list:

            self.artist_list.append(song['artists'][0]['id'])
        
        d = dict((Counter(self.artist_list)))

        for item in d.items():

            artist = item[0]
            
            times_in_playlist = item[1]

            if times_in_playlist > 1:

                self.artist_with_multiple_songs.append(artist)

        # print(list(enumerate(song_list)))

        for i, song in enumerate(song_list):
            
            artist = song['artists'][0]['id']

            song_uri = song['uri']

            self.song_dict[song_uri] = [artist, i]

            self.song_list.append(song_uri)
        
    def count_tracks_by_same_artist(self):
        
        for song_data in self.song_dict.items():

            # print('herwerwerw')

            # print(song)

            song = song_data[0]

            artist = song_data[-1][0]

            # print(self.artist_with_multiple_songs)

            if artist in self.artist_with_multiple_songs:

                # print('here')

                self.artist_dict[artist].append(song)

                # print(self.artist_dict)

            else:
                
                self.single_artist_dict[artist] = song
        
        # print(dict(self.artist_dict))

    def get_tracks_for_each_artist(self):

        # for artist in self.artist_list:

        #     query = f'https://api.spotify.com/v1/artists/{artist}/top-tracks?country=US'

        #     response = requests.get(query, headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"})

        #     response_json = response.json()

        #     for i in response_json['tracks']:

        #         self.artist_dict_who_have_multiple_songs_in_playlist[artist].append(i['uri'])

        self.artist_albums_dict = get_artist_albums(self.artist_list,self.token)

        for artist, album_list in self.artist_albums_dict.items():
            
            for album in album_list:

                query = f'https://api.spotify.com/v1/albums/{album}/tracks?limit=50'

                response = requests.get(query, headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"})

                response_json = response.json()


                sleep(0.2)

                try:

                    for song in response_json['items']:

                        # print(song['uri'])
                        if artist in self.artist_with_multiple_songs:

                            self.artist_dict_who_have_multiple_songs_in_playlist[artist].append(song['uri'])

                        else:

                            self.artist_dict_who_have_one_song_in_playlist[artist].append(song['uri'])

                    # print(response_json)
                except KeyError:
                    print(response_json)
                    break
        print(dict(self.artist_dict_who_have_multiple_songs_in_playlist))

    def switch_out_songs(self):
        for artist in self.artist_list:
            #interates through all the artists with duplicate songs in the playlist
            if artist in self.artist_dict_who_have_multiple_songs_in_playlist.keys():

                artist_discography = self.artist_dict_who_have_multiple_songs_in_playlist[artist]

                artist_songs_in_playlist = self.artist_dict[artist]
                #checks to see if the artists discography is large enough to replace every song with a unique song. if 0.5 or below every song can be replaced
                if (len(artist_songs_in_playlist)/len(artist_discography)) > 0.5:
                    #checks if every song in the artist's discography is in the playlist
                    if Counter(artist_discography) == Counter(artist_songs_in_playlist):

                        new_songs = artist_songs_in_playlist.copy()
                        
                        moved_song = new_songs.pop(-1)

                        new_songs.insert(0,moved_song)
                        #replaces the old song with the new one
                        for i,old_song in enumerate(artist_songs_in_playlist):

                            data = self.song_dict[old_song]

                            index = data[-1]

                            self.song_list.pop(index)

                            self.song_list.insert(index,new_songs[i])
                    #not enough songs to replace every song but enough to replace some
                    else:
                        #finds the number of songs to move to the front
                        # number_of_songs_to_move = abs(len(artist_songs_in_playlist)-len(artist_discography))

                        new_songs = [i for i in  artist_discography + artist_songs_in_playlist if i not in artist_discography or i not in artist_songs_in_playlist]

                        list_of_songs_to_slice = new_songs + artist_discography

                        new_songs_to_insert = list_of_songs_to_slice[:len(artist_songs_in_playlist)]

                        for i,old_song in enumerate(artist_songs_in_playlist):

                            data = self.song_dict[old_song]

                            index = data[-1]

                            self.song_list.pop(index)

                            self.song_list.insert(index,new_songs_to_insert[i])

                #all the songs in the playlist can be replaced
                else:
                    
                    new_songs = [i for i in  artist_discography + artist_songs_in_playlist if i not in artist_discography or i not in artist_songs_in_playlist]

                    new_songs_to_insert = new_songs[:len(artist_songs_in_playlist)]

                    for i,old_song in enumerate(artist_songs_in_playlist):

                        data = self.song_dict[old_song]

                        index = data[-1]

                        self.song_list.pop(index)

                        self.song_list.insert(index,new_songs_to_insert[i])

            else:

        #         query = f"https://api.spotify.com/v1/artists/{artist}/albums?include_groups=album,single&limit=50"

        #         response = requests.get(query, headers = {"Content-Type": "application/json", 
        
        # "Authorization": f"Bearer {self.token}"})

        #         # print(response.json())

        #         #chooses a random album from an artist
        #         try:
        #             item = random.choice(response.json()['items'])


        #             # item_type = item['album_type']

        #             item_id = item['id']

        #             self.artist_number_of_albums[artist] = len(response.json()['items'])
        #             self.album_id_list.append(item_id)
                    
        #         except IndexError:
        #             print(response.json())
        #             print('Index Error in get_artist_albums')                
                    
                artist_discography = self.artist_dict_who_have_one_song_in_playlist[artist]

                artist_song_in_playlist = self.single_artist_dict[artist]

                new_songs = [i for i in  artist_discography + [artist_song_in_playlist] if i not in artist_discography or i not in [artist_song_in_playlist]]

                for i,old_song in enumerate([artist_song_in_playlist]):

                    data = self.song_dict[old_song]

                    index = data[-1]

                    self.song_list.pop(index)

                    self.song_list.insert(index,new_songs[i])


    def create_and_add_to_playlist(self):

        new_playlist_id = create_playlist(self.base_playlist_name,username, self.token)

        self.song_list.reverse()

        add_items_to_playlist(new_playlist_id, self.song_list, self.token)




                


m = Mixer()
m.print_and_accept_user_playlist_choice()
m.create_song_dict()
m.count_tracks_by_same_artist()
m.get_tracks_for_each_artist()
m.switch_out_songs()
m.create_and_add_to_playlist()
        