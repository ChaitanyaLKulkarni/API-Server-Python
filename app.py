from flask import Flask, jsonify, request, make_response
import shortuuid
import base64
app = Flask(__name__)

allApps = {}
values = {}
suid = shortuuid.ShortUUID()


def getUuid(length=11):
    return suid.random(length=length)


def getBase64(s):
    message_bytes = s.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def getStr(b):
    base64_bytes = b.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message


@app.route("/create/<username>/<appName>", methods=["POST"])
def createApp(username, appName):
    if appName in allApps:
        return make_response(jsonify({"status": 409, "message": "App already exists"}), 409)
    else:
        masterKey = getUuid(15)
        masterStr = getBase64(username + ":" + masterKey)

        apiKey = getUuid(8)
        apiStr = getBase64(":"+apiKey)
        allApps[appName] = {"username": username,
                            "apiKey": apiKey, "masterKey": masterKey}
        print(allApps)
        values[apiKey] = {}
        return make_response(jsonify({"status": 200, "message": {"masterKey": masterStr, "apiKey": apiStr}}), 200)


@app.route("/app/<appName>", methods=["GET", "DELETE"])
def getAppInfo(appName):
    if appName in allApps:
        myApp = allApps[appName]
        if request.method == "GET":
            r = {"apiKey": getBase64(":" + myApp["apiKey"])}
            if request.args.get("master"):
                r["masterKey"] = getBase64(
                    myApp["username"]+":"+myApp["masterKey"])
            return make_response(jsonify({"status": 200, "message": r}), 200)

        if request.method == "DELETE":
            if not request.headers.get("Authorization"):
                return make_response(jsonify({"staus": 403, "message": "No Key Provided!"}), 403)

            apiKey = allApps[appName]["apiKey"]
            masterKey = allApps[appName]["masterKey"]

            username, mK = getStr(
                request.headers.get('Authorization').replace("Basic ", "")).split(":")

            if username != myApp["username"] or mK != masterKey:
                return make_response(jsonify({"staus": 403, "message": "Wrong Key Provided"}), 403)

            del allApps[appName]
            del values[apiKey]
            return make_response(jsonify({"status": 200, "message": "Deleted Successfully"}), 200)

    else:
        return make_response(jsonify({"status": 404, "message": "Not Found!"}), 404)


@app.route("/app/<appName>/<pin>", methods=["GET", "POST"])
def getPinValue(appName, pin):
    if appName not in allApps:
        return make_response(jsonify({"status": 404, "message": "not Found!"}), 404)

    if not request.headers.get("Authorization"):
        return make_response(jsonify({"staus": 403, "message": "No Key Provided!"}), 403)

    myApp = allApps[appName]
    apiKey = allApps[appName]["apiKey"]
    masterKey = allApps[appName]["masterKey"]
    if request.method == 'POST':
        username, mK = getStr(
            request.headers.get('Authorization').replace("Basic ", "")).split(":")

        if username != myApp["username"] or mK != masterKey:
            return make_response(jsonify({"staus": 403, "message": "Wrong Key Provided"}), 403)

        v = values[apiKey]["pin"] = request.args.get("value")
        return make_response(jsonify({"staus": 200, "message": {"pin": pin, "value": v}}), 200)

    _, aK = getStr(
        request.headers.get('Authorization').replace("Basic ", "")).split(":")

    if aK != apiKey and aK != masterKey:
        return make_response(jsonify({"staus": 403, "message": "Wrong Key Provided"}), 403)

    v = values[apiKey].get("pin")
    return make_response(jsonify({"staus": 200, "message": {"pin": pin, "value": v}}), 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
