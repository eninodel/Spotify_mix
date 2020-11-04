
from Refresh import refresh
from Secrets import username, client_b64_string, refresh_token
from get_user_playlists import get_user_playlists
from get_songs_from_playlist import get_songs
from get_artist_albums import get_artist_albums
from create_playlist import create_playlist
from get_album_tracks import get_album_tracks_and_append_to_dict
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
        self.song_dict_with_artists_and_indexes = {}
        self.main_artist_id_list = []
        self.artists_with_multiple_songs_in_playlist_list = []
        self.artist_dict_with_songs_in_playlist = defaultdict(list)
        self.artist_dict_with_discography = defaultdict(list)
        self.artist_dict_with_songs_in_playlist_who_have_one_song_in_playlist = defaultdict(list)
        self.artist_albums_dict = defaultdict(list)
        self.song_list = []
        self.single_artist_dict = {}

    def print_and_accept_user_playlist_choice(self):
        
        user_playlists = get_user_playlists(username,self.token)

        for name in user_playlists:

            print(name)

        playlist = input('Type playlist name here: ')

        self.base_playlist_name = playlist

        self.base_playlist_id = user_playlists[playlist]

    def create_song_dict(self):
        #returns a list with each song in the playlist
        song_list = get_songs(self.base_playlist_id, self.token)

        for song in song_list:
            #appends 
            self.main_artist_id_list.append(song['artists'][0]['id'])
        
        artist_times_dict = dict((Counter(self.main_artist_id_list)))

        for item in artist_times_dict.items():

            artist = item[0]
            
            times_in_playlist = item[1]

            if times_in_playlist > 1:

                self.artists_with_multiple_songs_in_playlist_list.append(artist)

        for song in song_list:
            
            artist = song['artists'][0]['id']

            song_uri = song['uri']

            self.artist_dict_with_songs_in_playlist[artist].append(song_uri)

            self.song_list.append(song_uri)

    def get_tracks_for_each_artist(self):
        #converts the artist id list into a set to account for large playlists where there would be artist with multiple songs
        artist_id_set = set(self.main_artist_id_list)
        #returns a default dictionary with each artist as the key and the values being the albums associated with each artist
        self.artist_albums_dict = get_artist_albums(artist_id_set,self.token)
        #gets each song in every album by the artist and 
        for artist, album_list in self.artist_albums_dict.items():
            get_album_tracks_and_append_to_dict(artist,album_list,self.artist_dict_with_discography,self.token)

        print('Getting artist tracks...')
        # print(self.artist_dict_with_discography)

    def switch_out_songs(self):

        main_artist_id_list = set(self.main_artist_id_list)

        artists_with_multiple_songs_in_playlist = set(self.artists_with_multiple_songs_in_playlist_list)
        for artist in main_artist_id_list:
            #interates through all the artists with duplicate songs in the playlist
            if artist in artists_with_multiple_songs_in_playlist:

                artist_discography = self.artist_dict_with_discography[artist]

                artist_songs_in_playlist = self.artist_dict_with_songs_in_playlist[artist]

                #checks to see if the artists discography is large enough to replace every song with a unique song. if 0.5 or below every song can be replaced
                if (len(artist_songs_in_playlist)/len(artist_discography)) > 0.5:
                    #checks if every song in the artist's discography is in the playlist
                    if Counter(artist_discography) == Counter(artist_songs_in_playlist):

                        new_songs = artist_songs_in_playlist.copy()
                        
                        moved_song = new_songs.pop(-1)

                        new_songs.insert(0,moved_song)
                        #replaces the old song with the new one
                        for i,old_song in enumerate(artist_songs_in_playlist):

                            index = self.song_list.index(old_song)

                            self.song_list.pop(index)

                            self.song_list.insert(index,new_songs[i])
                    #not enough songs to replace every song but enough to replace some
                    else:
                        #finds the number of songs to move to the front

                        new_songs = [i for i in  artist_discography + artist_songs_in_playlist if i not in artist_discography or i not in artist_songs_in_playlist]

                        random.shuffle(artist_discography)

                        list_of_songs_to_slice = new_songs + artist_discography

                        new_songs_to_insert = list_of_songs_to_slice[:len(artist_songs_in_playlist)]

                        for i,old_song in enumerate(artist_songs_in_playlist):

                            index = self.song_list.index(old_song)

                            self.song_list.pop(index)

                            self.song_list.insert(index,new_songs_to_insert[i])

                #all the songs in the playlist can be replaced
                else:
                    
                    new_songs = [i for i in  artist_discography + artist_songs_in_playlist if i not in artist_discography or i not in artist_songs_in_playlist]

                    random.shuffle(new_songs)

                    new_songs_to_insert = new_songs[:len(artist_songs_in_playlist)]

                    for i,old_song in enumerate(artist_songs_in_playlist):

                        index = self.song_list.index(old_song)

                        self.song_list.pop(index)

                        self.song_list.insert(index,new_songs_to_insert[i])

            else:

                artist_discography = self.artist_dict_with_discography[artist]

                artist_song_in_playlist = self.artist_dict_with_songs_in_playlist[artist]

                new_songs = [i for i in  artist_discography + [artist_song_in_playlist] if i not in artist_discography or i not in [artist_song_in_playlist]]

                index = self.song_list.index(artist_song_in_playlist[0])

                self.song_list.pop(index)

                self.song_list.insert(index,new_songs[0])

    def create_and_add_to_playlist(self):

        new_playlist_id = create_playlist(self.base_playlist_name,username, self.token)

        # self.song_list.reverse()

        add_items_to_playlist(new_playlist_id, self.song_list, self.token)


m = Mixer()
m.print_and_accept_user_playlist_choice()
m.create_song_dict()
m.get_tracks_for_each_artist()
m.switch_out_songs()
m.create_and_add_to_playlist()
        