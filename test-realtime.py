import asyncio
import websockets
import json



import requests

def test_stream_wav():
    url = "http://localhost:8000/infer/english"  # Update the URL with the appropriate host and port
    
    input_data = {
            "f0up_key": 0,
            "filter_radius": 3,
            "index_rate": 0.0,
            "rms_mix_rate": 1,
            "protect": 0.33,
            "hop_length": 128,
            "f0method": "rmvpe",
            "input_path": "https://firebasestorage.googleapis.com/v0/b/intenrship-e76b3.appspot.com/o/LJ001-0001.wav?alt=media&token=37bf871f-f2f2-4807-a37f-b5f297151877",
            "split_audio": True,
            "f0autotune": True,
            "clean_audio": True,
            "clean_strength": 0.7,
            "export_format": "WAV"
        }
    response = requests.post(url,json=input_data,stream=True)
    
    if response.status_code == 200:
        with open("streamed_audio2.wav", "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print("WAV file streamed successfully and saved as 'streamed_audio.wav'")
    else:
        print("Failed to stream WAV file:", response.status_code)

# Call the function to test the streaming endpoint
test_stream_wav()
