from __future__ import print_function
import os
import psutil
import socket
import time
now_CPU = 10
def Send_Stastic():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.2.48', 8001))
    # pid = os.getpid()
    # py = psutil.Process(pid)
    # now_CPU = 0.0
    memoryUse = psutil.virtual_memory().percent
    #print("memoryUse = ")

    #print(memoryUse)
    # while True:
    #     now_CPU = psutil.cpu_percent(interval=1, percpu=False)
    #     #print(now_CPU)
    #     if(now_CPU!=0.0):
    #       break

    now_CPU+=10
    string = str(now_CPU)+","+str(memoryUse)+",server2"
    #print(string)
    print("CPU = "+str(now_CPU))
    sock.send(string.encode('utf-8'))
    stri = sock.recv(1024)
    print("Response = "+stri.decode("utf-8"))
    sock.close()
if __name__ == '__main__':
    while True:
      Send_Stastic()
      time.sleep(1)
