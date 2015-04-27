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
                tmp = self.parsing_msg_su(line)
                if tmp != None:
                    # print(tmp)
                    tmp[0]
                else:
                    tmp = self.parsing_msg_kdm(line)
                    if tmp != None: print(tmp)

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
        st += 1
        end = msg.find("]",st,len(msg))
        stri = msg[st:end]
        try:
            value = int(stri)
            return str(value)
        except:
            return None

    def parsing_msg_su(self,gmsg):
        """Разбираем блок логов (для su) (сгрупированных) на составляющие время,на какие права претндвал,
        кто щапрашивал,реультат"""
        st =gmsg[0].find("su",0,len(gmsg[0]))
        if st == -1: #сообщения формата su или нет
            return None

        tmp = []
        msg =""
        msgc=""

        for line in gmsg:
            if line.find("su for",0,len(line)) != -1:
                msg = line
            if line.find("session closed",0,len(line)) != -1:
                msgc = line

        if msg=="": return None

        tmp.append(self.get_date(msg)) #записываем дату сообщения

        # находим на на кого притендовал пользователь (root-а)
        st = msg.find("for",0,len(msg))+4
        end = msg.find(" ",st,len(msg))
        tmp.append("guser="+msg[st:end])

        #находим какой пользователь претендовал на поуления прав
        st = msg.find("by",end,len(msg))+3
        end = msg.find(" ",st,len(msg))
        tmp.append("user="+msg[st:end])

        #проверка на успешность входа
        if -1 != msg.find("Successful",0,len(msg)):
            tmp.append("result=Successful")
        elif -1 != msg.find("FAILED ",0,len(msg)):
            tmp.append("result=FAILED")

        # если сессия был завершина то ствим пометку в виде времени и того что она была завершина
        if  msgc != "":
            tmp.append(self.get_date(msgc))
            tmp.append("result=close")

        return tmp

    def parsing_msg_kdm(self,gmsg):
        """Разбираем сообщаня, образоываные привходе в систему: дата,кто,результат"""
        st =gmsg[0].find("kdm:",0,len(gmsg[0]))
        if st == -1: #сообщения формата kdm или нет
            return None

        tmp = []
        for line in gmsg:
            res = None
            if line.find("authentication failure;",0,len(line)) != -1:
                res= False
            elif line.find("session opened",0,len(line)) != -1:
                res= True

            if res != None:
                tmp.append(self.get_date(line))

                st = line.find("ruser",0,len(line))+5
                if st == -1 : st = 0

                st = line.find("user",st,len(line))+5
                end = line.find(" ",st,len(line))
                if end == -1 :
                    if line.find("\n",st,len(line)) :
                        end = len(line)-1
                    else: end= len(line)

                tmp.append("user="+line[st:end])

                if res:
                    tmp.append("result=Successful")
                else:
                    tmp.append("result=FAILED")
        return tmp


event = Event_OS()
print(event.get_cef())
event.rights_root()
event.open_log_auth()
