import aiohttp
import requests
import os
import logging
import json
import asyncio
import aiofiles
import base64
import traceback

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
    
    def generate_audio(self, version='v2', language='en', text='', speaker='raw', speed=1.0, response_format='url', style=None, accent=None, output_file=None, async_mode=False, encode=False):
        if async_mode:
            return self._generate_audio_async(version, language, text, speaker, speed, response_format, style, accent, output_file, encode)
        else:
            return self._generate_audio_sync(version, language, text, speaker, speed, response_format, style, accent, output_file, encode)
    
    def _generate_audio_sync(self, version, language, text, speaker, speed, response_format, style, accent, output_file, encode):
        url = f'{self.base_url}/generate-audio/{version}/'
        payload = {
            'language': language,
            'text': text,
            'speed': speed,
            'response_format': response_format,
            'speaker': speaker,
            'encode': encode
        }
        
        if style:
            payload['style'] = style
        
        if accent:
            payload['accent'] = accent
        
        try:
            self.logger.debug(f" > Starting request: {url} with params: {json.dumps(payload, indent=4)}")
            
            response = requests.post(url, json=payload)
            return self._handle_response(response, response_format, output_file, encode)
        
        except Exception as e:
            self.logger.error(f" > An unexpected error occurred: {type(e).__name__}: {str(e)}")
            return None, 500, "Internal Server Error"

    async def _generate_audio_async(self, version, language, text, speaker, speed, response_format, style, accent, output_file, encode):
        url = f'{self.base_url}/generate-audio/{version}/'
        payload = {
            'language': language,
            'text': text,
            'speed': speed,
            'response_format': response_format,
            'speaker': speaker,
            'encode': encode
        }
        
        if style:
            payload['style'] = style
        
        if accent:
            payload['accent'] = accent
        
        try:
            self.logger.debug(f" > Starting request: {url} with params: {json.dumps(payload, indent=4)}")

            async with aiohttp.ClientSession() as client:
                response = await client.post(url, json=payload)
                return await self._handle_response_async(response, response_format, output_file, encode)
        
        except Exception as e:
            self.logger.error(f" > An unexpected error occurred: {type(e).__name__}: {str(e)}")
            #self.logger.error(traceback.format_exc())
            return None, 500, "Internal Server Error"

    def _handle_response(self, response, response_format, output_file, encode):
        status_code = response.status_code
        if status_code == 200:
            if response_format == 'url':
                response_data = response.json()
                file_url = response_data['data']['url']
                response_message = response_data['data']['message']
                self.logger.debug(f" > Generated audio URL: {file_url}")
                return file_url, status_code, response_message
            elif response_format == 'bytes':
                if output_file is not None:
                    audio_bytes = response.content
                    if encode == True:
                        audio_bytes = base64.b64decode(response.content)
                    with open(output_file, 'wb') as audio_file:
                        audio_file.write(audio_bytes)
                    file_size = os.path.getsize(output_file)
                    self.logger.debug(f" > Saved generated audio bytes: {file_size}")
                    return output_file, status_code, "Generated audio bytes and saved to file"
                else:
                    audio_bytes = response.content
                    if encode == True:
                        audio_bytes = base64.b64decode(response.content)
                    return audio_bytes, status_code, "Generated audio bytes"
        else:
            response_data = response.json()
            response_message = response_data['data']['message']
            self.logger.error(f" > Failed to generate audio. Response status code: {status_code}, Response message: {response_message}")
            return None, status_code, response_message

    async def _handle_response_async(self, response, response_format, output_file, encode):
        status_code = response.status
        if status_code == 200:
            if response_format == 'url':
                response_data = response.json()
                file_url = response_data['data']['url']
                response_message = response_data['data']['message']
                self.logger.debug(f" > Generated audio URL: {file_url}")
                return file_url, status_code, response_message
            elif response_format == 'bytes':
                if output_file is not None:
                    async with aiofiles.open(output_file, 'wb') as audio_file:
                        while True:
                            chunk = await response.content.read(1024)
                            if encode == True:
                                audio_bytes = base64.b64decode(chunk)
                                chunk = audio_bytes
                            if not chunk:
                                break
                            await audio_file.write(chunk)
                    file_size = os.path.getsize(output_file)
                    self.logger.debug(f" > Saved generated audio bytes: {file_size}")
                    return output_file, status_code, "Generated audio bytes and saved to file"
                else:
                    audio_data = await response.read()
                    if encode == True:
                        audio_bytes = base64.b64decode(audio_data)
                        audio_data = audio_bytes
                    return audio_data, status_code, "Generated audio bytes"
        else:
            response_data = response.json()
            response_message = response_data['data']['message']
            self.logger.error(f" > Failed to generate audio. Response status code: {status_code}, Response message: {response_message}")
            return None, status_code, response_message

async def stream_generator(output_file, response):
    async with open(output_file, 'wb') as audio_file:
        async for chunk in response.aiter_bytes():
            if chunk:
                await audio_file.write(chunk)
                yield chunk
