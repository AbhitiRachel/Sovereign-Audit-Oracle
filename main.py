from fastapi import FastAPI, UploadFile, File, HTTPException
from engine import process_and_detect
import time

app = FastAPI(
    title="Green-Grocer Vision System",
    description="Microservice for Food Quality Detection (Unit 1 & 5)"
)

@app.post("/inspect", status_code=200)
async def inspect_fruit(file: UploadFile = File(...)):

    start_time = time.time()
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Unsupported Media Type")

    try:
        content = await file.read()
        results = process_and_detect(content)  # now returns {"detections": [], "summary": {}}
        latency = time.time() - start_time

        return {
            "header": {
                "timestamp": time.ctime(),
                "latency_seconds": round(latency, 4),
                "status": "Success"
            },
            "data": {
                "total_count": results["summary"]["total_items"],
                "detections": results["detections"],
                "summary": results["summary"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))