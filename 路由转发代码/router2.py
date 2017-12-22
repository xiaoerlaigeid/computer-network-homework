# -*- coding:utf-8 -*-
from Tkinter import *
import socket
import threading
''' 
    --127.0.1.2
'''
routing_table = [
    ['127.0.1.1', '127.0.1.1', 30010],
    ['127.0.0.1', '127.0.0.2', 40000],
    ['127.0.2.1', '127.0.2.2', 40020]
]
class Transport:
    def __init__(self):
        self.root = Tk()
        self.root.title('Routing2')
        self.createWidgets(self.root)
        t = threading.Thread(target = self.recvMsg, args = (self,))
        t.start()
        self.root.mainloop()

    def createWidgets(self, root):
        #显示文本
        self.textout = Text(root)
        self.textout.grid(row = 0, column = 0, columnspan = 2, sticky = (W,E,N,S), 
            padx = 10, pady = 10, ipadx = 10, ipady = 10)

        #信息
        self.lbdes = Label(root, text = '目标主机')
        self.lbdes.grid(row = 1, column = 0, sticky = E, ipadx = 20)
        self.lbnext = Label(root, text = '下一跳')
        self.lbnext.grid(row = 1, column = 1, sticky = W, padx = 20)
        self.lbdinfo1 = Label(root, text = 'Host1  ')
        self.lbdinfo1.grid(row = 2, column = 0, sticky = E, ipadx = 20)
        self.lbninfo1 = Label(root, text = 'Router1')
        self.lbninfo1.grid(row = 2, column = 1, sticky = W, padx = 20)
        self.lbdinfo2 = Label(root, text = 'Host3  ')
        self.lbdinfo2.grid(row = 3, column = 0, sticky = E, ipadx = 20)
        self.lbninfo2 = Label(root, text = 'Router3')
        self.lbninfo2.grid(row = 3, column = 1, sticky = W, padx = 20)
        self.lbdinfo3 = Label(root, text = 'Host2  ')
        self.lbdinfo3.grid(row = 4, column = 0, sticky = E, ipadx = 20)
        self.lbninfo2 = Label(root, text = '-')
        self.lbninfo2.grid(row = 4, column = 1, sticky = W, padx = 20)

    def sendMsg(self, desIP, desPort, data):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.sendto(data, (desIP, desPort))
        client.close()

    def recvMsg(self,theSystem):
        #一接收就调用sendMsg
        ADDR = ('127.0.1.2', 40010)
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(ADDR)

        while True:
            #接收
            data, addr = server.recvfrom(2048)
            t_data = data.split('|')
            self.textout.insert(END, t_data[2] + '->' + t_data[3] + ': ' + t_data[4] + '\n')
            #判断下一跳
            for route in routing_table:
                if t_data[0] == route[0]:
                    desIP = route[1]
                    desPort = route[2]
                    break
            self.sendMsg(desIP, desPort, data)

Transport()