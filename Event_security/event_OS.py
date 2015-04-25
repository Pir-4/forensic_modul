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
            # passwd = getpass.getpass("[sudo] password for %s: " % user)
            # msg = user + ':' + passwd
            # os.system('su')
        else:
            print("gooooood roooooooooooooot")

        euid = os.geteuid()
        print('Running. Your euid is', euid)

    def open_log_auth(self):
        if self._system == "Linux":
            """открываем лог файл auth (пока свой,тестовый)"""
            path = "/home/valentin/projects/git_projects/forensic_modul/Event_security/auth_test.log"
            auth = open(path,'r')
            other = auth.readlines()
            auth.close()

            #образуем список всех событий, которые имеют (сессию [number])
            d = {}
            for line in other:
                type = self.get_type(line)
                if d.get(type,None) == None:
                    d[type] = 1
                else:
                    d[type] += 1

            key = d.keys()

            groups = []
            for type in key:
                i = d.get(type,0)
                tmp = []
                for line in other:
                    if type == self.get_type(line) and i != 0:
                        tmp.append(line)
                        i -= 1
                    elif i == 0:
                        break
                groups.append(tmp)
            for line in groups:
                print(self.parsing_msg_su(line))

    def get_date(self,msg):
        """возвращает дату из поступившего сообщения"""
        # print(msg)
        st = msg.find(" ",0,len(msg))
        st = msg.find(":",st+1,len(msg))
        st = msg.find(" ",st+1,len(msg))
        return msg[:st]

    def get_type(self,msg):
        """возращяет сесии сообщения"""
        st = msg.find("[",0,len(msg))
        point = msg.find(":",len(self.get_date(msg)),len(msg))

        if st ==-1 or st > point:
            return None

        st += 1
        end = msg.find("]",st,len(msg))
        return msg[st:end]

    def parsing_msg_su(self,gmsg):
        """Разбираем блок логов (для su) (сгрупированных) на составляющие время,на какие права претндвал,
        кто щапрашивал,реультат"""

        tmp = []
        msg =""
        for line in gmsg:
            if line.find("su for",0,len(line)) != -1:
                msg = line
                break

        if msg=="": return None

        tmp.append(self.get_date(msg))
        st =msg.find("su",0,len(msg))

        if st == -1:
            return None

        st = msg.find("for",0,len(msg))+4
        end = msg.find(" ",st,len(msg))
        tmp.append("guser="+msg[st:end])

        st = msg.find("by",end,len(msg))+3
        end = msg.find(" ",st,len(msg))
        tmp.append("user="+msg[st:end])

        if -1 != msg.find("Successful",0,len(msg)):
            tmp.append("result=Successful")
        elif -1 != msg.find("FAILED ",0,len(msg)):
            tmp.append("result=FAILED")

        return tmp



event = Event_OS()
print(event.get_cef())
event.rights_root()
event.open_log_auth()
#Apr 26 01:53:01 2015