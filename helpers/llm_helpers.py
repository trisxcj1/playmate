# ----- Imports -----
import litellm
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler    
from langchain import PromptTemplate, LLMChain
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory


import streamlit as st

# ----- LLMHelpers -----
class LLMHelpers:
    """
    Helper class to interact with LLM models for this application.
    """
    
    llm = Ollama(
        model='mistral',
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]),
        temperature=0.9
    )

    understand_user_input_prompt_template = PromptTemplate(
        input_variables=['history', 'input'],
        template="""
        ### Task:
        You are to determine user intent and extract relevant information.
        
        1. Identify the user's intent:
        - If the user is asking for a song in general:
            - Ressponse: "This user is asking for a song"
            
        - If the user is asking for a song by a specific artist:
            - Ressponse: "This user is asking for a song by artist name: <artist_name>"
            
        - If the user is asking for a specific song:
            - Ressponse: "This user is asking for the song name: <song_name>"
            
        - If the user is asking for a song in a specific genre:
            - Ressponse: "This user is asking for a song in the genre name: <genre_name>"
            
        - If the user is asking for a playlist in general:
            - Response: "This user is asking for a playlist"
            
        - If the user is asking for a playlist by a specific artist:
            - Response: "This user is asking for a playlist by artist name: <artist_name>"
            
        - If the user is asking for a playlist with songs from multiple artists:
            - Response: "This user is asking for a playlist with songs from the following arist names: <list_of_artist_names>"
        
        - If the user is asking for a playlist in a specific genre:
            - Ressponse: "This user is asking for a playlist in the genre name: <genre_name>"
            
        - If you cannot identify exactly what the user is asking:
            - Response: "general question"
        
        ### Instruction:
        Read the user prompt and the conversation history, and complete the task above.
        The response should be one from the options provided above.

        ### Conversation history:
        {history}

        ### Prompt:
        {input}
        """
    )
    
    basic_llm_prompt_template = PromptTemplate(
        input_variables=['history', 'input'],
        template="""
        ### Instruction:
        You are a helpful assistant who is a lively entertainer and a well-versed disc jockey.
        Users are coming to you to help them find and listen to music or playlists. Read the
        prompt below, match the user's mood/energy, and continue the conversation in an entertaining manner with the most
        appopriate response.
        
        Be conversational and keep the music pumping! All responses must be relates to
        suggesting music and playlists, and must be less than 200 words.
        
        ### Conversation history:
        {history}

        ### Prompt:
        {input}
        """
    )
    
    def __init__(self):
        """
        class [ LLMHelpers ]

        Provides:
        - Methods to easily interact with LLM models for this application.
        """

        print('Instantiated class: [ {0} ].'.format(type(self).__name__))
        print(self.__doc__)

        pass
    
    def understand_user_input(self, input_message, conversation_memory):
        """
        Understand user input and determine their intent.
        """
        conversation_chain = LLMChain(
            llm=self.llm,
            prompt=self.understand_user_input_prompt_template,
            memory=conversation_memory,
            verbose=True
        )
        llm_response = conversation_chain(input_message)
        return llm_response
        
          
    def generate_basic_llm_response(self, input_message, conversation_memory):
        """
        Generate a basic LLM response for general user input.
        """
        conversation_chain = LLMChain(
            llm=self.llm,
            prompt=self.basic_llm_prompt_template,
            memory=conversation_memory,
            verbose=True
        )
        llm_response = conversation_chain(input_message)
        return llm_response