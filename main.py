import logging
import os
import threading
from sys import stderr
import server

from fastapi import FastAPI, Request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s : %(name)s : %(levelname)s [%(threadName)s]  %(message)s",
    handlers=[
        logging.StreamHandler(stderr)
    ]
)

# Get the logger
log = logging.getLogger(__name__)


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    log.info("Startup event")
    server.start_tcp_servers(None, False)

@app.get("/{api:path}")
async def root(api: str, request: Request):
    parms = {}
    for k in request.query_params.keys():
        parms[k] = request.query_params[k]
    log.info(f"API: /{api}, parms: {parms}, headers: {request.headers}")
    return {"api": f"/{api}", "parms": parms, "headers": request.headers}


