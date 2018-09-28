# This example is using Python 3
import socket
import time
import thread
import struct

# Get host name, IP address, and port number.
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_port = 8010

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
            stack.append(stack.pop() / num)
    
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

bufsize = 16
def handler(conn):
    while True:
        data = conn.recv(2)
        if not data: break
        exp_num = struct.unpack('!h', data)
        count = 2
        ans = bytearray()
        ans += struct.pack('!h', exp_num)
        print(exp_num)
        # for i in range(0, exp_num):
        #     exp_len = struct.unpack('!h', conn.recv(2))
        #     count += 2
        #     exp = ''
        #     if count + exp_len <= bufsize:
        #         exp += conn.recv(exp_len).decode('utf-8')
        #         count += exp_len
        #     else: 
        #         exp += conn.recv(bufsize - count).decode('utf-8')
        #         count = exp_len + count - bufsize
        #         exp += conn.recv(count).decode('utf-8')
        #     res = calc(exp)
        #     ans += struct.pack(len(res))
        #     ans += res.encode('utf-8')
        # conn.sendall(ans)
    conn.close()

while True:
    conn, addr = s.accept()
    print('Server connected by', addr,'at', now())
    thread.start_new(handler, (conn,))