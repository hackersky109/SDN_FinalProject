from __future__ import print_function
import os
import psutil
import socket

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 8001))
    pid = os.getpid()
    py = psutil.Process(pid)
    now_CPU = 0.0
    #memoryUse = py.memory_info()[0]/2.0**30  # memory use in GB...I think
    memoryUse = psutil.virtual_memory().percent
    print("memoryUse = ")

    print(memoryUse)
    # print(psutil.cpu_percent(interval=1, percpu=False))
    # print(psutil.virtual_memory()) #  physical memory usage
    # print(psutil.virtual_memory().used)
    # print('memory use:', memoryUse)
    while True:
        now_CPU = psutil.cpu_percent(interval=1, percpu=False)
        print(now_CPU)
        if(now_CPU!=0.0):
          break
    string = str(now_CPU)+","+str(memoryUse)
    print(string)
    sock.send(string.encode('utf-8'))
    str = sock.recv(1024)
    print(str.decode("utf-8"))
    sock.close()
