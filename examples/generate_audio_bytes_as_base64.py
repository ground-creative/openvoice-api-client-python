import logging
import sys
import os
import base64
from dotenv import load_dotenv

load_dotenv()

# Required for the example
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from openvoice_api_client.client import OpenVoiceApiClient

# logging.basicConfig(level=logging.DEBUG)  # Set the root logger level to DEBUG

API_URL = os.getenv("API_URL", "http://localhost:5000")
VERSION = "v2"

# Create an instance of OpenVoiceApiClient with DEBUG log level
client = OpenVoiceApiClient(base_url=API_URL, log_level=logging.DEBUG)
output_file = "outputs/generated_audio_bytes_as_base64.wav"
if os.path.exists(output_file):
    os.remove(output_file)

try:
    # Example generate_audio call
    audio_base64, status_code, response_message = client.generate_audio(
        version=VERSION,
        model="en",
        input="Hello, this is a test. I am here, there and everywhere",
        speed=1.0,
        # speaker='kaiwen',
        # style='excited', # only v1
        # accent='en-au', # only v2
        response_format="base64",
    )
    if status_code == 200:
        audio_bytes = base64.b64decode(audio_base64)
        with open(output_file, "wb") as audio_file:
            audio_file.write(audio_bytes)
        client.logger.info(
            f"Audio file saved successfully, bytes received: {len(audio_bytes)}"
        )
    else:
        client.logger.error(f"Failed to generate audio: {len(audio_base64)}")
except Exception as e:
    print(f"An error occurred writing file: {e}")
