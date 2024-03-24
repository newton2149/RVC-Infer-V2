import json



def test_stream_wav():
    # Update the URL with the appropriate host and port
    import requests

    # Define the URL of the FastAPI endpoint
    url = "http://127.0.0.1:8000/infer/english"

    # Define the JSON data to be sent
    data = {
        "f0up_key": 0,
        "filter_radius": 3,
        "index_rate": 0.0,
        "rms_mix_rate": 1,
        "protect": 0.33,
        "hop_length": 128,
        "f0method": "rmvpe",
        "split_audio": True,
        "f0autotune": True,
        "clean_audio": True,
        "clean_strength": 0.7,
        "export_format": "WAV"
    }

    # Define the path to the audio file to be uploaded
    file_path = "/home/navneeth/EgoPro/dnn/RVC_CLI/test-wavs/LJ001-0001.wav"

    # Create a dictionary with the data and file to be sent
    files = {
        "data": (None, json.dumps(data), "application/json"),
        "file": ("file.wav", open(file_path, "rb"), "audio/x-wav")
    }

    # Send the POST request
    response = requests.post(url, files=files)



    if response.status_code == 200:
        with open("streamed_audio2.wav", "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print("WAV file streamed successfully and saved as 'streamed_audio.wav'")
    else:
        print("Failed to stream WAV file:", response.status_code)


# Call the function to test the streaming endpoint
test_stream_wav()
