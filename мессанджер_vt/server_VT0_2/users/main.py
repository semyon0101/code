import мессанджер_vt.server_VT0_2.users.db as db

users = db.db("users/users/users.db", "users", "name text, password text")


def start(obj):
    if obj["command"] == "open_user":
        if (obj["name"], obj["password"]) in users.get_text():
            return b"connected"
        else:
            return b"Error name or password is not defined"
    elif obj["command"] == "create_user":
        if len(obj["name"]) >= 3 and len(obj["password"]) >= 3:
            if users.create(obj["name"], obj["password"]):
                return b"user is already done"
            else:
                print(users.get_text())
                return b"user made"
        else:
            return b"name or password is very small"
