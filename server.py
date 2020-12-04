import socket
from threading import Thread

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
		self.conn.send(msg)

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
	def __init__(self, addr):
		self.socket = socket.socket()
		self.socket.bind(addr)
		self.socket.listen(5)
		self.connlst = []
		self.now_id = 0

	def popfun(self, _id):
		self.connlst.pop(_id)

	def connth(self, obj):
		while 1:
			dat = obj.recv(4)

	def mianloop(self):
		while 1:
			conn, addr = self.socket.accept()
			obj = Connection(addr, conn, self.now_id, self.popfun)
			self.connlst.append(obj)
			Thread(target=self.connth, args = (obj,)).start()
			self.now_id += 1
