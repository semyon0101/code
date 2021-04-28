import os


def copy(path_copy: str, path_paste: str):
    for i in range(len(path_paste.split("/"))):
        name = "/".join(path_paste.split("/")[:i + 1])
        if i != len(path_paste.split("/")) - 1:
            try:
                os.mkdir(name)
            except:
                pass
        else:
            paste_file = open(name, "w")
            copy_file_text = open(path_copy).read()
            paste_file.write(copy_file_text)
            paste_file.close()


copy("kk.py", "servers/15/main.py")
