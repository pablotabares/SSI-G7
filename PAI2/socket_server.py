#!/usr/bin/env python3
import socket
from threading import Thread


#Clase con el hilo para atender a los clientes.
#En el constructor recibe el socket con el cliente y los datos del cliente para escribir por pantalla
class Cliente(Thread):
    def __init__(self, socket_cliente, datos_cliente):
        Thread.__init__(self)
        self.socket = socket_cliente
        self.datos = datos_cliente

    # Bucle para atender al cliente.
    def run(self):
      # Bucle indefinido hasta que el cliente envie "adios"
      seguir = True
      while seguir:
         # Espera por datos
         peticion = self.socket.recv(1000)

         # Contestacion
         if ("exit"!=peticion.decode()):
             print (str(self.datos)+ " dice: "+peticion.decode())
             self.socket.send("Recibido el mensaje: ".encode()+peticion)

         # Contestacion y cierre a "exit"
         if ("exit"==peticion.decode()):
             print (str(self.datos)+ " pide cerrar la conexión")
             self.socket.send("Cerrando la conexión".encode())
             self.socket.close()
             print ("Conexión cerrada con "+str(self.datos))
             seguir = False




if __name__ == '__main__':
   # Se prepara el servidor
   server = socket.socket()
   server.bind(("", 8000))
   server.listen(1)
   print ("Esperando conexiones...")

   # bucle para atender clientes
   while 1:
      # Se espera a un cliente
      socket_cliente, datos_cliente = server.accept()
      # Se escribe su informacion
      print ("Conexión establecida con "+str(datos_cliente))
      # Se crea la clase con el hilo y se arranca.
      hilo = Cliente(socket_cliente, datos_cliente)
      hilo.start()
