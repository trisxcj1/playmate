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
    
    def get_track(self, artist_name):
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