import time


def version_control(v_path, flag=False):
    t = time.localtime(time.time())
    data = time.strftime('%m%d', t)

    with open(v_path, 'r', encoding='utf-8') as file:
        version_line = file.readline()
    v_ = "01"
    if version_line is None or version_line[:4] != data:
        v_ = "01"
    elif flag:
        v = int(version_line[4:])
        v_ = '{:02d}'.format(v+1)
    version = data+v_
    with open(v_path, 'w', encoding='utf-8') as file:
        file.write(f"{data+v_}\n")
    return version


if __name__ == '__main__':
    version_control("../res/version.txt")
