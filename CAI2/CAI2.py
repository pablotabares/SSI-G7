#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import random

def sha1_encrypt(cadena):
	hash = hashlib.sha1(cadena)
	hash.update('2345678902 98765421 3000')
	return hash.hexdigest()

def password_generate(length,string):
	index = 0
	random_char = ""
	while (index < length):
		random_char += random.choice(string)
		index = index + 1
	return random_char

def check_hash():
	

print sha1_encrypt(password_generate(8,'abcdefghijklmnopqrstuvwxyz0123456789'))
