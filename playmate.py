# ----- Imports -----
import streamlit as st
from langchain.memory import ConversationBufferMemory

import random

from helpers.llm_helpers import LLMHelpers
from helpers.music_helpers import MusicHelpers

llmh__i = LLMHelpers()
mh__i = MusicHelpers()

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
    
    user_is_asking_about = llmh__i.understand_user_input(user_input_message, conversation_memory)['text'].lower()
    
    if 'general question' in user_is_asking_about:
        app_reply = llmh__i.generate_basic_llm_response(user_input_message, conversation_memory)
    
    else:
        if 'a song by artist' in user_is_asking_about:
            artist_name = user_is_asking_about.split("artist name:")[-1].strip().strip('"')
            llm_reply = llmh__i.generate_basic_llm_response(user_input_message, conversation_memory)
            music_rec = mh__i.get_track(artist_name)
            music_rec_track = music_rec['name']
            music_rec_url = music_rec['url']
        else:
            artist_name = 'cardi b'
            llm_reply = llmh__i.generate_basic_llm_response(user_input_message, conversation_memory)
            music_rec = mh__i.get_track(artist_name)
            music_rec_track = music_rec['name']
            music_rec_url = music_rec['url']
        
        spotify_links_msg = f"""
        Here is a Spotify link with music by {artist_name}:
        
        {music_rec_track} {music_rec_url}
        """
        app_reply_text = f"""
        {llm_reply['text']}
        
        {spotify_links_msg}
        """
        app_reply = {
            'text': app_reply_text
        }
    
    st.session_state.messages.append({'role': 'assistant', 'content': app_reply['text']})
    st.chat_message('assistant').write(app_reply['text'])
    message = {'human': user_input_message, 'AI':app_reply['text']}
    st.session_state.chat_history.append(message)