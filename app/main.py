from requests.api import head
import uvicorn
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import Optional
from deta import Deta
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid
import requests


load_dotenv()
DETA_TOKEN = os.getenv("DETA_TOKEN")
PUSH_TOKEN = os.getenv("PUSH_TOKEN")
app = FastAPI()
deta = Deta(DETA_TOKEN)
tokendb = deta.Base("telemetry-tokens")
logdb = deta.Base("telemetry-logs")


class CreateToken(BaseModel):
    app: str
    description: str
    
class LogAction(BaseModel):
    level: str
    detail: str
    timestamp: str
    token: str
    app: str
    notify: bool

class Authorize(BaseModel):
    app: str
    token: str
    

@app.get("/")
def get_root():
    return {"msg": "Telemetry operated by berrysauce - Code/License at github.com/berrysauce/telemetry"}

@app.post("/token")
def post_session(item: CreateToken):
    today = str(datetime.now())
    token = str(uuid.uuid4())
    tokendb.insert({"app": item.app,
                    "description": item.description,
                    "token": token,
                    "created": today})
    return {"msg": "Token created!",
            "app": item.app,
            "description": item.description,
            "token": token}

@app.post("/validate")
def post_validate(auth: Authorize):
    try:
        session = tokendb.fetch({"token": auth.token}).items[0]
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if auth.app != session["app"]:
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        return {"valid": True}

@app.post("/log")
def post_log(log: LogAction):
    try:
        session = tokendb.fetch({"token": log.token}).items[0]
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if log.app != session["app"]:
        return {"msg": "Token is not valid for this app!"}
    timestamp = datetime.strptime(log.timestamp, "%Y-%m-%d %H:%M:%S.%f")
    localtime = datetime.utcnow()
    latency = str(localtime - timestamp)
    logdb.put({"app": log.app,
            "level": log.level,
            "detail": log.detail,
            "timestamp": log.timestamp,
            "latency": latency})
    
    if log.notify is True: 
        title = "{0} [{1}]".format(log.app, log.level)
        body = "{0} - Timestamp: {1}".format(log.detail, log.timestamp)
        r = requests.post("https://push.techulus.com/api/v1/notify/{0}?title={1}&body={2}".format(PUSH_TOKEN, title, body))
        
        return {"msg": "Action logged!",
                "latency": latency,
                "notification_status": r.status_code}
    
    return {"msg": "Action logged!",
            "latency": latency}
         
@app.post("/logs")
def post_logs(auth: Authorize, format: bool = False):
    try:
        session = tokendb.fetch({"token": auth.token}).items[0]
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if auth.app != session["app"]:
        return {"msg": "Token is not valid for this app!"}
    logs = logdb.fetch({"app": auth.app}).items
    
    if format is False:
        return logs
    else:
        return {"msg": "Work-in-progress"}
                

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=80)