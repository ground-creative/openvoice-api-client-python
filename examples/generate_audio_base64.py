import logging
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Required for the example
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from openvoice_api_client.client import OpenVoiceApiClient

#logging.basicConfig(level=logging.DEBUG)  # Set the root logger level to DEBUG

API_URL = os.getenv("API_URL", "http://localhost:5000")
VERSION = 'v2'
    
# Create an instance of OpenVoiceApiClient with DEBUG log level
client = OpenVoiceApiClient(base_url=API_URL, log_level=logging.DEBUG)
output_file='outputs/generated_audio_base64.wav'
if os.path.exists(output_file):
    os.remove(output_file)

try:
    # Example generate_audio call
    audio_file, status_code, response_message = client.generate_audio(
        version=VERSION,
        model='en',
        input='Hello, this is a test. I am here, there and everywhere',
        speed=1.0,
        #speaker='kaiwen',
        #style='excited', # only v1
        #accent='en-au', # only v2
        response_format='base64',
        output_file=output_file
    )

    if status_code == 200:
        with open(audio_file, 'rb') as audio_file:
            audio_data = audio_file.read()
        client.logger.info(f"Audio file saved successfully, bytes received: {len(audio_data)}")
    else:
        client.logger.error(f"Failed to generate audio file")

except Exception as e:
    print(f"An error occurred reading file: {str(e)}")



