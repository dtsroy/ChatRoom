import socket

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
			return
		return recv

	def header(self, _type, fle):
		if _type == 'msg':
			self.send(self.MSG)
		elif _type == 'file':
			self.send(self.FILE)
		_len = len(fle)