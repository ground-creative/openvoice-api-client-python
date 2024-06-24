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
    
# Create an instance of OpenVoiceApiClient with DEBUG log level
client = OpenVoiceApiClient(base_url=API_URL, log_level=logging.DEBUG)

async def main():
    # Example generate_audio call
    url, status_code, message = await client.generate_audio(
        version=VERSION,
        language='en',
        text='Hello, this is a test. I am here, there and everywhere',
        speed=1.0,
        #speaker='kaiwen',
        #style='excited', # only v1
        #accent='en-au', # only v2
        response_format='url',
        async_mode=True
    )

    if status_code == 200:
        client.logger.info(f"Audio file saved successfully or URL received: {url}")
    else:
        client.logger.error(f"Failed to generate audio: {message}")

# Run the async main function
asyncio.run(main())
