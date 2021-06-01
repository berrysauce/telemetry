import requests
from colorama import Fore, Back, Style
import json
from datetime import datetime

class Endpoint():
    endpoint = None
    token = None
    app = None
    
    def __init__(self, endpoint, app, token):
        self.endpoint = endpoint
        self.token = token
        self.app = app
        print(Fore.BLUE + "Connecting to Telemetry endpoint..." + Style.RESET_ALL)
        try:
            data = {
                "app": app,
                "token": token
            }
            r = requests.post(endpoint+"/validate", json.dumps(data))
            content = json.loads(r.text)
            if r.status_code == 200 and content["valid"] == True:
                print(Fore.GREEN + "Successfully connected to '{0}' as '{1}'".format(endpoint, app) + Style.RESET_ALL)
            elif r.status_code == 401 or content["valid"] == False:
                print(Fore.RED + "Failed to connected to '{0}' as '{1}' - Unauthorized".format(endpoint, app) + Style.RESET_ALL)
            else:
                print(Fore.RED + "Failed to connected to '{0}' as '{1}' - Got status code {2}".format(endpoint, app, r.status_code) + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + "Failed to connected to '{0}' as '{1}' - Error: {2}".format(endpoint, app, e) + Style.RESET_ALL)
        
    def log(self, level: str, detail: str, notify: bool = False):
        data = {
            "level": level,
            "detail": detail,
            "timestamp": str(datetime.now()),
            "token": self.token,
            "app": self.app,
            "notify": notify
        }
        requests.post(self.endpoint+"/log", data=data)
    
        

