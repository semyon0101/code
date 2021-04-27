import multiprocessing
import subprocess
import os
import time


def get_more_servers(_):
    while True:
        names1 = names
        for _i in range(len(names1)):
            _i = len(names1) - _i - 1
            name = names1[_i]
            if not name in os.listdir("servers"):
                names.pop(_i)

        for _i in range(len(os.listdir("servers"))):
            name = os.listdir("servers")[_i]
            if not name in names:
                names.append(name)
                p1 = multiprocessing.Process(target=start, args=[0])
                p1.start()
        time.sleep(0.5)


def start(_i):
    p = subprocess.Popen(["python", f"servers/{os.listdir('servers')[_i]}/main.py"])

    p.communicate()


names = []
d = []

for i in range(len(os.listdir("servers"))):
    p1 = multiprocessing.Process(target=start, args=[i])
    d.append(p1)

    names.append(os.listdir("servers")[i])

if __name__ == '__main__':
    for p1 in d:
        p1.start()
    p2 = multiprocessing.Process(target=get_more_servers, args=[0])
    p2.start()
    print("end")
