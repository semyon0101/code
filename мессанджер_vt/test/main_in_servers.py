import socket
import json
import users.main as user
import os


sock = socket.socket()
sock.bind(('localhost', 9090))

sock.listen(10)

while True:
    conn, adr = sock.accept()

    print('connected: ', adr)

    mes = b""
    x = 1
    while x:
        conn.settimeout(3)
        try:
            data = conn.recv(1024)
        except:
            conn.close()
            break
        mes += data
        if x == 1:
            obj = json.loads(mes.decode("utf-8"))
            if obj["path"] == "user":
                conn.send(user.start(obj))
            elif obj["path"].startswith("server-"):
                path = obj["path"][7:]
                b = False
                for name in os.listdir("servers"):
                    if name == path:
                        b = True
                        eval(f'''import servers.{path}.main as server
conn.send(server.start(obj))''')
                        break
                if not b:
                    conn.send(b"Error")
                    break
            else:
                conn.send(b"Error")
                break
        else:
            conn.send(b"Error")
            break

        x += 1
    print("break")

sock.close()