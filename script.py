import os
import shutil
import time

from flask import Flask, jsonify


app = Flask(__name__)


# PASS = "/home/whatsapp/"
# my pass
PASS = "/home/vrevt/"


@app.route("/create", methods=['POST'])
def create():
    # in port.txt single number - starting port
    time.sleep(30)
    file = open("port.txt", "r")
    port = int(file.readline())
    port += 1
    file.close()

    # creating a new folder
    srcDefaultBot = PASS + "default-bot"
    srcNewBot = PASS + str(port) + "-bot"
    shutil.copytree(srcDefaultBot, srcNewBot, symlinks=False, ignore=None, copy_function=shutil.copy2,
                    ignore_dangling_symlinks=False)

    # change port in docker-compose.yml
    srcDockerCompose = srcNewBot + "/docker-compose.yml"
    dockerCompose = open(srcDockerCompose, "r")
    code = dockerCompose.read()
    dockerCompose.close()

    code = code.replace("5000:5000", f"{port}:5000")

    dockerCompose = open(srcDockerCompose, "w")
    dockerCompose.write(code)
    dockerCompose.close()

    cmd = f"cd {srcNewBot} && docker-compose build"
    os.system(cmd)

    file = open("port.txt", "w")
    file.write(str(port))
    file.close()

    answer = {
        'status': 'created',
        'port': port,
    }
    return jsonify(answer)


@app.route("/start/<port>", methods=['POST'])
def start(port):
    srcBot = PASS + str(port) + "-bot"
    print(srcBot)
    cmd = f"cd {srcBot} && docker-compose up -d"

    try:
        os.system(cmd)
        return jsonify({"Status": "Started", 'Port': port})
    except:
        return jsonify({"Status": "Not Started", "Port": port})


@app.route("/down/<port>", methods=['POST'])
def down(port):
    srcBot = PASS + str(port) + "-bot"
    cmd = f"cd {srcBot} && docker-compose down"

    try:
        os.system(cmd)
        return jsonify({"Status": "Downed", 'Port': port})
    except:
        return jsonify({"Status": "Not Downed", "Port": port})


@app.route("/delete/", methods=['POST'])
def delete():
    cmd = "docker container prune -f"

    try:
        os.system(cmd)
        return jsonify({"Status": "Deleted"})
    except:
        return jsonify({"Status": "Not Deleted"})


@app.route("/deleteall/", methods=['POST'])
def deleteall():
    cmd = "docker rm -f $(docker ps -a -q)"

    try:
        os.system(cmd)
        return jsonify({"Status": "Deleted all"})
    except:
        return jsonify({"Status": "Not Deleted all"})


if __name__ == "__main__":
    app.run(debug=False, port=5000)
