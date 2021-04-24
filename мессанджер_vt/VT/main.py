import connected_user.user as db
# spend_message   open_server   open_user   create_user   create_server
# print(db.user("12", "23", "spend_message: 0, mmmmm", "semen, semen; 121, 341"))
# print(db.user("12", "23", "open_server: 0", "semen, semen; 121, 341"))
import get_password
import message_file

if db.user(command="open_user")!=b"connected":
   a = True
   while a:
      text = get_password.start()
      name, password = text
      if text:
         db.user(name, password)
         answer = db.user(command="create_user")
         if answer== b'user made' or answer== b'user is already done':
            a=False
         else:
            print(answer)
      else:
         a = False
if db.user(command="open_user")==b"connected":
   db.user(servers="semen, semen")
   message_file.start()