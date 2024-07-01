import logging
import sys
import os
import asyncio
from dotenv import load_dotenv

import traceback

load_dotenv()

# Required for the example
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from openvoice_api_client.client_async import OpenVoiceApiClientAsync  # Assuming asynchronous version is implemented in client_async module

#logging.basicConfig(level=logging.DEBUG)  # Set the root logger level to DEBUG

API_URL = os.getenv("API_URL", "http://localhost:5000")
VERSION = 'v2'
    
async def main():
    try:
        # Create an instance of OpenVoiceApiClientAsync with DEBUG log level
        client = OpenVoiceApiClientAsync(base_url=API_URL, log_level=logging.DEBUG)

        # Example generate_audio call
        audio_data, status_code, response_message = await client.generate_audio(
            version=VERSION,
            model='en',
            input='Hello, this is a test. I am here, there and everywhere',
            speed=1.0,
            voice='raw',
            response_format='base64'
        )

        if status_code == 200:
            url, status_code, response_message = await client.change_voice(
                audio_data=audio_data,
                encode=True,
                voice='elon',
                response_format='url'
            )
            if status_code == 200:
                client.logger.info(f"Audio data generated successfully, url: {url}")
            else:
                client.logger.error(f"Failed to generate audio data")

        else:
            client.logger.error(f"Failed to generate audio data")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(traceback.format_exc())


# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
