import socket
from threading import Thread
from tempfile import TemporaryFile as tf
from atexit import register
from os import system

MAX = 16777215
LOCAL = ('127.0.0.1', 10092)

class Connection:
	MSG = b'\x00\x00\x00\x01'
	FILE = b'\x00\x00\x00\x02'
	CLOSE = b'\x00\x00\x00\x03'
	def __init__(self, addr, conn, _id, popf):
		print(addr)
		if conn.recv(4) != b'dmct':
			popf(_id)
			return
		self.conn = conn
		self._id = _id
		self.popf = popf

	def send(self, msg):
		self.conn.sendall(msg)

	def dell(self):
		self.conn.close()
		self.popf(self._id)

	def recv(self, buff=1024):
		recv = self.conn.recv(buff)
		if not recv or recv == self.CLOSE:
			self.dell()
			exit(0)
		return recv

class Server:
	BUFF = 8192

	def __init__(self, addr):
		self.socket = socket.socket()
		self.socket.bind(addr)
		self.socket.listen(5)
		self.connlst = []
		self.now_id = 0

	def popfun(self, _id):
		a = self.connlst.pop(_id)
		print(a.addr, "Closed.  of id:", _id)
		self.connlst.insert(_id, None)

	def sendtoall(self, msg, flag=None):
		for idx, k in enumerate(self.connlst):
			if k:
				if flag != None:
					if idx != flag:
						k.send(msg)
					else:
						print('Flag', flag, 'stoped send.')

	def connth(self, obj):
		while 1:
			dat = obj.recv(4)
			print(dat)
			if dat == self.MSG:
				print('recv msg from ', obj.addr)
				realm = obj.recv(32768)
				self.sendtoall(self.MSG)
				self.sendtoall(repr([obj.addr, realm]).encode())
			elif dat == self.FILE:
				print('recv file from ', obj.addr)
				size = int.from_bytes(obj.recv(3), byteorder='big', signed=0)
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
				self.sendtoall(self.FILE)
				# self.sendtoall(size.to_bytes(length=3, byteorder='big', signed=0))
				# self.sendtoall(filer)
				bd = repr([obj.addr, filer]).encode()
				self.sendtoall(len(bd).to_bytes(length=3, byteorder='big', signed=0))
				self.sendtoall(bd)
			else:
				obj.sendtoall(repr(obj.addr).encode() + b' has sent an unknown request.')

	def mainloop(self):
		while 1:
			conn, addr = self.socket.accept()
			obj = Connection(addr, conn, self.now_id, self.popfun)
			self.connlst.append(obj)
			Thread(target=self.connth, args = (obj,)).start()
			self.now_id += 1

print('START......')
s = Server(LOCAL)
print('Creat Server obj success.')

def ccmd():
	while 1:
		inp = input('type exit to quit.')
		if inp == 'exit':
			system('taskkill /f /im python.exe]')

Thread(target=ccmd, args=()).start()

s.mainloop()

@register
def _exit():
	s.sendtoall(b'\x00\x00\x00\x03')
	for k in s.connlst:
		k.dell()
