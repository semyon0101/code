import connected_user.user as user
import logged
import message_file
import sys
import json

connection = user.start()
connection.start()
db = user.db()
com = {}
for arg in ["name", "password"]:
   exec("com.update({'"+str(arg)+"': '"+eval(f"db.{arg}")+"' })")
com.update({"command": "open_user"})

answer = connection.spend(com)
if answer == "Error name or password is not defined":
   print("get password")
   if not logged.connection_user(connection, db):
      connection.stop = True
      sys.exit()
elif answer == "Error":
   for _ in range(10):
      print("Error !!!!\n")


print("message file")
message_file.start(connection, db)

connection.stop = True
# com = db.get_info().update({"command"})

# if db.user(command="open_user")!=b"connected":
#    a = True
#    while a:
#       text = get_password.start()
#       name, password = text
#       if text:
#          db.user(name, password)
#          answer = db.user(command="create_user")
#          if answer== b'user made' or answer== b'user is already done':
#             a=False
#          else:
#             print(answer)
#       else:
#          a = False
# if db.user(command="open_user")==b"connected":
#    db.user(servers="semen, semen")
#    message_file.start()