import logging
import sys
import os
import asyncio
from dotenv import load_dotenv

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

        # Clean up existing files if they exist
        audio_file='outputs/change_voice_generate_audio_audio_file_input_async.wav'
        if os.path.exists(audio_file):
            os.remove(audio_file)
        output_file='outputs/change_voice_generate_audio_audio_file_async.wav'
        if os.path.exists(output_file):
            os.remove(output_file)

        # Example generate_audio call
        audio_data, status_code, response_message = await client.generate_audio(
            version=VERSION,
            model='en',
            input='Hello, this is a test. I am here, there and everywhere',
            speed=1.0,
            voice='raw',
            response_format='bytes',
            output_file=audio_file
        )

        if status_code == 200:
            audio_bytes, status_code, response_message = await client.change_voice(
                audio_file=audio_file,
                encode=True,
                output_file=output_file,
                voice='elon',
                response_format='bytes'
            )
            if status_code == 200:
                client.logger.info(f"Audio data generated successfully, bytes: {len(audio_bytes)}")
            else:
                client.logger.error(f"Failed to generate audio data")

        else:
            client.logger.error(f"Failed to generate audio data")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
