import unittest
import sys
import os
import base64
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
            'data': {
                'url': 'http://example.com/audio.wav',
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
                language='en',
                text='Hello, this is a test. I am here there and everywhere.',
                speaker='kaiwen',
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
            language='en',
            text='Hello, this is a test',
            speaker='kaiwen',
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
            language='en',
            text='Hello, this is a test',
            speaker='kaiwen',
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
    def test_generate_audio_bytes_with_encode(self, mock_post, mock_getsize, mock_open):
        # Mock response data for successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = base64.b64encode(b'audio_bytes_content') 
        mock_post.return_value = mock_response

        output_file = 'generate_audio_bytes.wav'
        audio_file, status_code, message = self.client.generate_audio(
            version='v2',
            language='en',
            text='Hello, this is a test',
            speaker='kaiwen',
            response_format='bytes',
            output_file=output_file,
            encode=True # Base64 encode the audio bytes
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
    def test_generate_audio_bytes_as_bytes_with_encode(self, mock_post, mock_getsize, mock_open):
        # Mock response data for successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = base64.b64encode(b'audio_bytes_content') 
        mock_post.return_value = mock_response

        # Call generate_audio with response_format='bytes' and encode=True
        audio_bytes_base64, status_code, message = self.client.generate_audio(
            version='v2',
            language='en',
            text='Hello, this is a test',
            speaker='kaiwen',
            response_format='bytes',
            encode=True # Base64 encode the audio bytes
        )

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(audio_bytes_base64, b'audio_bytes_content')
        mock_open.assert_not_called()
        mock_getsize.assert_not_called()

    def test_generate_audio_error(self):
        # Mock requests.post to raise an exception
        with patch('requests.post', side_effect=Exception('Test exception')):
            url, status_code, message = self.client.generate_audio(
                version='v2',
                language='en',
                text='Hello, this is a test',
                speaker='kaiwen',
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
            'data': {'message': 'Bad Request'}
        }

        # Mock requests.post to return the mock response
        with patch('requests.post', return_value=mock_response):
            url, status_code, message = self.client.generate_audio(
                version='v2',
                language='en',
                text='Hello, this is a test',
                speaker='kaiwen',
                response_format='url'
            )

            # Assertions
            self.assertEqual(status_code, 400)
            self.assertIsNone(url)
            self.assertEqual(message, 'Bad Request')


if __name__ == '__main__':
    unittest.main()

