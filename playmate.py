# ----- Imports -----
import streamlit as st
from langchain.memory import ConversationBufferMemory

import random

from helpers.llm_helpers import LLMHelpers
from helpers.music_helpers import MusicHelpers
from helpers.context_helpers import ContextHelpers

llmh__i = LLMHelpers()
mh__i = MusicHelpers()
ch__i = ContextHelpers()

conversation_memory = ConversationBufferMemory()

# ----- PlayMate -----
st.set_page_config(page_title='PlayMate 🎶')

music_emojis = [
    '🎶', '🎵', '🎧', '🎺',
    '🎷', '🪗', '🪇', '🎹'
]

new_chat_prompt_suggestions = [
    "Create a relaxing 2-hour playlist",
    "Find upbeat songs for my HIIT workout",
    "Recommend some jazz music",
    "Help me discover new indie artists",
    "Suggest calming classical music",
    "I am hosting a house party and I NEED to create a pumping party playlist",
    "Explore electronic dance music (EDM)",
    "Find songs for a scenic California coast road trip",
    "Help me discover new rock bands",
    "I am learning to play the guitar -- suggest acoustic guitar music",
    "Recommend songs for studying",
    "Help me find chill lo-fi beats",
    "In desparate need of an Ibiza mix",
]

st.title(f'Play Mate {random.choice(music_emojis)}✨')

selected_new_chat_prompt_suggestions = random.sample(new_chat_prompt_suggestions, 4)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
else:
    for message in st.session_state.chat_history:
        conversation_memory.save_context(
            {'input': message['human']},
            {'output': message['AI']}
        )


if 'messages' not in st.session_state:
    st.session_state['messages'] = [{
        'role': 'assistant',
        'content': "Hi there! What's up for today?"
    }]

    st.markdown(f"## Hi there! What's up for today? {random.choice(music_emojis)}")
    new_chat_container_p1 = st.empty()
    new_chat_container_p2 = st.empty()

    with new_chat_container_p1.container():
        suggestion_1, suggestion_2 = st.columns(2)

        suggestion_1.markdown(selected_new_chat_prompt_suggestions[0])
        suggestion_2.markdown(selected_new_chat_prompt_suggestions[1])

    with new_chat_container_p2.container():
        suggestion_3, suggestion_4 = st.columns(2)
        
        suggestion_3.markdown(selected_new_chat_prompt_suggestions[2])
        suggestion_4.markdown(selected_new_chat_prompt_suggestions[3])

for message in st.session_state.messages[1:]:
    st.chat_message(message['role']).write(message['content'])
    
if user_input_message := st.chat_input(key='general-user-input'):
    st.session_state.messages.append({'role': 'user', 'content': user_input_message})
    st.chat_message('user').write(user_input_message)
    
    user_is_asking_about = llmh__i.understand_user_input(user_input_message, conversation_memory)['text']
    
    if 'general question' in user_is_asking_about.lower():
        app_reply = llmh__i.generate_basic_llm_response(user_input_message, conversation_memory)
    
    else:
        context_steer = ch__i.guide_app_request_using_user_intent(user_is_asking_about)
        
        print('################')
        print(user_is_asking_about)
        print(context_steer)
        print('################')
        
        if context_steer == 'song by artist':
            entity_name = ch__i.extract_entities(user_is_asking_about, context_steer)
            music_rec = mh__i.get_artist_track(entity_name)
            music_rec_track = music_rec['name']
            music_rec_url = music_rec['url']
            spotify_links_msg = f'Here is a Spotify link with music by {entity_name}'
            
        elif context_steer == 'song by genre':
            entity_name = ch__i.extract_entities(user_is_asking_about, context_steer)
            music_rec = mh__i.get_genre_track(entity_name)
            music_rec_track = music_rec['name']
            music_rec_url = music_rec['url']
            spotify_links_msg = f'Here is a Spotify link with {entity_name} music'
        
        elif context_steer == 'playlist by artist':
            entity_name = ch__i.extract_entities(user_is_asking_about, context_steer)
            music_rec = mh__i.get_artist_playlist(entity_name)
            music_rec_track = music_rec['name']
            music_rec_url = music_rec['url']
            spotify_links_msg = f'Here is a Spotify link with playlists by {entity_name}'
        
        elif context_steer == 'playlist by genre':
            entity_name = ch__i.extract_entities(user_is_asking_about, context_steer)
            music_rec = mh__i.get_genre_playlist(entity_name)
            music_rec_track = music_rec['name']
            music_rec_url = music_rec['url']
            spotify_links_msg = f'Here is a Spotify playlist with {entity_name} music'
        
        else:
            entity_name = 'cardi b'
            music_rec = mh__i.get_artist_track(entity_name)
            music_rec_track = music_rec['name']
            music_rec_url = music_rec['url']
            spotify_links_msg = f'Here is a Spotify playlist with {entity_name} music'
        
        print('################')
        print(entity_name)
        print('################')
        
        llm_reply = llmh__i.generate_basic_llm_response(user_input_message, conversation_memory)
        
        spotify_links_msg_with_recs = f"""
        {spotify_links_msg}:
        
        {music_rec_track} {music_rec_url}
        """
        app_reply_text = f"""
        {llm_reply['text']}
        
        {spotify_links_msg_with_recs}
        """
        app_reply = {
            'text': app_reply_text
        }
    
    st.session_state.messages.append({'role': 'assistant', 'content': app_reply['text']})
    st.chat_message('assistant').write(app_reply['text'])
    message = {'human': user_input_message, 'AI':app_reply['text']}
    st.session_state.chat_history.append(message)