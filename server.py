import socket
from threading import Thread
from tempfile import TemporaryFile as tf

MAX = 16777215
class Connection:
	MSG = b'\x00\x00\x00\x01'
	FILE = b'\x00\x00\x00\x02'
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
		if not recv:
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
		for k in self.connlst:
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
				self.sendtoall(realm)
			elif dat == self.FILE:
				print('recv file from ', obj.addr)
				size = int.from_bytes(obj.recv(3), byteorder='big', signed=0)
				print('The size is', size)
				times, modd = size // self.BUFF, size % self.BUFF
				print(times, 'times', 'ssy', modd)
				fp = tf()
				for k in range(times):
					fp.write(obj.recv(self.BUFF))
				fp.write(obj.recv(modd))
				fp.seed(0)
				filer = fp.read()
				fp.close()
				self.sendtoall(self.FILE)
			else:
				obj.p

	def mianloop(self):
		while 1:
			conn, addr = self.socket.accept()
			obj = Connection(addr, conn, self.now_id, self.popfun)
			self.connlst.append(obj)
			Thread(target=self.connth, args = (obj,)).start()
			self.now_id += 1
