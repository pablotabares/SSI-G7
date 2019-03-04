import os

def rename(first):
    file = open("log" + first + ".txt","a")
    file.write("hi"+ "\n")
    file.close()

rename("mama")