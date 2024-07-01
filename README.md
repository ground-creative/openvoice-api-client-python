# PYTHON OPENVOICE API CLIENT

Python client for OpenVoice api<br />
https://github.com/ground-creative/openvoice-api-python.git

## Installation

Install with pip
```
pip install git+https://github.com/ground-creative/openvoice-api-client-python.git
```

## Usage

```
client = OpenVoiceApiClient()

url, status_code, message = client.generate_audio(
    version=VERSION,
    model='en',
    input='Hello, this is a test. I am here, there and everywhere',
    speed=1.0,
    response_format='url'
)

if status_code == 200:
    client.logger.info(f"URL received: {url}")
else:
    client.logger.error(f"Failed to generate audio url: {message}")
```
View examples folder for more examples