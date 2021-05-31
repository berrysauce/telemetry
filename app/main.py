from starlette.responses import StreamingResponse
import uvicorn
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import List, Optional, final
from deta import Deta
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid
import json


load_dotenv()
DETA_TOKEN = os.getenv("DETA_TOKEN")
app = FastAPI()
deta = Deta(DETA_TOKEN)
tokendb = deta.Base("telemetry-tokens")
logdb = deta.Base("telemetry-logs")


class CreateToken(BaseModel):
    app: str
    description: str
    
class LogAction(BaseModel):
    level: str
    description: str
    timestamp: str
    token: str
    app: str

class GetLogs(BaseModel):
    app: str
    token: str
    

@app.get("/")
def get_root():
    return {"msg": "Telemetry operated by berrysauce - Code/License at github.com/berrysauce/telemetry"}

@app.post("/token")
def post_session(item: CreateToken):
    today = str(datetime.now())
    token = str(uuid.uuid4())
    tokendb.put({"app": item.app,
            "description": item.description,
            "token": token,
            "created": today})
    return {"msg": "Token created!",
            "app": item.app,
            "description": item.description,
            "token": token}


@app.post("/log")
def post_log(log: LogAction):
    try:
        session = next(tokendb.fetch({"token": log.token}))[0]
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if log.app != session["app"]:
        return {"msg": "Token is not valid for this app!"}
    timestamp = datetime.strptime(log.timestamp, "%Y-%m-%d %H:%M:%S.%f")
    localtime = datetime.now()
    latency = str(localtime - timestamp)
    logdb.put({"app": log.app,
            "level": log.level,
            "description": log.description,
            "timestamp": log.timestamp,
            "latency": latency})
    return {"msg": "Action logged!",
            "latency": latency}
        
        
@app.post("/logs")
def post_logs(auth: GetLogs, format: bool = False):
    try:
        session = next(tokendb.fetch({"token": auth.token}))[0]
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if auth.app != session["app"]:
        return {"msg": "Token is not valid for this app!"}
    logs = next(logdb.fetch({"app": auth.app}))
    
    if format is False:
        return logs
    else:
        return {"msg": "Work-in-progress"}
            
                

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=80)