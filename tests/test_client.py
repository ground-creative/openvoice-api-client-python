import unittest
import sys
import os
import base64
import asyncio
from unittest import TestCase, mock
from unittest.mock import patch, mock_open, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from openvoice_api_client.client import OpenVoiceApiClient

class TestClient(unittest.TestCase):
    def setUp(self):
        # Initialize OpenVoiceApiClient with mock base_url (replace with your actual base_url if needed)
        self.client = OpenVoiceApiClient()
    
    def test_generate_audio_url(self):
        # Mock response data
        mock_response_data = {
            'result': {
                'data': {
                    'url': 'http://example.com/audio.wav',
                },
                'message': 'Audio file generated successfully'
            }
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        
        # Mock requests.post to return the mock response
        with patch('requests.post', return_value=mock_response) as mock_post:
            url, status_code, message = self.client.generate_audio(
                version='v2',
                model='en',
                input='Hello, this is a test. I am here there and everywhere.',
                voice='kaiwen',
                response_format='url'
            )
            # Assertions
            self.assertEqual(status_code, 200)
            self.assertEqual(url, 'http://example.com/audio.wav')
            self.assertEqual(message, 'Audio file generated successfully')
            mock_post.assert_called_once()  # Ensure requests.post was called exactly once
            
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize', return_value=12345)  # Mock file size to avoid FileNotFoundError
    @patch('requests.post')
    def test_generate_audio_bytes(self, mock_post, mock_getsize, mock_open):
        # Mock response data for successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'audio_bytes_content'  # Mock audio bytes content
        mock_post.return_value = mock_response

        output_file = 'generate_audio_bytes.wav'
        audio_file, status_code, message = self.client.generate_audio(
            version='v2',
            model='en',
            input='Hello, this is a test',
            voice='kaiwen',
            response_format='bytes',
            output_file=output_file
        )

        # Assertions
        self.assertEqual(status_code, 200)  # Verify status code for successful response
        self.assertEqual(audio_file, output_file)  # Verify that output_file path is returned
        mock_open.assert_called_once_with(output_file, 'wb')  # Ensure open was called with output_file
        mock_open().write.assert_called_once_with(b'audio_bytes_content')  # Ensure write was called with audio content
        mock_getsize.assert_called_once_with(output_file)  # Ensure getsize was called

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize', return_value=12345)  # Mock file size to avoid FileNotFoundError
    @patch('requests.post')
    def test_generate_audio_bytes_as_bytes(self, mock_post, mock_getsize, mock_open):
        # Mock response data for successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'audio_bytes_content'  # Mock audio bytes content
        mock_post.return_value = mock_response

        audio_bytes, status_code, message = self.client.generate_audio(
            version='v2',
            model='en',
            input='Hello, this is a test',
            voice='kaiwen',
            response_format='bytes'
        )

        # Assertions
        self.assertEqual(status_code, 200)  # Verify status code for successful response
        self.assertEqual(type(audio_bytes), bytes)  # Verify that audio_bytes is of type bytes
        mock_open.assert_not_called()  # Ensure open was not called
        mock_getsize.assert_not_called()  # Ensure getsize was not called
        
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize', return_value=12345)  # Mock file size to avoid FileNotFoundError
    @patch('requests.post')
    def test_generate_audio_base64(self, mock_post, mock_getsize, mock_open):
        # Mock response data for successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'result': {
                'data': {
                    'audio_data': base64.b64encode(b'audio_bytes_content').decode('utf-8')
                }
            }
        }
        mock_post.return_value = mock_response

        output_file = 'generate_audio_base64.wav'
        audio_file, status_code, message = self.client.generate_audio(
            version='v2',
            model='en',
            input='Hello, this is a test',
            voice='kaiwen',
            response_format='base64',
            output_file=output_file
        )
        
        # Assertions
        self.assertEqual(status_code, 200)  # Verify status code for successful response
        self.assertEqual(audio_file, output_file)  # Verify that output_file path is returned
        mock_open.assert_called_once_with(output_file, 'wb')  # Ensure open was called with output_file
        
        # Decode base64 and compare
        called_args = mock_open().write.call_args[0][0]  # Get the arguments written to mock_open
        #decoded_audio_bytes = base64.b64decode(called_args)
        #self.assertEqual(decoded_audio_bytes, b'audio_bytes_content')
        self.assertEqual(called_args, b'audio_bytes_content')
        
        mock_getsize.assert_called_once_with(output_file)  # Ensure getsize was called

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize', return_value=12345)  # Mock file size to avoid FileNotFoundError
    @patch('requests.post')
    def test_generate_audio_bytes_as_base64(self, mock_post, mock_getsize, mock_open):
        # Mock response data for successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'result': {
                'data': {
                    'audio_data': base64.b64encode(b'audio_bytes_content').decode('utf-8')
                }
            }
        }
        mock_post.return_value = mock_response

        audio_bytes, status_code, message = self.client.generate_audio(
            version='v2',
            model='en',
            input='Hello, this is a test',
            voice='kaiwen',
            response_format='base64'
        )

        # Assertions
        self.assertEqual(status_code, 200)  # Verify status code for successful response
        self.assertEqual(type(audio_bytes), bytes)  # Verify that audio_bytes is of type bytes
        mock_open.assert_not_called()  # Ensure open was not called
        mock_getsize.assert_not_called()  # Ensure getsize was not called

    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.post')
    def test_change_voice(self, mock_post, mock_open):
        # Mock response data for successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'changed_audio_bytes_content'  # Mock audio bytes content
        mock_post.return_value = mock_response

        audio_file = 'test_audio_file.wav'
        mock_open().read.return_value = b'fake audio content'

        # Mock the base64 encoding process
        encoded_audio_data = base64.b64encode(b'fake audio content').decode('utf-8')

        audio_bytes, status_code, message = self.client.change_voice(
            audio_data=encoded_audio_data,
            voice='elon',
            response_format='bytes'
        )

        # Assertions
        self.assertEqual(status_code, 200)  # Verify status code for successful response
        self.assertEqual(type(audio_bytes), bytes)  # Verify that audio_bytes is of type bytes
        mock_post.assert_called_once()  # Ensure post was called once

        # Clean up
        if os.path.exists(audio_file):
            os.remove(audio_file)

    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.post')
    def test_change_voice_encode_param(self, mock_post, mock_open):
        # Mock response data for successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'changed_audio_bytes_content'  # Mock audio bytes content
        mock_post.return_value = mock_response

        audio_file = 'test_audio_file.wav'
        mock_open().read.return_value = b'fake audio content'

        # Mock the base64 encoding process
        audio_data = b'fake audio content'

        audio_bytes, status_code, message = self.client.change_voice(
            audio_data=audio_data,
            voice='elon',
            encode=True,
            response_format='bytes'
        )

        # Assertions
        self.assertEqual(status_code, 200)  # Verify status code for successful response
        self.assertEqual(type(audio_bytes), bytes)  # Verify that audio_bytes is of type bytes
        mock_post.assert_called_once()  # Ensure post was called once

        # Clean up
        if os.path.exists(audio_file):
            os.remove(audio_file)

    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.post')
    def test_change_voice_audio_file_param(self, mock_post, mock_open):
        # Mock response data for successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'changed_audio_bytes_content'  # Mock audio bytes content
        mock_post.return_value = mock_response

        audio_file = 'test_audio_file.wav'
        mock_open().read.return_value = b'fake audio content'

        audio_bytes, status_code, message = self.client.change_voice(
            audio_file=audio_file,
            voice='elon',
            encode=True,
            response_format='bytes'
        )

        # Assertions
        self.assertEqual(status_code, 200)  # Verify status code for successful response
        self.assertEqual(type(audio_bytes), bytes)  # Verify that audio_bytes is of type bytes
        mock_post.assert_called_once()  # Ensure post was called once

        # Clean up
        if os.path.exists(audio_file):
            os.remove(audio_file)

    def test_generate_audio_error(self):
        # Mock requests.post to raise an exception
        with patch('requests.post', side_effect=Exception('Test exception')):
            url, status_code, message = self.client.generate_audio(
                version='v2',
                model='en',
                input='Hello, this is a test',
                voice='kaiwen',
                response_format='url'
            )

            # Assertions
            self.assertEqual(status_code, 500)
            self.assertIsNone(url)
            self.assertEqual(message, 'Internal Server Error')

    def test_generate_audio_bad_request(self):
        # Mock response data for bad request
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'result': {
                'data': {},
                'message': 'Bad Request'
            }
        }

        # Mock requests.post to return the mock response
        with patch('requests.post', return_value=mock_response):
            url, status_code, message = self.client.generate_audio(
                version='v2',
                model='en',
                input='Hello, this is a test',
                voice='kaiwen',
                response_format='url'
            )
            
            # Assertions
            self.assertEqual(status_code, 400)
            self.assertIsNone(url)
            self.assertEqual(message, 'Bad Request')


if __name__ == '__main__':
    unittest.main()

