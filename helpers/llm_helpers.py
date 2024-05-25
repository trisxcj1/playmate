# ----- Imports -----
import litellm

from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler    
from langchain import PromptTemplate, LLMChain
from langchain.chains import LLMChain, SequentialChain, RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import GPT4AllEmbeddings
from langchain import hub

from langchain.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

from bs4 import BeautifulSoup

import streamlit as st

# ----- LLMHelpers -----