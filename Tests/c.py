import socket 
import struct
import os
import json
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("127.0.0.1",3008))
print("connect success....")
filepath = "a.png"
size =  os.stat(filepath).st_size
f= struct.pack("l",os.stat(filepath).st_size)
client.send(f)
img = open(filepath,"rb")
client.sendall(img.read())
img.close()
client.close()