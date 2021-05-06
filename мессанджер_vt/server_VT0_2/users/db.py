import json


class db:
    def __init__(self):
        self.path = "users/users"

    def create_user(self, name, password):

        try:
            user = open(self.path + str(name))
            user.close()
            return False
        except:
            user = open(self.path + str(name), "w")
            info = {"name": name,
                    "password": password}
            user.write(json.dumps(info))
            user.close()
            return True

    def refract_user(self, name, refract_info):
        try:
            user = open(self.path + str(name), "r")
            info = json.loads(user.read())
            user.close()
        except:
            return "problem with user"
        try:
            user = open(self.path + str(name), "w")
            keys = list(refract_info.keys())
            for key in keys:
                info[key] = refract_info[key]
            user.write(json.dumps(info))
            user.close()
            return "refract made"
        except:
            return "kwargs error"

    def open_user(self, name, password):
        user = open(self.path + str(name), "r")
        info = json.loads(user.read())
        user.close()
        if info["name"] == name and info["password"] == password:
            return True, info
        else:
            return False


