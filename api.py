from fastapi import FastAPI, Request
import subprocess
import time

app = FastAPI()


# Helper function to execute commands
def execute_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return {"output": result.stdout, "error": result.stderr}
    except Exception as e:
        return {"error": str(e)}


# Infer
@app.post("/infer")
async def infer(request: Request):
    command = ["python", "main.py", "infer"] + await request.json()
    return execute_command(command)


# Batch Infer
@app.post("/batch_infer")
async def batch_infer(request: Request):
    command = ["python", "main.py", "batch_infer"] + await request.json()
    return execute_command(command)




# Preprocess
@app.post("/preprocess")
async def preprocess(request: Request):
    command = ["python", "main.py", "preprocess"] + await request.json()
    return execute_command(command)


# Extract
@app.post("/extract")
async def extract(request: Request):
    command = ["python", "main.py", "extract"] + await request.json()
    return execute_command(command)


# Train
@app.post("/train")
async def train(request: Request):
    command = ["python", "main.py", "train"] + await request.json()
    return execute_command(command)


# Index
@app.post("/index")
async def index(request: Request):
    command = ["python", "main.py", "index"] + await request.json()
    return execute_command(command)





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