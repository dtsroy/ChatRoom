from socket import socket
from threading import Thread as th
from sys import argv
from json import dumps

canjixu = 1
HOST = argv[1]
begin = int(argv[2])
jieshu = int(argv[3])

class Link:
	def __init__(self, addr):
		self.socket = socket()
		self.addr = addr
		
	def _tryto(self):
		global canjixu
		try:
			if canjixu:
				self.socket.connect(self.addr)
				self.socket.send('request:connect to server'.encode('utf-8'))
				if self.socket.recv(1024).decode('utf-8') == 'response:pass':
					canjixu = 0
					print('FIND!!!')
					print(self.addr)
					with open('ServerAddress.txt', 'w+') as f:
						f.write(repr(self.addr))
		except Exception as e:
			print('ERROR!!!')
			print(e, self.addr)
		self.socket.close()
		
class Thsec:
	def __init__(self, start, end):
		self.start, self.end = start, end
	
	def run(self):
		global HOST
		for m in range(self.start, self.end + 1):
			if canjixu:
				th(target = Link((HOST, m))._tryto, args = ()).start()
			else:
				break

def split(_1, _2):
	if _1 % 100 != 0 or _2 % 100 != 0:
		raise Exception('开始和结束必须为100的倍数')
	b = _1 // 100
	e = _2 // 100
	li=[]
	for k in range(b, e):
		li.append([k * 100, k * 100 + 99])
	#print(li)
	return li
		
def main():
	for k in split(begin, jieshu):
		if canjixu:
			Thsec(k[0], k[1]).run()
		else:
			break
			
if __name__ == '__main__':
	main()
