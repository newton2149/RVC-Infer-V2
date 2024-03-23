from fastapi import FastAPI,HTTPException
import time

from inferV2 import run_batch_infer_script,run_infer_script
from trainv2 import run_preprocess_script,run_extract_script,run_train_script,run_index_script
from model import TrainInputData,IndexInputData,PreprocessInputData,ExtractInputData,InputData , BatchInputData


app = FastAPI()


    
def run_script(script_function, data):
    try:
        result = script_function(**data.dict())
        return {"message": result}

    except ValueError as value_error:
        raise HTTPException(status_code=400, detail=str(value_error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


# Infer
@app.post("/infer")
async def infer(data: InputData):
    return run_script(run_infer_script, data)

# Batch Infer
@app.post("/batch_infer")
async def batch_infer(data: BatchInputData):
    return run_script(run_batch_infer_script, data)

# Preprocess
@app.post("/preprocess")
async def preprocess(data: PreprocessInputData):
    return run_script(run_preprocess_script, data)

# Extract
@app.post("/extract")
async def extract(data: ExtractInputData):
    return run_script(run_extract_script, data)

# Train
@app.post("/train")
async def train(data: TrainInputData):
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