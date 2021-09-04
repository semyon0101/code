r = 2.6
D = []
t = open("expanded", "r").readlines(-1)
for i in range(len(t)):
    if i != len(t) - 1:
        line = t[i][0:-1]
        arg = line.split(",")
        if arg.count("?"):
            arg.remove("?")
        D.append(arg)
print("end render")


class C_1:
    def __init__(self):
        self.collection = []

    @staticmethod
    def profit(_collection, r):
        u = {}
        for _str in _collection:
            for char in _str:
                if char in u:
                    u[char] += 1
                else:
                    u[char] = 1
        return ((sum(list(u.values())) / len(list(u.keys()))) * len(list(u.keys()))) / \
               (len(list(u.keys())) ** r)

    @staticmethod
    def get_H_W(_collection):
        u = {}
        for _str in _collection:
            for char in _str:
                if char in u:
                    u[char] += 1
                else:
                    u[char] = 1

        return sum(list(u.values())) / len(list(u.keys())), len(list(u.keys()))

    def __str__(self):
        return f"{self.collection}"


def get_answer_1(D, r):
    answer = []
    for i in range(len(D)):
        if i % 10 == 0:
            print(i)
        _str = D[i]
        if not answer:
            collection = C_1()
            collection.collection.append(_str)
            answer.append(collection)
            continue

        v = {}
        for i in range(len(answer)):
            collection = answer[i]
            v[collection.profit(collection.collection + [_str], r) -
              collection.profit(collection.collection, r)] = i

        H_1, W_1 = 0, 0
        H_2, W_2 = 0, 0
        for i in range(len(answer)):
            collection = answer[i]
            if i == v[max(list(v.keys()))]:
                H_1 += collection.get_H_W(collection.collection + [_str])[0]
                W_1 += collection.get_H_W(collection.collection + [_str])[1]
                H_2 += collection.get_H_W(collection.collection)[0]
                W_2 += collection.get_H_W(collection.collection)[1]
            else:
                H_1 += collection.get_H_W(collection.collection)[0]
                W_1 += collection.get_H_W(collection.collection)[1]
                H_2 += collection.get_H_W(collection.collection)[0]
                W_2 += collection.get_H_W(collection.collection)[1]

        H_2 += C_1.get_H_W(_str)[0]
        W_2 += C_1.get_H_W(_str)[1]
        H_1 /= len(answer)
        H_2 /= len(answer)
        if H_1 / W_1 ** (r - 1) <= H_2 / W_2 ** (r - 1):
            collection = C_1()
            collection.collection.append(_str)
            answer.append(collection)
        else:
            answer[v[max(list(v.keys()))]].collection.append(_str)
    return answer


for c in get_answer_1(D, r):
    print(c)
