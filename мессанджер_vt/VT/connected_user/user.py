import socket
import sqlite3


class db1:
    def __init__(self, name):
        con = sqlite3.connect(name)
        cur = con.cursor()
        try:
            cur.execute("CREATE TABLE user(name text, password text, command text, servers text)")
        except:
            pass
        self.cur, self.con = cur, con

    def get_text(self):
        return [*self.cur.execute("SELECT * FROM user")]

    def create_user(self, name, password, command, servers):
        if not (name, password, command, servers) in self.get_text():
            self.cur.execute(f"INSERT INTO user VALUES ('{name}','{password}','{command}', '{servers}')")
            self.con.commit()
        else:
            return True

    def remake_user(self, name, password, command, servers):
        self.cur.execute(f"DELETE FROM user")
        self.create_user(name, password, command, servers)
        self.con.commit()


db = db1("connected_user/user.db")
if len(db.get_text()) < 1:
    db.create_user("", "", "", "")


# create_user, open_user
def user(nike=None, password=None, command=None, servers=None):
    sock = socket.socket()
    nike1, password1, command1, servers1 = db.get_text()[0]
    if nike != None:
        nike1 = nike
        db.remake_user(nike, password1, command1, servers1)
    if password != None:
        password1 = password
        db.remake_user(nike1, password, command1, servers1)
    if command != None:
        command1 = command
        db.remake_user(nike1, password1, command, servers1)
    if servers != None:
        servers1 = servers
        db.remake_user(nike1, password1, command1, servers)


    if command1.startswith("open_server: "):
        command2 = command1[13:]
        command1 = "open_server: "
        for i in range(len(servers1.split("; "))):
            if int(command2) == i:
                command1 += servers1.split("; ")[i]
    elif command1.startswith("spend_message: "):
        command2 = command1[15:]
        command3 = ", ".join(command2.split(", ")[1:])
        command2 = command2.split(", ")[0]
        command1 = "spend_message: "

        for i in range(len(servers1.split("; "))):
            if int(command2) == i:
                command1 += servers1.split("; ")[i]
        command1 += ", "+ command3

    if command1:
        sock.connect(('localhost', 9090))
        message = "['''{0}''','''{1}''','''{2}'''],close".format(nike1, password1, command1)
        sock.send(message.encode("utf-8"))

        data = sock.recv(1024)
        sock.close()
        return data
