def copy(name: str):
    copy_path = "мессанджер_vt/test/copy_file.py"
    paste_path = f"мессанджер_vt/test/servers/{name}/main.py"
    try:
        open(paste_path)
        return b"server is already done"
    except:
        paste_file = open(paste_path, "w")
        copy_file_text = open(copy_path).read()
        paste_file.write(copy_file_text)
        paste_file.close()
        return b"server made"

