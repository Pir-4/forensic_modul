__author__ = 'valentin'
# -*- coding:utf-8 -*-
#поределяет вид операционной системы и работает с ее событиями безопасности
#!/usr/bin/env python
import sys
import platform
import os
import getpass

class Event_OS():
    def __init__(self):
        self._system = str(platform.system())
        self._info_system = self.info_sistem()

    def info_sistem(self):
        """возврящает вендора,"""
        tmp =[]
        if self._system =="Linux":
            tmp.append(self._system)
            dist = platform.dist()
            tmp.append(str(dist[0])+"-"+dist[1])
            tmp.append(str(platform.version()))
        elif self._system == "Windows":
            tmp.append("Microsoft")
            device = platform.platform()
            st = len(self._system)+1
            point = str.find("-",st,len(device))
            tmp.append(device[:point])
            tmp.append(str(platform.version()))
        else:
            return None

        return tmp


    def get_cef(self):
        """получем сообщение в формате cef"""
        tmp =""
        for info in self._info_system:
            tmp += info+"|"
        return tmp
    def rights_root(self):
        """скрипт на запрос прав root если их нет"""
        euid = os.geteuid()
        print(euid)
        if euid != 0:
            user = "root"
            passwd = getpass.getpass("[sudo] password for %s: " % user)
            msg = user + ':' + passwd
            sys.stdin('su')
            # home = os.path.expanduser('~')
            # script = sys.argv[0]

        # euid = os.geteuid()
        # print('Running. Your euid is', euid)
    def open_log_auth(self):
        """открываем лог файл auth"""
        # auth = open('/var/log/auth.log','r')
        # print(auth)


event = Event_OS()
print(event.get_cef())
event.rights_root()
# event.open_log_auth()