#!/usr/bin/env python3
import socket
import ssl

def connect_and_send(msg):
    # Se establece la conexion
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = context.wrap_socket(sock)
    conn.connect(("localhost", 443))
    # Se solicita al usuario el mensaje a enviar
    conn.send(msg.encode())
    # Se recibe la respuesta y se escribe en pantalla
    datos = conn.recv(1000)
    conn.close()
