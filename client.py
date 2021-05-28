import requests
import json

BASE_URL = 'http://192.168.31.157:5000'

username = input('Username : ')
appName = input('App Name: ')
print("")
# Create a App
resp = requests.post(BASE_URL + f"/create/{username}/{appName}")
result = json.loads(resp.content.decode("utf-8"))
print("Create App : ", resp.status_code, result)

apiKey = result["message"]["apiKey"]
masterKey = result["message"]["masterKey"]

# Check App Status:
resp = requests.get(BASE_URL + f"/app/{appName}")
print("App Status : ", resp.status_code,
      json.loads(resp.content.decode("utf-8")))
print("")
# Check Pin Status (Without Key)
resp = requests.get(BASE_URL + f"/app/{appName}/1")
print("Pin Status (w/o key) : ", resp.status_code,
      json.loads(resp.content.decode("utf-8")))


# Check Pin Status (With ApiKey)
resp = requests.get(
    BASE_URL + f"/app/{appName}/1", headers={"Authorization": "Basic "+apiKey})
print("Pin Status (w ApiKey) : ", resp.status_code,
      json.loads(resp.content.decode("utf-8")))
print("")

# Setting Pin Status (With ApiKey)
resp = requests.post(
    BASE_URL + f"/app/{appName}/1?value=150", headers={"Authorization": "Basic " + apiKey})
print("Setting Pin (w ApiKey) : ", resp.status_code,
      json.loads(resp.content.decode("utf-8")))

# Setting Pin Status (With MasterKey)
resp = requests.post(
    BASE_URL + f"/app/{appName}/1?value=150", headers={"Authorization": "Basic "+masterKey})
print("Setting Pin (w masterKey) : ", resp.status_code,
      json.loads(resp.content.decode("utf-8")))
print("")

# Check Pin Status (With ApiKey)
resp = requests.get(
    BASE_URL + f"/app/{appName}/1", headers={"Authorization": "Basic "+apiKey})
print("Pin Status (w ApiKey) : ", resp.status_code,
      json.loads(resp.content.decode("utf-8")))


# Check Pin Status (With MasterKey)
resp = requests.get(
    BASE_URL + f"/app/{appName}/1", headers={"Authorization": "Basic "+masterKey})
print("Pin Status (w MasterKey) : ", resp.status_code,
      json.loads(resp.content.decode("utf-8")))
print("")

# Delete App (without key)
resp = requests.delete(BASE_URL + f"/app/{appName}")
print("Delete (w/o Key) : ", resp.status_code,
      json.loads(resp.content.decode("utf-8")))

# Delete App (with ApiKey)
resp = requests.delete(
    BASE_URL + f"/app/{appName}", headers={"Authorization": "Basic "+apiKey})
print("Delete (w ApiKey) : ", resp.status_code,
      json.loads(resp.content.decode("utf-8")))


# Delete App (with MasterKey)
resp = requests.delete(
    BASE_URL + f"/app/{appName}", headers={"Authorization": "Basic "+masterKey})
print("Delete (w MasterKey) : ", resp.status_code,
      json.loads(resp.content.decode("utf-8")))
print("")

# Check App Status:
resp = requests.get(BASE_URL + f"/app/{appName}")
print("App Status : ", resp.status_code,
      json.loads(resp.content.decode("utf-8")))
print("")
