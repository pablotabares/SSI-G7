#!/usr/bin/python
# -*- coding: utf-8 -*-

##############################################
## Script para enviar un correo electrónico ##
##############################################

# Importación de la librería necesaria para el envío de correos
import smtplib

def sendMail(dst, sub, msg):
	# << Montaje del correo electrónico
	email = """From: %s
To: %s
MIME-Version: 1.0
Content-type: text/html
Subject: %s
%s
""" %('ssii.g7.etsii.us@gmail.com', dst, sub, msg)
# >> Fin del montaje del correo electrónico

	# << Envío del correo
	# Apertura del servido SMTP en el servidor de correo electrónico de origen
	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		try:
			# Inicio de sesión en el servidor de correo electrónico de origen.
			server.login('ssii.g7.etsii.us@gmail.com', 'hcXDPhBNYD')
			try:
				# Envío del correo electrónico
				server.sendmail('ssii.g7.etsii.us@gmail.com', dst, email)
			except Exception as e:
				print(e)
				print('Error al enviar el correo electrónico')
		except:
			print('Error al iniciar sesión en GMail')
		# Cierre del servidor SMTP
		server.quit()
	except:
		print('Error al iniciar el servidor SMTP')
	# >> Fin del envío del correo

######################
##  FIN DEL SCRIPT  ##
######################
