import requests
import json
from time import sleep

app = "test"
token = "f209f573-6c32-4763-bc5c-583a1b17e0db"
endpoint = "https://telemetry.brry.cc"

print("Connecting to Telemetry Endpoint...")
r = requests.post(endpoint + "/validate", data=json.dumps({"app": app, "token": token}))
if r.status_code == 200:
    print("Connected successfully!")
else:
    print(f"Failed to connect - {r.status_code}")

print(100*"-")

logs = []
while True:
    r = requests.post(endpoint + "/logs?formatted=true", data=json.dumps({"app": app, "token": token}))
    requested_logs = json.loads(r.text)
    for log in requested_logs:
        if log not in logs:
            print("{0} - [{1}] [{2}] - {3} // Latency: {4}".format(app, log["level"], log["timestamp"], log["detail"], log["latency"]))
            logs.append(log)
    sleep(5)