import os
import sys


BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
Res_Path = os.path.join(BASE_DIR, "res")
file_path = os.path.join(Res_Path, "data.csv")
pic_path = os.path.join(BASE_DIR, "pic")
Log_Path = os.path.join(Res_Path, "logs")
Version_Path = os.path.join(Res_Path, "version.txt")

