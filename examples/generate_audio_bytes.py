import logging
import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from openvoice_api_client.client import OpenVoiceApiClient

#logging.basicConfig(level=logging.DEBUG)  # Set the root logger level to DEBUG

API_URL = os.getenv("API_URL", "http://localhost:5000")
VERSION = 'v2'
    
# Create an instance of OpenVoiceApiClient with DEBUG log level
OpenVoiceApiClient = OpenVoiceApiClient(base_url=API_URL, log_level=logging.DEBUG)

# Example generate_audio call
url, status_code, response_message = OpenVoiceApiClient.generate_audio(
    version=VERSION,
    language='en',
    text='Hello, this is a test. I am here, there and everywhere',
    speed=1.0,
    #speaker='kaiwen',
    #style='excited', # only v1
    #accent='en-au', # only v2
    response_format='bytes',
    output_file='outputs/generated_audio_bytes.wav'
)

if status_code == 200:
    OpenVoiceApiClient.logger.info(f"Audio file saved successfully or URL received: {url}")
else:
    OpenVoiceApiClient.logger.error(f"Failed to generate audio: {response_message}")