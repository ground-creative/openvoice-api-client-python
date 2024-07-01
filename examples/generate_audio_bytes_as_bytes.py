import logging
import sys
import os
from dotenv import load_dotenv

import traceback

load_dotenv()

# Required for the example
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from openvoice_api_client.client import OpenVoiceApiClient

#logging.basicConfig(level=logging.DEBUG)  # Set the root logger level to DEBUG

API_URL = os.getenv("API_URL", "http://localhost:5000")
VERSION = 'v2'
    
# Create an instance of OpenVoiceApiClient with DEBUG log level
client = OpenVoiceApiClient(base_url=API_URL, log_level=logging.DEBUG)
output_file='outputs/generated_audio_bytes_as_bytes.wav'
if os.path.exists(output_file):
    os.remove(output_file)

try:
    # Example generate_audio call
    audio_bytes, status_code, response_message = client.generate_audio(
        version=VERSION,
        model='en',
        input='Hello, this is a test. I am here, there and everywhere',
        speed=1.0,
        #speaker='kaiwen',
        #style='excited', # only v1
        #accent='en-au', # only v2
        response_format='bytes',
    )
    if status_code == 200:
        with open(output_file, 'wb') as audio_file:
            audio_file.write(audio_bytes)
        client.logger.info(f"Audio file saved successfully, bytes received: {len(audio_bytes)}")
    else:
        client.logger.error(f"Failed to generate audio: {len(audio_bytes)}")
except Exception as e:
    print(traceback.format_exc())
    print(f"An error occurred writing file: {e}")



