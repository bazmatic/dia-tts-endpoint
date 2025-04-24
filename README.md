# Dia TTS Serverless Endpoint

A serverless endpoint for generating speech using the [Dia](https://github.com/nari-labs/dia) text-to-speech model. This project provides a simple way to deploy Dia as a serverless endpoint using RunPod.

## Features

- Generate natural-sounding dialogue from text
- Support for multiple speakers using [S1], [S2] tags
- Optional voice cloning using audio prompts
- Configurable generation parameters (temperature, top_p)
- Serverless deployment with RunPod

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/bazmatic/dia-tts-endpoint.git
cd dia-tts-endpoint
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Test locally:
```bash
python rp_handler.py
```

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t dia-tts-endpoint:latest .
```

2. Run the container:
```bash
docker run --gpus all -p 8000:8000 dia-tts-endpoint:latest
```

3. For RunPod deployment:
```bash
docker build -t your-dockerhub-username/dia-tts-endpoint:v1.0.0 --platform linux/amd64 .
docker push your-dockerhub-username/dia-tts-endpoint:v1.0.0
```

## API Usage

### Input Parameters

```json
{
    "input": {
        "text": "Required. The dialogue text to convert to speech. Use [S1] and [S2] tags for different speakers.",
        "audio_prompt_path": "Optional. Path to audio file for voice cloning.",
        "temperature": "Optional. Controls randomness in generation. Default: 1.0",
        "top_p": "Optional. Controls nucleus sampling. Default: 1.0"
    }
}
```

### Output Format

```json
{
    "audio": "Base64 encoded WAV audio data",
    "sample_rate": 44100,
    "format": "wav"
}
```

### Example Usage

```python
import requests
import base64
import soundfile as sf
import io

# Example text with two speakers
text = "[S1] Hello, how are you? [S2] I'm doing great, thank you! [S1] That's wonderful to hear."

# Make request to endpoint
response = requests.post(
    "YOUR_ENDPOINT_URL",
    json={
        "input": {
            "text": text,
            "temperature": 1.0,
            "top_p": 1.0
        }
    }
)

# Decode and save audio
result = response.json()
audio_data = base64.b64decode(result["audio"])
audio_bytes = io.BytesIO(audio_data)
audio, sample_rate = sf.read(audio_bytes)
sf.write("output.wav", audio, sample_rate)
```

## Error Handling

The endpoint returns error messages in the following format:

```json
{
    "error": "Error message description"
}
```

Common errors include:
- Missing required text parameter
- Invalid audio prompt path
- Model loading or generation errors

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Dia](https://github.com/nari-labs/dia) - The text-to-speech model
- [RunPod](https://runpod.io/) - Serverless GPU platform
