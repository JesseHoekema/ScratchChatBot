from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import logging


logging.getLogger("uvicorn").handlers = []
logging.getLogger("uvicorn.access").handlers = []
logging.getLogger("uvicorn.error").handlers = []



app = FastAPI()

@app.get("/ping")
def ping():
    return JSONResponse({"status": "ok"})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=6913, log_level="critical")
