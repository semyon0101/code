import socket
import json
import sys
import time
import threading

path_to_db = "user.db"


class start:
    def __init__(self):
        self.args = []
        self.sock = socket.socket()
        self.stop = False

    def start(self):
        try:
            self.sock.connect(('localhost', 9090))
        except:
            print("please start server")
            sys.exit()
        threading.Thread(target=self.__f).start()

    def __f(self):
        while not self.stop:
            try:
                arg = self.args[0]
                self.sock.send(arg)
                self.args.pop(0)

            except:
                pass

            time.sleep(1)

    def spend(self, info):
        self.args.append(json.dumps(info).encode())
        try:
            return json.loads(self.sock.recv(1024).decode())
        except:
            self.stop = True
            return "error server is abort me"


class db:
    def __init__(self):
        self.args_array = ["name", "password"]
        for arg in self.args_array:
            exec(f"self.{arg} = ''")

    def refract(self, **kwargs):
        err = []
        for arg in list(kwargs.keys()):
            if arg in self.args_array:
                exec(f"self.{arg} = {kwargs[arg]}")
            else:
                err.append(f"{arg} not in {self.args_array}")
        self.update(vars(self))
        return err

    @staticmethod
    def update(info):
        _db = open(path_to_db, "w")
        _db.write(json.dumps(info))
        _db.close()

    @staticmethod
    def get_info():
        _db = open(path_to_db)
        info = _db.read()
        _db.close()
        return json.loads(info)


s = start()
s.start()
obj = {"path": "user",
       "command": "open_user",
       "name": "semen123",
       "password": "3421"
       }
print(s.spend(obj))
obj = {"path": "user",
       "command": "refract_user",
       "name": "semen",
       "password": "123456",
       "refract_info": {
           "password": "123456"
           }
       }
print(s.spend(obj))
s.stop = True
# obj = db()
# obj.refract(name="12", password="43")
# print(obj.get_info())
