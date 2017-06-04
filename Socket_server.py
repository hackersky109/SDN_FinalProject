import socket
import threading

print('server start...')
# class ThreadedServer(object):
# def __init__(self, host, port):
#     self.host = host
#     self.port = port
#     self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     self.sock.bind((self.host, self.port))
#     self.sock.listen(5)
    #threading.Thread(target = self.listenToClient).start()

def init(_host,_port):
    global host, port, sock

    host = _host
    port = _port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    threading.Thread(target = listenToClient).start()

    print("Success")

def listenToClient():
    print("host = "+host)
    print("port"+str(port))

    while True:
        connection,address = sock.accept()
        try:
            connection.settimeout(60)
            buf = connection.recv(1024)
            print(buf.decode("utf-8"))

            s = "OKkkkkkk"
            connection.send(s.encode('utf-8'))
        except socket.timeout:
            print('time out')
        connection.close()
# init('127.0.0.1',8001)
