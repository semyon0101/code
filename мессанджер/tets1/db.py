import sqlite3


class db:
    def __init__(self, name):
        con = sqlite3.connect(name)
        cur = con.cursor()
        try:
            cur.execute("CREATE TABLE users(name text,password text)")
        except:
            pass
        self.cur, self.con = cur, con

    def get_text(self):
        return [*self.cur.execute("SELECT * FROM users")]

    def create_user(self, name, password):
        if not (name, password) in self.get_text():
            self.cur.execute(f"INSERT INTO users VALUES ('{name}',{password})")
            self.con.commit()
        else:
            return True

    def remake_user(self, name, password):
        names = []
        for name in self.get_text():
            names.append(name[0])
        if name in names:
            self.cur.execute(f"DELETE FROM users WHERE name={name}")
            self.create_user(name, password)
            self.con.commit()
        else:
            return True
