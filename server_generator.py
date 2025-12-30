import time
import json
import random
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

# 1. The Generator Logic (Simulates your Sensor Data)
async def generateSensorStream():
    while True:
        # Create fake data
        data = {
            "sensorId": f"sensor_{random.randint(1, 3):02d}",
            "temperature": round(random.uniform(20.0, 35.0), 2),
            "timestamp": int(time.time()),
            "status": random.choice(["OK", "WARNING"])
        }
        
        # Serialize to JSON and add a newline (critical for streaming)
        yield json.dumps(data) + "\n"
        
        # Control the speed (1 message per second)
        await asyncio.sleep(1)

# 2. The Endpoint (Your laptop connects here)
@app.get("/stream")
async def streamEndpoint():
    print("--> New client connected to stream")
    return StreamingResponse(generateSensorStream(), media_type="application/x-ndjson")

# To run locally for testing: uvicorn server_generator:app --reload