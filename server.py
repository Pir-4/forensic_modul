__author__ = 'Valentin'
# -*- coding:utf-8 -*-
# server tcp

import time
import thread as thread
from socket import *

from Work_db import manager_db


class Server():
    def __init__(self, myHost='', myPort=8080):
        """creating socket"""
        self._sockobj = socket(AF_INET, SOCK_STREAM)
        self._sockobj.bind((myHost, myPort))
        self._sockobj.listen(5)
        self.manag_bd = manager_db.Manager()


    def __del__(self):
        """closing socket"""
        self._sockobj.close()

    def dispecher(self):
        """receiving clients and their distribution in the processing flow"""
        while True:
            connection, address = self._sockobj.accept()
            print('server connected by', address)
            print('at', self.now())
            thread.start_new(self.handleClient, (connection, address,))

    def now(self):
        """Getting the current time on the server"""
        return time.ctime(time.time())

    def change_host(self, str_cef, address):
        """Replacing format CEF field host to the IP address of the client"""
        tmp = str_cef
        if str_cef.find("CEF:",0,len(str_cef)) != -1:
            tmp = str_cef[:21] + str(address[0]) + str_cef[25:]

        elif str_cef.find("|",0,len(str_cef)) != -1:
            st = str_cef.find("|",0,len(str_cef))
            st = str_cef.find("|",st+1,len(str_cef))
            tmp = str_cef[:st+1]+str(address[0])+"|"+str_cef[st+1:]
        return tmp


    def handleClient(self, connection, address):
        """Processing a request from an individual customer"""
        # time.sleep(5) #server Action
        while True:
            try:
                data = connection.recv(1024).decode("utf-8")
            except:
                print('client disconnect: ', address, 'at', self.now())
                data = ""

            if not data: break

            data = self.change_host(data, address)
            result = self.manag_bd.dispatcher(data)

            mutex = thread.allocate_lock()


            if type(result)==type(list()):
                mutex.acquire() #Lock interrupt
                l = len(result)
                reply = str(l)
                connection.send(reply.encode("utf-8"))
                for line in result:
                    time.sleep(0.0025)
                    reply = line
                    connection.send(reply.encode("utf-8"))
                mutex.release()# permission to interrupt
            else:
                reply = str(self.now())
                connection.send(reply.encode("utf-8"))



        connection.close()


sev = Server()
sev.dispecher()