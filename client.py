import socket
from threading import Thread
from tempfile import TemporaryFile as tf

MAX = 16777215
LOCAL = ('127.0.0.1', 10092)

class Client:
	MSG = b'\x00\x00\x00\x01'
	FILE = b'\x00\x00\x00\x02'
	CLOSE = b'\x00\x00\x00\x03'
	def __init__(self, addr):
		self.addr = addr
		self.socket = socket(socket.AF_INET, socket.STREAM)
		self.socket.connect(addr)
		print('Connect to server success!')

	def send(self, msg):
		self.socket.sendall(msg)

	def recv(self, buff):
		recv = self.socket.recv(buff)
		if not recv or recv == self.CLOSE:
			self.send(self.CLOSE)
			self.socket.close()
			exit(0)
		return recv

	def mainloop_send(self):
		while 1:
			req = input('Type MSG or FILE to next')
			if req == 'MSG':
				s = input('>')
				if not s:
					print('msg mustn\'t empty.')
					continue
				#self.send(self.MSG)
				m = s.encode()
				if m.__len__() > 32768:
					print('msg file too large(more than 32768)')
					continue
				self.send(m)
				print('suc.')
			elif req == 'FILE':
				s = input('>')
				try:
					f = open(s, 'rb')
					fb = repr([s, f.read()]).encode()
					f.close()
				except Exception as e:
					print('Exception info:')
					print(e)
					continue
				if fb.__len__() > MAX:
					print('file too large(more than %d)' % MAX)
					continue
				self.send(len(fb).to_bytes(length=3, byteorder='big', signed=0))
				self.send(fb)
				print('suc.')
			else:
				print('Command cloud not be found.')
				continue

	def mainloop_recv(self):
		while 1:
			s = self.recv(4)
			if s == self.MSG:
				dat = exec(self.recv(32768))
				print(dat[0], ': ', dat[1].encode())
			elif s == self.FILE:
				size = int.from_bytes(self.recv(3), byteorder='big', signed=0)
				print('The size is', size)
				times, modd = size // self.BUFF, size % self.BUFF
				print(times, 'times,', 'other', modd)
				fp = tf()
				for k in range(times):
					fp.write(obj.recv(self.BUFF))
				fp.write(obj.recv(modd))
				fp.seek(0)
				filer = fp.read()
				fp.close()
