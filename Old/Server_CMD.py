from socket import socket
from threading import Thread as th
import json
from sys import argv

class TCPLink(object):
	def __init__(self, connection, address, allfunc):
		self.socket = connection
		self.addr = address
		self.func = allfunc
		
		if self.socket.recv(1024).decode('utf-8') == 'request:connect to server':
			self.socket.send('response:pass'.encode('utf-8'))
			self.cansend = 1
		else:
			self.socket.send('You has no connect permission.'.encode('utf-8'))
			self.socket.close()
			self.cansend = 0
		
	def thread_(self):
		while self.cansend:
			data = self.socket.recv(1024).decode('utf-8')
			if data != '':
				data = json.loads(data)
				if data['type'] == 's.b.in':
					self.func((data['name'] + ' come in').encode('utf-8'))
					continue
				if data['type'] == 's.b.out':
					self.func((data['name'] + ' out').encode('utf-8'))
					self.socket.close()
					self.cansend = 0
					break
				if data['type'] == 'msg':
					self.func((data['name'] + ':' + data['msg']).encode('utf-8'))
					continue
			else:
				self.socket.close()
				self.cansend = 0
				break
	
	def main(self):
		th(target = self.thread_, args = ()).start()

class SERVER(object):
	def __init__(self, port):
		self.LOCAL = ('localhost', port)
		self._server = socket()
		self._server.bind(self.LOCAL)
		self.clients = []
		self.index = 0
		self._server.listen(100)
		
	def _all(self, msg):
		for m in self.clients:
			if m.cansend:
				try:
					m.socket.send(msg)
				except Exception as e:
					print('error.', e)
		
	def main(self):
		while True:
			conn, addr = self._server.accept()
			print(addr)
			tcp = TCPLink(conn, addr, self._all)
			self.clients.append(tcp)
			tcp.main()
		
if __name__ == '__main__':
	SERVER(int(argv[1])).main()
