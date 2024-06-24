import logging
import sys
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Required for the example
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from openvoice_api_client.client import OpenVoiceApiClient

API_URL = os.getenv("API_URL", "http://localhost:5000")
VERSION = 'v2'
output_file='outputs/generated_audio_bytes_async.wav'

# Create an instance of OpenVoiceApiClient with DEBUG log level
client = OpenVoiceApiClient(base_url=API_URL, log_level=logging.DEBUG)

async def main():
    try:
        # Example generate_audio call
        audio_file, status_code, response_message = await client.generate_audio(
            version=VERSION,
            language='en',
            text='Hello, this is a test. I am here, there and everywhere',
            speed=1.0,
            speaker='elon',
            #style='excited', # only v1
            #accent='en-au', # only v2
            response_format='bytes',
            output_file=output_file,
            async_mode=True,
            encode=True
        )

        if status_code == 200:
            with open(audio_file, 'rb') as audio_file:
                audio_data = audio_file.read()
            client.logger.info(f"Audio file saved successfully, bytes received: {len(audio_data)}")
        else:
            client.logger.error(f"Failed to generate audio file")

    except Exception as e:
        client.logger.error(f"An error occurred: {str(e)}")

# Run the async main function
asyncio.run(main())
