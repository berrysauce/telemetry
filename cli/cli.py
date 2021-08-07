import requests
import json
from time import sleep
from colorama import Fore, Back, Style
from pyfiglet import Figlet

app = "test"
token = "f209f573-6c32-4763-bc5c-583a1b17e0db"
endpoint = "https://telemetry.brry.cc"

try:
    f = Figlet(font="slant")
    print(f.renderText("telemetry CLI"))

    print(Fore.BLUE + ">>> Connecting to Telemetry endpoint..." + Style.RESET_ALL)
    try:
        r = requests.post(endpoint + "/validate", data=json.dumps({"app": app, "token": token}))
        
        if r.status_code == 200:
            print(Fore.GREEN + "... Connected successfully!" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"... Failed to connect! \n... Status code: {r.status_code} \n... Detail: {r.text}" + Style.RESET_ALL)
            print(Fore.YELLOW + "Stopping telemetry log listener (Error)" + Style.RESET_ALL)
            quit()
    except Exception as e:
        print(Fore.RED + f"... Failed to connect! \n... Detail: {e}" + Style.RESET_ALL)
        print(Fore.YELLOW + "Stopping telemetry log listener (Error)" + Style.RESET_ALL)
        quit()

    print(100*"-")

    logs = []
    while True:
        r = requests.post(endpoint + "/logs?formatted=true", data=json.dumps({"app": app, "token": token}))
        requested_logs = json.loads(r.text)
        for log in requested_logs:
            loglevel = log["level"]
            logtimestamp = log["timestamp"]
            logdetail = log["detail"]
            loglatency = log["latency"]
            if log not in logs:
                if loglevel == "INFO":
                    levelcolor = Fore.BLUE
                elif loglevel == "DEBUG":
                    levelcolor = Fore.MAGENTA
                elif loglevel == "WARNING":
                    levelcolor = Fore.YELLOW
                elif loglevel == "ERROR":
                    levelcolor = Fore.RED
                elif loglevel == "CRITICAL":
                    levelcolor = Fore.RED
                else:
                    levelcolor = Fore.BLUE
                print(f"{app} - " + levelcolor + f"[{loglevel}] " + Style.RESET_ALL + f"[{logtimestamp}] - {logdetail} " + Fore.CYAN + f"// Latency: {loglatency}" + Style.RESET_ALL)
                logs.append(log)
        sleep(5)
except KeyboardInterrupt:
    print(" ")
    print(Fore.YELLOW + "Stopped telemetry log listener (KeyboardInterrupt)" + Style.RESET_ALL)