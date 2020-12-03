import socket

class Connection:
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
			return
		return recv

	def header(self, _type, fle):
		_len = len(fle)