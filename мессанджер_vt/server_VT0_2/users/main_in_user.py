import мессанджер_vt.server_VT0_2.users.db as db

users = db.db()


def start(obj):
    mes = {}
    try:
        if obj["command"] == "open_user":
            b, info = users.open_user(obj["name"], obj["password"])

            if b:
                mes["answer"] = "connected"
                mes["info"] = info
            else:
                mes["answer"] = "Error name or password is not defined"
        elif obj["command"] == "create_user":
            if len(obj["name"]) >= 3 and len(obj["password"]) >= 3:
                if users.create_user(obj["name"], obj["password"]):
                    mes["answer"] = "user made"
                else:
                    mes["answer"] = "user is already done"
            else:
                mes["answer"] = "name or password is very small"
        elif obj["command"] == "refract_user":
            b, info = users.refract_user(obj["name"], obj["password"], obj["refract_info"])
            if b:
                mes["answer"] = "refract made"
                mes["info"] = info
            else:
                mes["answer"] = info
        else:
            mes["answer"] = "command is not defined"
    except:
        mes["answer"] = "Error"
    return mes
