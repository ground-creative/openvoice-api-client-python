import logging
import aiohttp
import aiofiles
import os
import json
import base64
import traceback

class OpenVoiceApiClientAsync:
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
    
    async def generate_audio(self, version='v2', model='en', input='', voice='raw', speed=1.0, response_format='url', style=None, accent=None, output_file=None):
        url = f'{self.base_url}/{version}/generate-audio'
        payload = {
            'model': model,
            'input': input,
            'speed': speed,
            'response_format': response_format,
            'voice': voice
        }
        
        if style:
            payload['style'] = style
        
        if accent:
            payload['accent'] = accent
        
        try:
            self.logger.debug(f" > Starting request: {url} with params: {json.dumps(payload, indent=4)}")

            async with aiohttp.ClientSession() as client:
                response = await client.post(url, json=payload)
                return await self._handle_response(response, response_format, output_file)
        
        except Exception as e:
            self.logger.error(f" > An unexpected error occurred: {type(e).__name__}: {str(e)}")
            if self.logger.getEffectiveLevel() == logging.DEBUG:
                self.logger.error(traceback.format_exc())
            return None, 500, "Internal Server Error"
        
    async def change_voice(self, voice, audio_data=None, audio_file=None, version='v2', model='en', response_format='url', accent=None, output_file=None, encode=False):
        
        if audio_file:
            try:
                async with aiofiles.open(audio_file, 'rb') as audio:
                    audio_bytes = await audio.read()
                    audio_data = base64.b64encode(audio_bytes).decode('utf-8')
            except Exception as e:
                self.logger.error(f" > An unexpected error occurred: {type(e).__name__}: {str(e)}")
                if self.logger.getEffectiveLevel() == logging.DEBUG:
                    self.logger.error(traceback.format_exc())
                return None, 500, "Internal Server Error"
        
        elif encode:
            audio_bytes = base64.b64encode(audio_data).decode('utf-8')
            audio_data = audio_bytes
        
        url = f'{self.base_url}/{version}/change-voice'
        payload = {
            'model': model,
            'response_format': response_format,
            'voice': voice,
            'audio_data': audio_data
        }
        
        if accent:
            payload['accent'] = accent
        
        try:
            self.logger.debug(f" > Starting request:\n{url}\nparams:\n {json.dumps(payload, indent=4)}")
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    return await self._handle_response(response, response_format, output_file)
        
        except Exception as e:
            self.logger.error(f" > An unexpected error occurred: {type(e).__name__}: {str(e)}")
            if self.logger.getEffectiveLevel() == logging.DEBUG:
                self.logger.error(traceback.format_exc())
            return None, 500, "Internal Server Error"

    async def _handle_response(self, response, response_format, output_file):
        status_code = response.status
        
        if status_code == 200:
            
            if response_format == 'url':
                response_data = await response.json()
                file_url = response_data['result']['data']['url']
                response_message = response_data['result']['message']
                self.logger.debug(f" > Generated audio URL: {file_url}")
                return file_url, status_code, response_message
            
            elif response_format == 'bytes' or response_format == 'base64':
                
                if output_file is not None:
                    
                    if response_format == 'base64':
                        response_data = await response.json()
                        audio_base64 = response_data['result']['data']['audio_data']
                        audio_bytes = base64.b64decode(audio_base64)
                    else:
                        audio_bytes = await response.read()
                    
                    async with aiofiles.open(output_file, 'wb') as audio_file:
                        await audio_file.write(audio_bytes)

                    return output_file, status_code, "Generated audio bytes and saved to file"
                
                else:
                    
                    if response_format == 'base64':
                        response_data = await response.json()
                        audio_base64 = response_data['result']['data']['audio_data']
                        audio_bytes = base64.b64decode(audio_base64)
                    else:
                        audio_bytes = await response.read()
                    
                    return audio_bytes, status_code, "Generated audio bytes"
            
            elif response_format == 'stream':
                return response, status_code, "Generated audio stream"
        
        else:
            response_data = await response.json()
            response_message = response_data['data']['message']
            self.logger.error(f" > Failed to generate audio. Response status code: {status_code}, Response message: {response_message}")
            return None, status_code, response_message

    async def async_stream_generator(self, output_file, response):
        self.logger.debug(" > Starting streaming and writing to file...")
        try:
            async with aiofiles.open(output_file, 'wb') as audio_file:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    await audio_file.write(chunk)
        except Exception as e:
            self.logger.error(f"Error during streaming: {e}")
            if self.logger.getEffectiveLevel() == logging.DEBUG:
                    self.logger.error(traceback.format_exc())
        else:
            self.logger.debug(" > Streaming and writing completed.")
