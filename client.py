import socket
from threading import Thread

MAX = 16777215
LOCAL = ('127.0.0.1', 10092)

class Client:
	def __init__(self, addr):
		self.addr = addr
		self.socket = socket(socket.AF_INET, socket.STREAM)
		self.socket.connect(addr)
		print('Connect to server success!')
