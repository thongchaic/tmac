import socket 
def get(ip,params):
    addr = socket.getaddrinfo(ip, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET %s HTTP/1.0\r\nHost: %s\r\n\r\n' % (params, ip), 'utf8'))
    while True:
        data = s.recv(1024)
        if data:
            pass
        else:
            break
    s.close()
    
def http_post():
    pass