import socket
import struct
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("127.0.0.1",3008))
server.listen(3)
while True:
    print("start.......")
    sock,adddr = server.accept()
    d = sock.recv(struct.calcsize("l"))
    total_size = struct.unpack("l",d)
    num  = total_size[0]//1024
    data = b''
    for i in range(num):
        data += sock.recv(1024)
    data += sock.recv(total_size[0]%1024)

    with open("recv/a.png","wb") as f:
        f.write(data)
    sock.close()
sock.close()