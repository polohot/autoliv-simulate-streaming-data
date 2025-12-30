import time
import json
import random
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

# 1. Add a health check to confirm server is ALIVE
@app.get("/")
def healthCheck():
    return {"status": "running", "message": "Go to /stream to see data"}

# 2. Generator Logic
async def generateSensorStream():
    while True:
        data = {
            "sensorId": f"sensor_{random.randint(1, 3):02d}",
            "temperature": round(random.uniform(20.0, 35.0), 2),
            "timestamp": int(time.time()),
            "status": random.choice(["OK", "WARNING"])
        }
        yield json.dumps(data) + "\n"
        await asyncio.sleep(1)

@app.get("/stream")
async def streamEndpoint():
    print("--> New client connected to stream")
    
    # 3. CRITICAL FIX: Disable Buffering in headers
    response = StreamingResponse(generateSensorStream(), media_type="application/x-ndjson")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no" # Tells Koyeb/Nginx to send data INSTANTLY
    return response

# CMD: uvicorn server_generator:app --host 0.0.0.0 --port 8000