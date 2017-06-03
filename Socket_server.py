import socket
import threading

print('server start...')
class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        threading.Thread(target = self.listenToClient).start()

    def listenToClient(self):

        while True:
            connection,address = self.sock.accept()
            try:
                connection.settimeout(60)
                buf = connection.recv(1024)
                print(buf.decode("utf-8"))

                s = "OKkkkkkk"
                connection.send(s.encode('utf-8'))
            except socket.timeout:
                print('time out')
            connection.close()
        # size = 1024
        # while True:
        #     try:
        #         data = client.recv(size)
        #         if data:
        #             # Set the response to echo back the recieved data
        #             response = data
        #             client.send(response)
        #         else:
        #             raise error('Client disconnected')
        #     except:
        #         client.close()
        #         return False

if __name__ == '__main__':
    
    threadServer = ThreadedServer('127.0.0.1',8001)
    # while True:
    #   print("1")
