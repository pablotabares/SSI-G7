import os
import datetime


def logger(file_name, log_name):
    print("Hi")
    now = datetime.datetime.now()

    file0 = open(log_name, "r")
    first = file0.read(7)
    file0.close()

    month = first[5:7]

    print("Current month: " + str(now.month))
    print("Creation month: " + month)

    if(int(month) < 6):
        if(int(month) + 6 > now.month):
            file = open(log_name, "a")
            file.write(now.strftime('%Y-%m-%d %H:%M:%S') + " " + file_name + "\n")
            file.close()
        else:
            rename(log_name)
            file = open("log" + first + ".txt", "a")
            file.write(now.strftime('%Y-%m-%d %H:%M:%S') + " " + file_name + "\n")
            file.close()
    else:
        if(now.month + 6 < int(month)):
            file = open(log_name, "a")
            file.write(now.strftime('%Y-%m-%d %H:%M:%S') + " " + file_name + "\n")
            file.close()
        else:
            rename(log_name)
            file = open("log" + first + ".txt", "a")
            file.write(now.strftime('%Y-%m-%d %H:%M:%S') + " " + file_name + "\n")
            file.close()


def rename(file_name):
    pre, ext = os.path.splitext(file_name)
    os.rename(file_name, pre + ".bak")


logger("Archivo", "ok.txt")
