import socket
import json
import users.main as user
import threading
import subprocess


class Player:
    def __init__(self, _conn):
        self.conn = _conn
        self.name = None
        self.func = '''
import socket
import json
import users.main as user
import os
import copy
conn = {}
while True:
    try:
        data = conn.recv(1024)
    except:
        conn.close()
        break
    obj = json.loads(date.decode())
    answer_obj = {}
    if obj["path"] == "user":
        answer_obj.update(user.start(obj))
    elif obj["path"].startswith("server-"):
        path = obj["path"][7:]
        b = False
        for name in os.listdir("servers"):
            if name == path:
                b = True
                eval(f"import servers.{path}.main as server\nanswer_obj.update(server.start(obj))")
        if not b:
            answer_obj["answer"] = "server not found"
    elif obj["command"] == "create_server":
        answer_obj.update(copy.copy(obj["server"]))
    conn.send(json.dumps(answer_obj))
    

'''
        self.subprocess = subprocess.Popen(["python", "-c", ""])

    def start(self):
        try:
            obj = json.loads(self.conn.recv(1024).decode())
            answer_obj = user.start(obj)
            answer = answer_obj["answer"]
            if answer == "connected" or answer == "user made":
                self.conn.send(json.dumps(answer_obj))
                self.subprocess = subprocess.Popen(["python", "-c", self.func.format(self.conn)])
            else:
                self.conn.send(json.dumps(answer))
        except:
            pass

    def __str__(self):
        return f"{self.subprocess.poll() is None}"

    def __repr__(self):
        return f"{self.subprocess.poll() is None}"


class All_online:
    def __init__(self):
        self.online = []

    def start_player(self, _conn):
        player = Player(_conn)
        threading.Thread(player.start())
        self.online.append(player)

    def get_online(self):
        names = []
        arr = self.online.copy()
        for player in arr:
            if str(player) == "False":
                stop = False
                for i in range(len(self.online)):
                    if not stop and player == self.online[i]:
                        self.online.pop(i)
                        stop = True
            else:
                names.append(player.name)
        return names


all_online = All_online()

sock = socket.socket()
sock.bind(('localhost', 9090))
sock.listen()
print("start server")
while True:
    conn, adr = sock.accept()

    print('connected: ', adr)
    all_online.start_player(conn)


sock.close()
