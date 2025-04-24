import runpod
import torch
import soundfile as sf
import io
import base64
from typing import Optional
from dia.model import Dia
from dia.config import DiaConfig

# Initialize model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = None

def load_model():
    global model
    if model is None:
        config = DiaConfig()
        model = Dia.from_pretrained("nari-labs/Dia-1.6B")
        model.to(device)

def handler(event):
    try:
        # Load model if not already loaded
        load_model()
        
        # Get input parameters
        input = event['input']
        text = input.get('text')
        audio_prompt_path = input.get('audio_prompt_path')
        temperature = input.get('temperature', 1.0)
        top_p = input.get('top_p', 1.0)
        
        # Validate input
        if not text:
            return {
                "error": "Text parameter is required"
            }
        
        # Generate audio
        output = model.generate(
            text,
            audio_prompt_path=audio_prompt_path,
            temperature=temperature,
            top_p=top_p
        )
        
        # Convert audio to bytes
        audio_bytes = io.BytesIO()
        sf.write(audio_bytes, output, 44100, format='WAV')
        audio_bytes.seek(0)
        
        # Convert to base64 for transmission
        audio_base64 = base64.b64encode(audio_bytes.read()).decode('utf-8')
        
        return {
            "audio": audio_base64,
            "sample_rate": 44100,
            "format": "wav"
        }
        
    except Exception as e:
        return {
            "error": str(e)
        }

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
