import logging
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Required for the example
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from openvoice_api_client.client import OpenVoiceApiClient

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)  # Set the root logger level to DEBUG

API_URL = os.getenv("API_URL", "http://localhost:5000")
VERSION = 'v2'

# Create an instance of OpenVoiceApiClient with DEBUG log level
client = OpenVoiceApiClient(base_url=API_URL)

# Specify the output file path where the streamed content should be saved
output_file = 'outputs/generated_audio_stream.wav'

# Example generate_audio call with streaming
stream, status_code, response_message = client.generate_audio(
    version=VERSION,
    language='en',
    text='profoundly creative and freeing. And underneath everything, this playful exploration of language is about dissent, about rising up and crying out in support of that which is alive and vital. This book is about imagination, about truth-telling and contemplation; it is an undertaking that is fierce, creative, and honest. My own journey toward language was sparked in 1996 when I discovered Keith Basso’s astonishing book Wisdom Sits in Places. Writing about the unique place-making language of the Western Apache, Basso described language in a way that I’d never considered before, as roots and fragments strung together to sing of the land. This idea intrigued me so much that I began carrying Donald Borror’s classic little book, the Dictionary of Word Roots and Combining Forms. ',
    #speaker='kaiwen',
    #style='excited', # only v1
    #accent='en-au', # only v2
    response_format='stream',
    output_file=output_file  # Provide the output file path for the client to save the stream
)

if status_code == 200 and stream:
    client.logger.info(f"Streaming audio started. Saving to {output_file}")
else:
    client.logger.error(f"Failed to generate audio: {response_message}")
