import requests
from colorama import Fore, Back, Style

class Endpoint():
    endpoint = None
    token = None
    
    def __init__(self, endpoint, app, token):
        self.endpoint = endpoint
        self.token = token
        print("Connecting to the following Telemetry endpoint:")
        print(Fore.BLUE + "Connecting to Telemetry endpoint..." + Style.RESET_ALL)
        try:
            data = {
                "app": app,
                "token": token
            }
            r = requests.get(endpoint, data)
            if r.status_code == 200 and r.json["valid"] == True:
                print(Fore.GREEN + "Successfully connected to '{0}'".format(endpoint) + Style.RESET_ALL)
            elif r.status_code == 401 or r.json["valid"] == False:
                print(Fore.RED + "Failed to connected to '{0}' - Unauthorized".format(endpoint) + Style.RESET_ALL)
            else:
                print(Fore.RED + "Failed to connected to '{0}' - Got status code {1}".format(endpoint, r.status_code) + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + "Failed to connected to '{0}' - Error: {1}".format(endpoint, e) + Style.RESET_ALL)
        
    def log(self, level: str, detail: str, notify: bool):
        print("Logging following action:")
        print("> LEVEL:    {0}".format(level))
        print("> DETAIL:   {0}".format(detail))
        print("> NOTIFY:   {0}".format(notify))
        print("---------------------------------------")
        print("ENDPOINT: {0}, {1}".format(self.endpoint, self.token))
    
        

