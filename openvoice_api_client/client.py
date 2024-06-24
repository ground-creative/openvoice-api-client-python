# openvoice_api_client.py

import requests
import os
import logging
import json
import traceback
import threading

class OpenVoiceApiClient:
    def __init__(self, base_url='http://localhost:5000', log_level=None, log_format=None):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        self._configure_logging(log_level, log_format)
    
    def _configure_logging(self, log_level, log_format):
        if log_level:
            self.logger.setLevel(log_level)
        else:
            # Use the application's default logging level if custom level is not provided
            app_log_level = logging.getLogger().getEffectiveLevel()
            self.logger.setLevel(app_log_level)
        
        if not log_format:
            log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(log_format)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
    
    def generate_audio(self, version='v2', language='en', text='', speaker='raw', speed=1.0, response_format='url', style=None, accent=None, output_file=None):
        url = f'{self.base_url}/generate-audio/{version}/'
        payload = {
            'language': language,
            'text': text,
            'speed': speed,
            'response_format': response_format,
            'speaker': speaker,
        }
        
        if style:
            payload['style'] = style
        
        if accent:
            payload['accent'] = accent
        
        try:
            self.logger.debug(f" > Starting request: {url} with params: {json.dumps(payload, indent=4)}")
            
            if response_format == 'stream':
                response = requests.post(url, json=payload, stream=True)
            else:
                response = requests.post(url, json=payload)
                
            status_code = response.status_code
            
            if status_code == 200:
                if response_format == 'url':
                    response_data = response.json()
                    file_url = response_data['data']['url']
                    response_message = response_data['data']['message']
                    self.logger.debug(f" > Generated audio URL: {file_url}")
                    return file_url, status_code, response_message
                elif response_format == 'bytes':
                    with open(output_file, 'wb') as audio_file:
                        audio_file.write(response.content)
                    file_size = os.path.getsize(output_file)
                    self.logger.debug(f" > Saved generated audio bytes: {file_size}")
                    return output_file, status_code, None
                elif response_format == 'stream':
                    def run_generator():
                        generator = stream_generator(output_file, response)
                        for chunk in generator:
                            # Process each chunk as needed
                            pass
                    thread = threading.Thread(target=run_generator)
                    return thread.start(), status_code, "Streaming started"

            else:
                response_data = response.json()
                response_message = response_data['data']['message']
                self.logger.error(f" > Failed to generate audio URL. Response status code: {status_code}, Response message: {response_message}")
                return None, status_code, response_message
        
        except Exception as e:
            self.logger.error(f" > An unexpected error occurred: {type(e).__name__}: {str(e)}")
            #traceback.print_exc()  # Print detailed traceback
            return None, 500, "Internal Server Error"


def stream_generator(output_file, response):
    with open(output_file, 'wb') as audio_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                audio_file.write(chunk)
                yield chunk
            
