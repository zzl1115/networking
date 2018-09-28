import socket
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server machine and port.
#
# API: connect(address)
#   connect to a remote socket at the given address.
server_ip = '127.0.0.1'
server_port = 8048
s.connect((server_ip, server_port))
print('Connected to server ', server_ip, ':', server_port)
def create_test(list):
	data = b''
	data += struct.pack('!h', len(list))
	for i in range(0, len(list)):
		data += struct.pack('!h', len(list[i]))
		data += list[i].encode('utf-8')
	return data

def mysendall(conn, ans, bufsize):
    pos = 0
    end = len(ans)
    while end > pos:
        if pos + bufsize > end:
            conn.sendall(ans[pos: end])
        else: conn.sendall(ans[pos: pos + 16])
        pos += 16

def recvall(conn, bufsize):
    data = b''
    while True:
        part = conn.recv(bufsize)
        data += part
        if len(part) < bufsize:
            break
    return data

def print_res(rec):
	num = struct.unpack('!h', rec[0: 2])[0]
	pos = 2
	for i in range(0, num):
		len = struct.unpack('!h', rec[pos: pos + 2])[0]
		pos += 2
		res = rec[pos: pos + len]
		pos += len
		print(res.decode('utf-8'))

bufsize = 16
list = ['3+12', '3+(5-2)*3-2/(3-1)', '6/6', '8+7-5']
data = create_test(list)
mysendall(s, data, bufsize)

res = recvall(s, 16)

print_res(res)


s.close()