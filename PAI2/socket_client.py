#!/usr/bin/env python3
import socket

# Se establece la conexion
s = socket.socket()
s.connect(("localhost", 8000))
# Se solicita al usuario el mensaje a enviar
message = input('Mensaje a enviar: ')
while ("exit"!=message):
    s.send(message.encode())
    # Se recibe la respuesta y se escribe en pantalla
    datos = s.recv(1000)
    print (datos.decode())
    # Se solicita al usuario el mensaje a enviar
    message = input('Mensaje a enviar: ')

# Se envia "exit"
s.send(message.encode())
# Se espera respuesta, se escribe en pantalla y se cierra la conexion
datos = s.recv(1000)
print (datos.decode())
s.close()
