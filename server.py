from sqlalchemy.exc import OperationalError
import psycopg2
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks, Depends
import time
import os
from inferV2 import run_batch_infer_script, run_infer_script
from trainv2 import run_preprocess_script, run_extract_script, run_train_script, run_index_script
from model import TrainInputData, IndexInputData, PreprocessInputData, ExtractInputData, InputData, BatchInputData, BatchRequest, TrainRequest
from server_utils import zip_wav_files, download_file_from_firebase_storage, extract_zip, run_script
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker,declarative_base
import uuid
from fastapi.responses import StreamingResponse
import shutil
import random
from fastapi import HTTPException
import json
import random
import shutil
import asyncio
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIAL_FILE"))  # Replace with your path
firebase_admin.initialize_app(cred, {
    'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET")  # Replace with your bucket URL
})

# Initialize Google Cloud Storage client
bucket = storage.bucket()


model_map = {
    'english': "./logs/models/weights/lj-ten.pth",
    'french': "./logs/models/weights/fr-mlb.pth"
}

pretrained_map = {
    'd': "./rvc/pretraineds/pretrained_v2/D48k.pth",
    'g': "./rvc/pretraineds/pretrained_v2/G48k.pth"

}


def clear_output_folder():
    shutil.rmtree("output", ignore_errors=True)


# Database configuration
DB_NAME = os.getenv("DB_NAME")
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create database if it doesn't exist
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}';")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {DB_NAME};")
    cur.close()
    conn.close()
except psycopg2.Error as e:
    print("Error creating database:", e)

# Continue with FastAPI initialization
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Job(Base):
    __tablename__ = "RVC_QUEUE"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    data = Column(String)
    status = Column(String)
    result = Column(String, nullable=True)
    date = Column(String, default=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def upload_file_to_firebase_storage(local_file_path, remote_file_path):
    try:

        blob = bucket.blob(remote_file_path)
        blob.upload_from_filename(local_file_path)
        expiration_time = datetime.utcnow() + timedelta(hours=1)

        # Get the download URL
        download_url = blob.generate_signed_url(expiration=expiration_time)

        return download_url

    except Exception as e:
        print("Error uploading file:", e)


async def perform_batch_input(data, lang):
    print(type(data))
    data = BatchInputData(**data.dict())
    data.pth_path = model_map[lang]
    data.index_path = model_map[lang]
    data.output_folder = f'./output/{random.randint(0, 1000)}_batch/'

    local_path = f'./temp_db/download/{random.randint(0, 100000)}.zip'

    download_file_from_firebase_storage(data.input_folder, local_path)

    data.input_folder = extract_zip(local_path)
    os.makedirs(data.output_folder, exist_ok=True)

    run_script(run_batch_infer_script, data)

    zip_path = f"./output/generated_{random.randint(0, 100000)}.zip"

    zip_wav_files(data.output_folder, zip_path)

    shutil.rmtree(data.input_folder)
    shutil.rmtree(data.output_folder)
    os.remove(local_path)
    url = upload_file_to_firebase_storage(
        zip_path, f"output/{os.path.basename(zip_path)}")
    os.remove(zip_path)

    return url


def process_batch_input(job_id: String, data, lang, db):
    response = asyncio.run(perform_batch_input(data, lang))
    db.query(Job).filter(Job.id == job_id).update(
        {"status": "COMPLETED", "result": response})
    db.commit()

    return {"job_id": job_id, "status": "COMPLETED"}


app = FastAPI(
    title="RVC_API",
    version="1.0",
    description="API for RVC",
    docs_url="/docs",

)
os.makedirs("output", exist_ok=True)


@app.post("/infer/{lang}")
async def infer(lang: str, data: str = Form(...), file: UploadFile = File(...)):

    data = data.replace(" ", "")
    data = json.loads(data)
    print(data)
    print(type(data))

    if lang not in model_map:
        raise HTTPException(status_code=400, detail="Unsupported language")

    # Create directories if they don't exist
    os.makedirs("output", exist_ok=True)
    os.makedirs("temp_db/download", exist_ok=True)

    try:
        # Save the uploaded WAV file to a temporary directory
        local_path = f'./temp_db/download/{random.randint(0, 100000)}.wav'
        with open(local_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Create InputData object from InputRequest
        data_obj = InputData(**data)

        # Set paths in InputData
        data_obj.pth_path = model_map[lang]
        data_obj.index_path = model_map[lang]
        data_obj.output_path = f'./output/{random.randint(0, 1000)}.wav'
        data_obj.input_path = local_path

        # Run inference script
        run_script(run_infer_script, data_obj)

        # Check if output file exists
        if not os.path.exists(data_obj.output_path):
            raise HTTPException(status_code=500, detail="Inference failed")

        # Stream the output file as a response
        def stream_file():
            with open(data_obj.output_path, "rb") as file:
                while True:
                    chunk = file.read(65536)  # Read 64 KB chunks
                    if not chunk:
                        break
                    yield chunk

        response = StreamingResponse(stream_file(), media_type="audio/wav")

        # Clean up temporary directory
        shutil.rmtree('./temp_db/download/')

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Batch Infer
@app.post("/batch_infer/{lang}")
async def batch_infer(lang: str, data: BatchRequest, background_tasks: BackgroundTasks, db=Depends(get_db)):

    os.makedirs("output", exist_ok=True)
    os.makedirs("temp_db/download", exist_ok=True)

    data_string = data.model_dump_json()

    job = Job(data=data_string, status="PENDING")
    db.add(job)
    db.commit()
    db.refresh(job)

    background_tasks.add_task(process_batch_input, job.id, data, lang, db)

    return {"job_id": job.id, "status": job.status}


@app.get("/jobs/{job_id}/")
async def get_job_status(job_id: str, db=Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"id": job.id, "data": job.data, "status": job.status, "result": job.result}


# Preprocess
@app.post("/preprocess")
async def preprocess(data: PreprocessInputData):
    label = random.randint(0, 1000)
    local_path = f"./train_db/dataset/{label}_data.zip"
    download_file_from_firebase_storage(data.dataset_path, local_path)

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
    uvicorn.run(app, host="127.0.0.1", port=8000)
