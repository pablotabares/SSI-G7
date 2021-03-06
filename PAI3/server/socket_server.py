#!/usr/bin/env python3
import socket
import ssl
from threading import Thread
import server as serverfunctions

#Clase con el hilo para atender a los clientes.
#En el constructor recibe el socket con el cliente y los datos del cliente para escribir por pantalla
class Cliente(Thread):
    def __init__(self, conn, datos_cliente):
        Thread.__init__(self)
        self.datos = datos_cliente
        self.conn = conn

    # Bucle para atender al cliente.
    def run(self):
        #Pedimos el email y lo recibimos
        self.conn.send('Email:'.encode())
        mail = self.conn.recv(1000).decode()

        #Pedimos la pass y la recibimos
        self.conn.send('Password:'.encode())
        pwd = self.conn.recv(1000).decode()

        #Comprobamos las credenciales y enviamos el resultado
        [success, msg, acc] = serverfunctions.login(mail, pwd)
        print(msg)
        self.conn.send('true'.encode() if success else 'false'.encode())
        self.conn.send(msg.encode())

        #En caso de que sean erroneas cerramos la conexion
        if not success:
            print ("Conexión cerrada con "+str(self.datos))
            self.conn.shutdown(2)
            self.conn.close()
            return

        #Recibimos la transferencia y la procesamos
        peticion = self.conn.recv(1000).decode()
        print (str(self.datos)+ " dice: "+peticion)
        [code, msg] = serverfunctions.receive(peticion, acc)

        #Imprimimos el resultado y se lo enviamos al cliente
        print(msg)
        self.conn.send(msg.encode())

        #Cerramos la conexión
        self.conn.shutdown(2)
        self.conn.close()
        print ("Conexión cerrada con "+str(self.datos))


if __name__ == '__main__':
    # Aseguramos que el sistema está instalado
    serverfunctions.initialize_db()
    # Se prepara el servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    server.bind(("", 443))
    server.listen(1)
    print ("Esperando conexiones...")

    # bucle para atender clientes
    while True:
        # Se espera a un cliente
        socket_cliente, datos_cliente = server.accept()
        try:
                conn = ssl.wrap_socket(socket_cliente, server_side=True, certfile = "cert/server.crt", keyfile="cert/server.key", ssl_version = ssl.PROTOCOL_TLSv1_2)

                # Se escribe su informacion
                print ("Conexión establecida con "+str(datos_cliente))
                # Se crea la clase con el hilo y se arranca.
                hilo = Cliente(conn, datos_cliente)
                hilo.start()
        except:
                print('Exception')
