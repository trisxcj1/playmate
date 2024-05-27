# ----- Imports -----
import re

# ----- ContextHelpers -----

class ContextHelpers:
    """
    """
    def __init__(self):
        """
        class [ ContextHelpers ]

        Provides:
        - Methods direct the MusicHelpers, given a user's intent.
        """

        print('Instantiated class: [ {0} ].'.format(type(self).__name__))
        print(self.__doc__)

        pass
    
    def guide_app_request_using_user_intent(self, user_intent):
        """
        """
        song_by_artist_options = [
            r'.*\bsong by artist\b.*',
            r'song by artist name: \w+'
        ]
        
        song_by_genre_options = [
            r'.*\ba song in the genre\b.*',
            r'.*\ba .* song\b.*'
        ]
        
        playlist_by_artist_options = [
            r'.*\ba playlist by artist\b.*',
            r'.*\bsongs by artist\b.*'
        ]
        
        playlist_by_genre_options = [
            r'.*\ba playlist by genre\b.*',
            r'.*\ba playlist in the genre\b.*',
            r'.*\bsongs in the genre\b.*',
            r'.*\bsongs in the .* genre\b.*',
            r'.*\bThis user is asking for a playlist in the genre name\b.*',
            r'.*\b.* asking for a .* playlist\b.*'
        ]
        
        steer_towards = ''
        
        for pattern in song_by_artist_options:
            print(f'checking the [{pattern}] pattern')
            if re.search(pattern, user_intent, re.IGNORECASE):
                steer_towards = 'song by artist'
                break
        
        if not steer_towards:
            for pattern in song_by_genre_options:
                print(f'checking the [{pattern}] pattern')
                if re.search(pattern, user_intent, re.IGNORECASE):
                    steer_towards = 'song by genre'
                    break
                
        if not steer_towards:
            for pattern in playlist_by_artist_options:
                print(f'checking the [{pattern}] pattern')
                if re.search(pattern, user_intent, re.IGNORECASE):
                    steer_towards = 'playlist by artist'
                    break
                
        if not steer_towards:
            for pattern in playlist_by_genre_options:
                print(f'checking the [{pattern}] pattern')
                if re.search(pattern, user_intent, re.IGNORECASE):
                    steer_towards = 'playlist by genre'
                    break

        print(f"Steer towards: {steer_towards}")
        return steer_towards
    
    def extract_entities(self, user_intent, context_steer):
        """
        """
        if context_steer == 'song by artist':
            entity_name = user_intent.split("artist name:")[-1].strip().strip('"').strip('.')
            
        if context_steer == 'song by genre':
            entity_name = user_intent.split("genre name:")[-1].strip().strip('"').strip('.')
            
        if context_steer == 'playlist by artist':
            entity_name = user_intent.split("artist name:")[-1].strip().strip('"').strip('.')
            
        if context_steer == 'playlist by genre':
            entity_name = user_intent.split("genre name:")[-1].strip().strip('"').strip('.')
            if entity_name in ['', ' ', None]:
                pattern_1 = r'\basking for (\w+s) songs\b'
                pattern_1_match = re.search(pattern_1, user_intent, re.IGNORECASE)
                entity_name = pattern_1_match.group(1)
                
            if entity_name in ['', ' ', None]:
                pattern_2 = r'\basking for a (\w+s) playlist\b'
                pattern_2_match = re.search(pattern_2, user_intent, re.IGNORECASE)
                entity_name = pattern_1_match.group(1)
        
        return entity_name
        