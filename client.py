import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server machine and port.
#
# API: connect(address)
#   connect to a remote socket at the given address.
server_ip = '127.0.0.1'
server_port = 8181
s.connect((server_ip, server_port))
print('Connected to server ', server_ip, ':', server_port)

bufsize = 16
count = 0
data = bytearray()
data.append(2)
exp1 = '3+12'
exp2 = '1+12/3'
data.append(len(exp1))
data.append(exp1.encode('utf-8'))
data.append(len(exp2))
data.append(exp2.encode('utf-8'))
s.sendall(data)
data = s.recv(bufsize)
print('Client received:', data)

s.close()