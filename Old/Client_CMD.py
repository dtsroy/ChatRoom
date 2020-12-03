from socket import socket
import json
from threading import Thread as th

PORT = int(input('port:'))
HOST = input('host:')
ADDR = (HOST, PORT)

client = socket()
client.connect(ADDR)
client.send('request:connect to server'.encode('utf-8'))
if client.recv(1024).decode('utf-8') == 'response:pass':
	print('SUC to connect to server.')
NAME = input('Your Name:')
client.send(json.dumps({'type':'s.b.in', 'name':NAME}).encode('utf-8'))

def _recv():
	while True:
		dt = client.recv(1024).decode('utf-8')
		if dt != '':
			print(dt)
		else:
			print('Server close!')
			break

def _send():
	while 1:
		msg = input('>>')
		client.send(json.dumps({'type':'msg', 'name':NAME, 'msg':msg}).encode('utf-8'))
		if msg == 'q':
			client.send(json.dumps({'type':'s.b.out', 'name':NAME}).encode('utf-8'))
			break
			
def main():
	n1 = th(target = _send, args = ())
	n2 = th(target = _recv, args = ())
	n1.start()
	n2.start()

if __name__ == '__main__':
	main()
	