import logging
import sys
import os
import asyncio
import aiofiles
from dotenv import load_dotenv

load_dotenv()

# Required for the example
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from openvoice_api_client.client_async import OpenVoiceApiClientAsync

API_URL = os.getenv("API_URL", "http://localhost:5000")
VERSION = 'v2'

async def main():
    output_file = 'outputs/generated_audio_bytes_as_base64_async.wav'
    
    if os.path.exists(output_file):
        os.remove(output_file)

    # Create an instance of OpenVoiceApiClientAsync with DEBUG log level
    client = OpenVoiceApiClientAsync(base_url=API_URL, log_level=logging.DEBUG)

    try:
        # Example generate_audio call
        audio_bytes, status_code, response_message = await client.generate_audio(
            version=VERSION,
            model='en',
            input='Hello, this is a test. I am here, there and everywhere',
            speed=1.0,
            response_format='base64',
        )

        if status_code == 200:
            # Write the generated audio bytes to a file asynchronously
            async with aiofiles.open(output_file, mode='wb') as audio_file:
                await audio_file.write(audio_bytes)
            client.logger.info(f"Audio file saved successfully, bytes received: {len(audio_bytes)}")
        else:
            client.logger.error(f"Failed to generate audio: {len(audio_bytes)}")

    except Exception as e:
        print(f"An error occurred writing file: {e}")

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
