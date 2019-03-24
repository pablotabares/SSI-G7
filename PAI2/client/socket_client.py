#!/usr/bin/env python3
import socket

def connect_and_send(msg):
    # Se establece la conexion
    s = socket.socket()
    s.connect(("localhost", 8000))
    # Se solicita al usuario el mensaje a enviar
    s.send(msg.encode())
    # Se recibe la respuesta y se escribe en pantalla
    datos = s.recv(1000)
    s.close()
