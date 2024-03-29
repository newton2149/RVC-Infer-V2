import zipfile
import os
import requests
from tqdm import tqdm
from fastapi import HTTPException

def zip_wav_files(input_dir, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, _, files in os.walk(input_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, input_dir)
                zipf.write(file_path, arcname=arcname)

def download_file_from_firebase_storage(download_url, output_file_path):
    print("Downloading file...")
    print(download_url)
    response = requests.get(download_url, stream=True)  # Set stream=True to download in chunks
    total_size_in_bytes = int(response.headers.get('content-length', 0))  # Total size of the file
    
    # Initialize tqdm with total size of the file
    progress_bar = tqdm(total=total_size_in_bytes, unit='B', unit_scale=True)
    
    if response.status_code == 200:
        with open(output_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):  # Download in 1 KB chunks
                if chunk:
                    f.write(chunk)
                    progress_bar.update(len(chunk))  # Update progress bar with the size of the downloaded chunk
        
        progress_bar.close()  # Close progress bar after download completes
        print("File downloaded successfully.")
    else:
        raise HTTPException(status_code=response.status_code,
                            detail=f"Failed to download file. Status code: {response.status_code}")
        
def extract_zip(zip_file_path, extract_to='inference_db'):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        os.makedirs(extract_to, exist_ok=True)
        zip_ref.extractall(extract_to)
        return os.path.join(extract_to, zip_ref.namelist()[0])
    
    
    
def run_script(script_function, data):
    try:
        result = script_function(**data.dict())
        return {"message": result}

    except ValueError as value_error:
        raise HTTPException(status_code=400, detail=str(value_error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
    
