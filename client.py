import socket
from threading import Thread
from tempfile import TemporaryFile as tf
import os

MAX = 16777215
LOCAL = ('127.0.0.1', 10092)

class Client:
	MSG = b'\x00\x00\x00\x01'
	FILE = b'\x00\x00\x00\x02'
	CLOSE = b'\x00\x00\x00\x03'
	BUFF = 8192

	def __init__(self, addr):
		self.addr = addr
		self.socket = socket.socket()
		self.socket.connect(addr)
		self.socket.send(b'dmct')
		print('Connect to server success!')

	def send(self, msg):
		self.socket.sendall(msg)

	def recv(self, buff):
		recv = self.socket.recv(buff)
		if not recv or recv == self.CLOSE:
			self.send(self.CLOSE)
			self.socket.close()
			os.system('taskkill /f /im python.exe')
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
				self.send(self.MSG)
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
				self.send(self.FILE)
				self.send(len(fb).to_bytes(length=3, byteorder='big', signed=0))
				self.send(fb)
				print('suc.')
			else:
				print('Command cloud not be found.')
				continue

	def mainloop_recv(self):
		while 1:
			s = self.recv(4)
			#print(s)
			if s == self.MSG:
				dat = eval(self.recv(32768).decode())
				print(dat[0], ': ', dat[1].decode())
			elif s == self.FILE:
				size = int.from_bytes(self.recv(3), byteorder='big', signed=0)
				print('The size is', size)
				times, modd = size // self.BUFF, size % self.BUFF
				print(times, 'times,', 'other', modd)
				fp = tf()
				for k in range(times):
					fp.write(self.recv(self.BUFF))
				fp.write(self.recv(modd))
				fp.seek(0)
				filer = eval(fp.read().decode())
				fp.close()
				print('recv file from ', filer[0])
				datt = eval(filer[1].decode())
				print('file name is', datt[0], 'saving in recv/%s' % datt[0])
				try:
					os.mkdir('recv/')
				except Exception as e:
					print(e)
					#continue
				with open('recv/%s' % datt[0], 'wb+') as f:
					f.write(datt[1])
				print('save suc.')

	def main(self):
		Thread(target=self.mainloop_send).start()
		Thread(target=self.mainloop_recv).start()

c = Client(LOCAL)
c.main()
