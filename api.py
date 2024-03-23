from fastapi import FastAPI,HTTPException,Response,status,WebSocket
import time
import os
from inferV2 import run_batch_infer_script,run_infer_script
from trainv2 import run_preprocess_script,run_extract_script,run_train_script,run_index_script
from model import TrainInputData,IndexInputData,PreprocessInputData,ExtractInputData,InputData , BatchInputData,InputRequest,BatchRequest,TrainRequest
from fastapi.responses import StreamingResponse
import shutil
import random

import requests
from fastapi import HTTPException
from fastapi.responses import FileResponse

import random
import zipfile
import shutil
from tqdm import tqdm 



model_map = {
    'english':"./logs/models/weights/lj-ten.pth",
    'french':"./logs/models/weights/fr-mlb.pth"
}

pretrained_map = {
    'd':"./rvc/pretraineds/pretrained_v2/D48k.pth",
    'g':"./rvc/pretraineds/pretrained_v2/G48k.pth"
  
}
def clear_output_folder():
    shutil.rmtree("output", ignore_errors=True)
    
    
def zip_wav_files(input_dir, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, _, files in os.walk(input_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, input_dir)
                zipf.write(file_path, arcname=arcname)

def download_file_from_firebase_storage(download_url, output_file_path):
    print("Downloading file...")
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

app = FastAPI(
    title="RVC_API",
    version="1.0",
    description="API for RVC",
    docs_url="/docs",
    
)
os.makedirs("output", exist_ok=True)

@app.post("/infer/{lang}")
async def infer(lang: str, data: InputRequest):
    
        
    os.makedirs("output", exist_ok=True)
    os.makedirs("temp_db/download", exist_ok=True)
    
    
    data = InputData(**data.model_dump())
    
    data.pth_path = model_map[lang]
    data.index_path = model_map[lang]
    data.output_path = f'./output/{random.randint(0, 1000)}.wav'
    
    local_path = f'./temp_db/download/{random.randint(0, 100000)}.wav'
    download_file_from_firebase_storage(data.input_path,local_path)
    data.input_path = local_path
    
    run_script(run_infer_script, data)
    
    if not os.path.exists(data.output_path):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    def stream_file():
        with open(data.output_path, "rb") as file:
            while True:
                chunk = file.read(65536)  # Read 64 KB chunks
                if not chunk:
                    break
                yield chunk
    
    response = StreamingResponse(stream_file(), media_type="audio/wav")
    
    shutil.rmtree('./temp_db/download/')
    
    return response

# Batch Infer
@app.post("/batch_infer/{lang}")
async def batch_infer(lang:str, data: BatchRequest):
    
    os.makedirs("output", exist_ok=True)
    os.makedirs("temp_db/download", exist_ok=True)
    
    
    data = BatchInputData(**data.model_dump())
    data.pth_path = model_map[lang]
    data.index_path = model_map[lang]
    data.output_folder = f'./output/{random.randint(0, 1000)}_batch/'
    
    local_path = f'./temp_db/download/{random.randint(0, 100000)}.zip'
        
    download_file_from_firebase_storage(data.input_folder,local_path)
    
    data.input_folder = extract_zip(local_path)
    os.makedirs(data.output_folder, exist_ok=True)
    
    run_script(run_batch_infer_script, data)
    
    zip_path = f"./output/generated_{random.randint(0, 100000)}.zip"
    
    zip_wav_files(data.output_folder, zip_path)
        
    
    shutil.rmtree(data.input_folder)
    shutil.rmtree(data.output_folder)
    os.remove(local_path)
    
    return FileResponse(zip_path, media_type="application/zip", filename="generated.zip")
    
    

# Preprocess
@app.post("/preprocess")
async def preprocess(data: PreprocessInputData):
    label = random.randint(0, 1000)
    local_path = f"./train_db/dataset/{label}_data.zip"
    download_file_from_firebase_storage(data.dataset_path,local_path)
    
    data.dataset_path = extract_zip(local_path, f'train_db/dataset/{label}')
    
    
    return run_script(run_preprocess_script, data)

# Extract
@app.post("/extract")
async def extract(data: ExtractInputData):
    return run_script(run_extract_script, data)

# Train
@app.post("/train")
async def train(data: TrainRequest):
    data = TrainInputData(**data.model_dump())
    data.d_pretrained_path = pretrained_map['d']
    data.g_pretrained_path = pretrained_map['g']
    
    return run_script(run_train_script, data)

# Index
@app.post("/index")
async def index(data: IndexInputData):
    return run_script(run_index_script, data)


# Ping endpoint to check latency
@app.get("/ping")
async def ping():
    start_time = time.time()
    end_time = time.time()
    latency = end_time - start_time
    return {"ping": "pong", "latency": latency}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1",port=8000)