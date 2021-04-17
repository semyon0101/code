import socket
import sqlite3


class db1:
    def __init__(self, name):
        con = sqlite3.connect(name)
        cur = con.cursor()
        try:
            cur.execute("CREATE TABLE user(name text, password text, command text)")
        except:
            pass
        self.cur, self.con = cur, con

    def get_text(self):
        return [*self.cur.execute("SELECT * FROM user")]

    def create_user(self, name, password, command):
        if not (name, password, command) in self.get_text():
            self.cur.execute(f"INSERT INTO user VALUES ('{name}','{password}','{command}')")
            self.con.commit()
        else:
            return True

    def remake_user(self, name, password, command):
        self.cur.execute(f"DELETE FROM user")
        self.create_user(name, password, command)
        self.con.commit()


db = db1("connected_user/user.db")
if len(db.get_text()) < 1:
    db.create_user("", "", "")


# create_user, open_user
def user(nike=None, password=None, command=None):
    sock = socket.socket()
    nike1, password1, command1 = db.get_text()[0]
    if nike != None:
        nike1 = nike
        db.remake_user(nike, password1, command1)
    if password != None:
        password1 = password
        db.remake_user(nike1, password, command1)
    if command != None:
        command1 = command
        db.remake_user(nike1, password1, command)

    sock.connect(('localhost', 9090))
    message = '["{0}","{1}","{2}"],close'.format(nike1, password1, command1)
    sock.send(message.encode("utf-8"))

    data = sock.recv(1024)
    sock.close()
    return data
