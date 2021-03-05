import socket

sock = socket.socket()
sock.connect(('localhost', 9090))
nike = input("nike ")
pasvord = input("pasvord ")
message='[{0},{1}]'.format(nike, pasvord)
sock.send(message.encode("utf-8"))

data = sock.recv(1024)
sock.close()

print(data)
