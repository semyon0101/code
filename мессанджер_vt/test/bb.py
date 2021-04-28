import multiprocessing
import subprocess
import os
import time


def get_more_servers(_):
    while True:
        names1 = names.copy()
        a = len(names)
        for _i in range(a):
            _i = a - _i - 1
            name = names1[_i]
            if not str(name) in os.listdir("servers"):
                names.pop(_i)

        for _i in range(len(os.listdir("servers"))):
            name = int(os.listdir("servers")[_i])
            if not name in names:
                names.append(name)
                names.sort()
                _i = 0
                for _j in range(len(names)):
                    if names[_j] == name:
                        _i = _j
                        break
                p1 = multiprocessing.Process(target=start, args=[_i])
                p1.start()
                print(names)
        time.sleep(0.5)


def start(_i):
    print(os.listdir('servers')[_i])
    p = subprocess.Popen(["python", f"servers/{os.listdir('servers')[_i]}/main.py"])

    p.communicate()


names = []
d = []

for i in range(len(os.listdir("servers"))):
    p1 = multiprocessing.Process(target=start, args=[i])
    d.append(p1)

    names.append(int(os.listdir("servers")[i]))

if __name__ == '__main__':
    for p1 in d:
        p1.start()
    p2 = multiprocessing.Process(target=get_more_servers, args=[0])
    p2.start()
    print("end")
