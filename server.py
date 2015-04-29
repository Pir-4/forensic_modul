__author__ = 'Valentin'
# -*- coding:utf-8 -*-
# сервер tcp

import time
import thread as thread
from socket import *

from Work_db import manager_db


class Server():
    def __init__(self, myHost='', myPort=8080):
        """Создание сокета"""
        self._sockobj = socket(AF_INET, SOCK_STREAM)
        self._sockobj.bind((myHost, myPort))
        self._sockobj.listen(5)
        self.manag_bd = manager_db.Manager()


    def __del__(self):
        """Закрытие сокета"""
        self._sockobj.close()

    def dispecher(self):
        """Прием клиентов и распределение их по потока обработки"""
        while True:
            connection, address = self._sockobj.accept()
            print('server connected by', address)
            print('at', self.now())
            thread.start_new(self.handleClient, (connection, address,))

    def now(self):
        """Получение текущего времени на сервере"""
        return time.ctime(time.time())

    def change_host(self, str_cef, address):
        """Замена в формате CEF поля host на IP адрес лиента"""
        if str_cef.find("CEF:",0,len(str_cef)) != -1:
            tmp = str_cef[:21] + str(address[0]) + str_cef[25:]
        else:
            st = str_cef.find("|",0,len(str_cef))
            tmp = str_cef[:st+1]+str(address[0])+"|"+str_cef[st+1:]
        return tmp


    def handleClient(self, connection, address):
        """Обработка запроса от одельного клиента"""
        # time.sleep(5) #действия сервера
        while True:
            try:
                data = connection.recv(1024).decode("utf-8")
            except:
                print('client disconnect: ', address, 'at', self.now())
                data = ""

            if not data: break

            data = self.change_host(data, address)
            print(data)

            self.manag_bd.dispatcher(data)
            reply = str(self.now())
            connection.send(reply.encode("utf-8"))
        connection.close()


sev = Server()
# sev.dispecher()
# st = "Apr 27 20:22:12|127.0.0.1|Linux|debian-7.8|#1 SMP Debian 3.2.68-1|su|user=valentin|result=Successful|"
st = "Apr 23 04:05:29|127.0.0.1|Linux|debian-7.8|#1 SMP Debian 3.2.68-1|su|user=valentin|result=FAILED|"
sev.manag_bd.dispatcher(st)