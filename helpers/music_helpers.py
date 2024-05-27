# ----- Imports -----
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import os
from dotenv import load_dotenv

# ----- MusicHelpers -----
load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

spotipy_auth_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
)
sp__i = spotipy.Spotify(auth_manager=spotipy_auth_manager)

class MusicHelpers:
    """
    """
    def __init__(self):
        """
        class [ MusicHelpers ]

        Provides:
        - Methods to get surface links for arists, playlists, and genres for users.
        """

        print('Instantiated class: [ {0} ].'.format(type(self).__name__))
        print(self.__doc__)

        pass
    
    def get_artist_track(self, artist_name):
        """
        """
        results = sp__i.search(
            q=f'artist:{artist_name}',
            type='track',
            limit=1
        )
        odict = {'name':'', 'url':''}
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            odict['name'] = track['name']
            odict['url'] = track['external_urls']['spotify']
            return odict
        
        odict['name'] = None
        odict['url'] = None
        return odict
    
    def get_genre_track(self, genre_name):
        """
        """
        results = sp__i.search(
            q=f'genre:{genre_name}',
            type='track',
            limit=1
        )
        odict = {'name':'', 'url':''}
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            odict['name'] = track['name']
            odict['url'] = track['external_urls']['spotify']
            return odict
        
        odict['name'] = None
        odict['url'] = None
        return odict
    
    def get_artist_playlist(self, artist_name):
        """
        """
        results = sp__i.search(
            q=f'artist:{artist_name}',
            type='playlist',
            limit=1
        )
        odict = {'name':'', 'url':''}
        if results['playlists']['items']:
            playlist = results['playlists']['items'][0]
            odict['name'] = playlist['name']
            odict['url'] = playlist['external_urls']['spotify']
            return odict
        
        odict['name'] = None
        odict['url'] = None
        return odict
    
    def get_genre_playlist(self, genre_name):
        """
        """
        results = sp__i.search(
            q=f'genre:{genre_name}',
            type='playlist',
            limit=1
        )
        odict = {'name':'', 'url':''}
        if results['playlists']['items']:
            playlist = results['playlists']['items'][0]
            odict['name'] = playlist['name']
            odict['url'] = playlist['external_urls']['spotify']
            return odict
        
        odict['name'] = None
        odict['url'] = None
        return odict