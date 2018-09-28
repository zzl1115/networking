# This example is using Python 3
import socket
import time
import _thread
import struct

# Get host name, IP address, and port number.
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_port = 8048

# Make a TCP socket object.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to server IP and port number.
s.bind(('127.0.0.1', host_port))

# Listen allow 10 pending connects.
s.listen(20)

print('\nServer started. Waiting for connection...\n')

# Current time on the server.
def now():
    return time.ctime(time.time())

def calc(s):  
    def update(op, num):
        if op == '+':
            stack.append(num)
        elif op == '-':
            stack.append(-num)
        elif op == '*':
            stack.append(stack.pop() * num)
        elif op == '/':
            stack.append(stack.pop() // num)
    
    stack = []
    num, op = 0, '+'
    for i in range(len(s)):
        if s[i].isdigit():
            num = num * 10 + int(s[i])
        elif s[i] in ['+', '-', '*', '/', ')']:
            update(op, num)
            if s[i] == ')':
                num = 0
                while isinstance(stack[-1], int):
                    num += stack.pop() 
                op = stack.pop()
                update(op, num)
            num, op = 0, s[i]
        elif s[i] == '(':
            stack.append(op)
            num, op = 0, '+'
    update(op, num)
    return str(sum(stack))

def recvall(conn, bufsize):
    data = b''
    while True:
        part = conn.recv(bufsize)
        data += part
        if len(part) < bufsize:
            break
    return data

def process_data(data):
    ans = b''
    exp_num = struct.unpack('!h', data[0: 2])[0]
    pos = 2
    ans += struct.pack('!h', exp_num)
    for i in range(0, exp_num):
        exp_len = struct.unpack('!h', data[pos: pos + 2])[0]
        pos += 2
        exp = data[pos: pos + exp_len].decode('utf-8')
        pos += exp_len
        res = calc(exp)
        print(exp + '=' + res)
        ans += struct.pack('!h', len(res))
        ans += res.encode('utf-8')
    return ans

def mysendall(conn, ans, bufsize):
    pos = 0
    end = len(ans)
    while end > pos:
        if pos + bufsize > end:
            conn.sendall(ans[pos: end])
        else: conn.sendall(ans[pos: pos + 16])
        pos += 16

def handler(conn):
    bufsize = 16
    data = recvall(conn, bufsize)
    ans = process_data(data)
    mysendall(conn, ans, bufsize)
    conn.close()    


while True:
    conn, addr = s.accept()
    print('Server connected by', addr,'at', now())
    _thread.start_new(handler, (conn,))