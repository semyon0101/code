import socket
import db

db = db.db("users.db")

sock = socket.socket()
sock.bind(('localhost', 9090))
sock.listen(10)
print(db.get_text())


def remake_message(message):
    try:
        message = b"".join(message.split(b",close"))

        arr = eval(message)
        error_marks = [",", "]", "[", "{", "}", "/", "\\", " ", "-", "=", "+", "*",
                       "&", "^", "%", "$", "#", "@", "!", "(", ")", "|", "<", ">", "~"]
        error = False
        for mark in error_marks:
            error = ("".join(arr[0].split(mark)) != arr[0] or
                     "".join(arr[1].split(mark)) != arr[1] or
                     error)
        error = (error or arr[0] == "" or arr[1] == "")
        if error:
            return b"Error special character was used in name or password"
        if arr[2] == "open_user":
            if (arr[0], arr[1]) in db.get_text():
                return b"connected"
            else:
                return b"Error name or password is not defined"
        elif arr[2] == "create_user":
            if len(arr[0]) >= 3 and len(arr[1]) >= 3:
                if db.create_user(arr[0], arr[1]):
                    return b"user is already done"
                else:
                    return b"user made"
            else:
                return b"name or password is very small"

        else:
            return b"command is not defined"
    except:
        return b"Error"


while True:
    conn, addr = sock.accept()

    print('connected:', addr)

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
        if x == 1 and data.endswith(b"],close"):
            conn.send(remake_message(mes))
        else:
            conn.send(b"Error")
            break

        x += 1
    print("break")

sock.close()
