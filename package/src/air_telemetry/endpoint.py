# import requests

class Endpoint():
    endpoint = None
    token = None
    
    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.token = token
        print("Connecting to the following Telemetry endpoint:")
        print("> ENDPOINT:   {0}".format(endpoint))
        print("> TOKEN:      {0}".format(token))
        
    def log(self, level: str, detail: str, notify: bool):
        print("Logging following action:")
        print("> LEVEL:    {0}".format(level))
        print("> DETAIL:   {0}".format(detail))
        print("> NOTIFY:   {0}".format(notify))
        print("---------------------------------------")
        print("ENDPOINT: {0}, {1}".format(self.endpoint, self.token))
    
        

