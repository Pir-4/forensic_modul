 #__author__ = 'Valentin'
 # -*- coding:utf-8 -*-
#клиентская часть

from socket import *
import event_generator

class Client():
    def  __init__(self,serverHost= 'localhost',serverPort=8080):
        self._sockobj = socket(AF_INET,SOCK_STREAM)

        try:
            self._sockobj.connect((serverHost,serverPort))
            self.isConnect = True
        except:
            self.isConnect = False

    def send_message(self,mess):
        self._sockobj.send(mess.encode("utf-8"))

    def recv_message(self):
        data = self._sockobj.recv(1024).decode("utf-8")
        return data

    def move_client(self):
        while self.isConnect:
            data = str(input("message: "))
            if data =="1": data = event_generator.get_Antivir()
            elif data == "2": data = event_generator.get_OS()
            elif data == "3": data = event_generator.get_OS_ip()
            self.send_message(data)
            print(self.recv_message())

    def __del__(self):
        self._sockobj.close()

# cli = Client()
# cli.move_client()

