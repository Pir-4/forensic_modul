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
        self._manag_bd = manager_db.Manager()

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
        tmp = str_cef[:21] + str(address[0]) + str_cef[25:]
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

            self._manag_bd.dispatcher(data)
            reply = str(self.now())
            connection.send(reply.encode("utf-8"))
        connection.close()


sev = Server()
sev.dispecher()