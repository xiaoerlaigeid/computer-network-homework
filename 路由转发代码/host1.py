# -*- coding:utf-8 -*-
from Tkinter import *
import socket
import threading
''' 
    --127.0.0.1
'''
class Transport:
    def __init__(self):
        #ui
        self.root = Tk()
        self.root.title('HOST1')
        self.createWindow(self.root)
        t = threading.Thread(target = self.recvMsg, args = (self,))
        t.start()
        self.root.mainloop()

    def createWindow(self, root):
        #提示label
        self.lbin = Label(root, text = '选择主机并填写数据')
        self.lbin.grid(row = 0, column = 0, columnspan = 2)
        
        #输入框
        self.Data = StringVar()
        self.entry = Entry(root, width = 50, textvariable = self.Data)
        self.entry.grid(row = 1, column = 0, columnspan = 2)
        
        #单选框
        self.radioVar = StringVar()
        self.radio1 = Radiobutton(root, text = 'Host2', 
            command = self.ClickRadiobutton, value = '127.0.1.1|30010|Host1|Host2|', variable = self.radioVar)
        self.radio1.grid(row = 2, column = 0, sticky = E, ipadx = 10)

        self.radio2 = Radiobutton(root, text = 'Host3', 
            command = self.ClickRadiobutton, value = '127.0.2.1|30020|Host1|Host3|', variable = self.radioVar)
        self.radio2.grid(row = 2, column = 1, sticky = W, padx = 10)

        #发送按钮
        self.btsend = Button(root, text = '发送', command = self.sendMsg)
        self.btsend.grid(row = 3, column = 1)

        #显示文本
        self.textout = Text(root)
        self.textout.grid(row = 4, column = 0, columnspan = 2, 
            sticky = (W,E,N,S), padx = 10, pady = 10, ipadx = 10, ipady = 10)
        
    #只能向router1
    def sendMsg(self):
        data = self.radioVar.get() + self.Data.get()
        t_sdata = self.radioVar.get().split('|')
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.sendto(data, ('127.0.0.2', 40000))
        self.textout.insert(END, '向' + t_sdata[3] + '发送: ' + self.Data.get() + '\n')
        client.close()

    def recvMsg(self,theSystem):
        ADDR = ('127.0.0.1', 30000)
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(ADDR)
        
        #接收
        while True:
            data, addr = server.recvfrom(2048)
            t_data = data.split('|')
            self.textout.insert(END, '收到' + t_data[2] + '的数据: ' + t_data[4] + '\n')

    def ClickRadiobutton(self):
        pass

Transport()