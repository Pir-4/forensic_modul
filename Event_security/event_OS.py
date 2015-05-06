__author__ = 'valentin'
# -*- coding:utf-8 -*-

# !/usr/bin/env python
import sys
import platform
import os
import getpass
import client
from  datetime import datetime

class Event_OS():
    def __init__(self):
        self._system = str(platform.system())
        self._info_system = self.info_sistem()
        self._dist = {}
        self.events = []
        self.last_rec = ""
        self.last_size = 0

        self.client = client.Client()

    def info_sistem(self):
        """возвращает информацию о ОС"""
        tmp = []
        if self._system == "Linux":
            tmp.append(self._system)
            dist = platform.dist()
            tmp.append(str(dist[0]) + "-" + dist[1])
            tmp.append(str(platform.version()))

        elif self._system == "Windows":
            tmp.append("Microsoft")
            device = platform.platform()
            st = len(self._system) + 1
            point = device.find("-", st, len(device))
            tmp.append(device[:point])
            tmp.append(str(platform.version()))
        else:
            return None

        return tmp


    def get_system(self):
        """получем сообщение о хра-х системы в формате cef """
        tmp = ""
        for info in self._info_system:
            tmp += info + "|"
        return tmp

    def rights_root(self):
        """скрипт на запрос прав root если их нет"""
        # euid = os.geteuid()
        # print(euid)
        # if euid != 0:
        #     user = "root"
        #     # passwd = getpass.getpass("[sudo] password for %s: " % user)
        #     # msg = user + ':' + passwd
        #     # os.system('su')
        # else:
        #     print("gooooood roooooooooooooot")

        # euid = os.geteuid()
        # print('Running. Your euid is', euid)

        if os.getuid() == 0:
            return True
        else:
            print("error: the program is started without rights root")

        return False

    def open_log_auth(self):
        if self._system == "Linux":
            """открываем лог файл auth (пока свой,тестовый)"""
            if self.rights_root():
                path = "/var/log/auth.log"
            else:
                path = "/home/valentin/projects/git_projects/forensic_modul/Event_security/auth_test.log"
        else:
            path = "C:\\Users\\Valentin\\PycharmProjects\\forensic_modul\\auth_test.txt"

        auth = open(path, 'r')
        self.other = auth.readlines()
        auth.close()
        self.last_event("", 0, 'r')  # считываем последнее событие,которое запомнили
        self.control_event()

    def formation_dist(self, msgs):
        """Составляем набор имеющихся сесиий индетификации событий"""

        for line in msgs:
            type = self.get_type(line)
            if type != None:
                if self._dist.get(type, None) == None:
                    self._dist[type] = 1
                else:
                    self._dist[type] += 1


    def formation_group(self, msgs):
        """возвраящает список сгрупированных сообщений по их номеру сессии"""
        key = self._dist.keys()
        groups = []
        for type in key:
            i = self._dist.get(type, 0)
            tmp = []
            for line in msgs:
                if type == self.get_type(line) and i != 0:
                    tmp.append(line)
                    i -= 1
                elif i == 0:
                    break
            groups.append(tmp)
        return groups

    def formation_event(self, groups):
        """форимирование из поступивших сгрупированных событий в инифицированный ввид"""
        for line in groups:
            tmp = self.parsing_msg_su(line)
            if tmp != None:
                self.events.append(tmp)
            else:
                tmp = self.parsing_msg_kdm(line)
                if tmp != None:
                    self.events.append(tmp)

    def get_date(self, msg):
        """возвращает дату из поступившего сообщения"""
        # print(msg)
        st = msg.find(" ", 0, len(msg))
        st = msg.find(":", st + 1, len(msg))
        st = msg.find(" ", st + 1, len(msg))
        return msg[:st]

    def get_type(self, msg):
        """возращяет сесии сообщения"""
        st = msg.find("[", 0, len(msg))
        st += 1
        end = msg.find("]", st, len(msg))
        stri = msg[st:end]
        try:
            value = int(stri)
            return value
        except:
            return None

    def parsing_msg_su(self, gmsg):
        """Разбираем блок логов (для su) (сгрупированных) на составляющие время,на какие права претндвал,
        кто щапрашивал,реультат"""
        if len(gmsg) == 0: return None
        st = gmsg[0].find("su", 0, len(gmsg[0]))
        if st == -1:  #сообщения формата su или нет
            return None

        #провереят и записывает,если соообщение о конце сесии записалось позже основного блока
        if len(gmsg) == 1:
            type = self.get_type(gmsg[0])
            tmp = self.parsing_one_su(gmsg[0])
            ev = -1
            for i in range(0, len(self.events)):
                if self.events[i][0] == type:
                    ev = i
                    break
            if ev == -1: return None
            self.events.extend(tmp)
            return

        #это часть выполняется, если у нас не одно, а целая группа сообщений
        mes = []
        for line in gmsg:
            tmp = self.parsing_one_su(line)
            if tmp != None:
                for elem in tmp:
                    mes.append(elem)
        return mes

    def parsing_one_su(self, o_msg):
        """парсит одну строку"""
        tmp = []
        msg = ""
        msgc = ""

        if o_msg.find("su for", 0, len(o_msg)) != -1:
            msg = o_msg
        if o_msg.find("session closed", 0, len(o_msg)) != -1:
            msgc = o_msg

        if msg == "" and msgc == "": return None

        if msg != "":
            tmp.append(self.get_type(msg))  #записываем номер сессии для дальнейшей работы
            tmp.append("su")  # записываем тип сообщения, для разборна на стороне сервера
            tmp.append(self.get_date(msg))  #записываем дату сообщения

            # находим на на кого притендовал пользователь (root-а)
            # st = msg.find("for",0,len(msg))+4
            # end = msg.find(" ",st,len(msg))
            # tmp.append("guser="+msg[st:end])

            #находим какой пользователь претендовал на поуления прав
            st = msg.find("by", 0, len(msg)) + 3
            end = msg.find(" ", st, len(msg))
            tmp.append("user=" + msg[st:end])

            #проверка на успешность входа
            if -1 != msg.find("Successful", 0, len(msg)):
                tmp.append("result=Successful")
            elif -1 != msg.find("FAILED ", 0, len(msg)):
                tmp.append("result=FAILED")


        # если сессия был завершина то ствим пометку в виде времени и того что она была завершина
        if msgc != "":
            tmp.append(self.get_date(msgc))
            tmp.append("result=close")

        return tmp

    def parsing_msg_kdm(self, gmsg):
        """Разбираем сообщаня, образоываные привходе в систему: дата,кто,результат"""
        if len(gmsg) == 0: return None

        st = gmsg[0].find("kdm:", 0, len(gmsg[0]))
        if st == -1:  #сообщения формата kdm или нет
            return None

        tmp = []
        for line in gmsg:
            res = None
            if line.find("authentication failure;", 0, len(line)) != -1:
                res = False
            elif line.find("session opened", 0, len(line)) != -1:
                res = True

            if res != None:
                tmp.append(self.get_type(line))
                tmp.append("kdm")
                tmp.append(self.get_date(line))

                st = line.find("ruser", 0, len(line)) + 5
                if st == -1: st = 0

                st = line.find("user", st, len(line)) + 5
                end = line.find(" ", st, len(line))
                if end == -1:
                    if line.find("\n", st, len(line)):
                        end = len(line) - 1
                    else:
                        end = len(line)

                tmp.append("user=" + line[st:end])

                if res:
                    tmp.append("result=Successful")
                else:
                    tmp.append("result=FAILED")
        return tmp

    def last_event(self, line, size, rw):
        """Записываем в файл последнию строку считаную в прошлый раз"""
        if self._system == "Windows":
            path = "C:\\Users\\Valentin\\PycharmProjects\\forensic_modul\\auth_last.txt"
        if self._system == "Linux":
                path = "/home/valentin/projects/git_projects/forensic_modul/Event_security/auth_last.txt"

        auth = open(path, rw)
        if rw == 'w':
            line = str(size) + " " + line
            auth.write(line)
            auth.close()
        elif rw == 'r':
            tmp = auth.readline()
            if tmp == "":
                self.last_rec = ""
                self.last_size = 0
            else:
                try:
                    st = tmp.find(' ', 0, len(tmp))
                    self.last_size = int(tmp[:st])
                    self.last_rec = tmp[st + 1:]
                except ValueError:
                    self.last_rec = ""
                    self.last_size = 0

    def control_event(self):
        """смотрит, был ли пополнен файл новыви событиями"""
        if self.last_rec == "" or len(self.other) < self.last_size:
            """Если произошел первый запуск или файл auth переполнился и наался ввести заново"""
            self.formation_dist(self.other)  #образуем список всех событий, которые имеют (сессию [number])
            groups = self.formation_group(self.other)
            self.formation_event(groups)
            self.last_event(self.other[len(self.other)-1],len(self.other),'w')

        elif self.other[len(self.other) - 1] == self.last_rec:
            """Если новых событий не произошло, то просто выходим"""
            print("====")
            return
        elif self.other[len(self.other) - 1] != self.last_rec:
            """Если имеем новый бок(и) событий"""
            self.tmp_dist()  #потом урать
            if self.last_rec.find("\n", 0, len(self.last_rec)) == -1:
                self.last_rec += '\n'
            flag = False
            ev = []
            for line in self.other:
                if line == self.last_rec:
                    flag = True
                if flag and line != self.last_rec:
                    ev.append(line)

            self.formation_dist(ev)  #образуем список всех событий, которые имеют (сессию [number])
            groups = self.formation_group(ev)
            self.formation_event(groups)
            self.last_event(ev[len(ev)-1],len(self.other),'w')

    def toString(self, msg):
        """Переводит входное сообщение в формат строки для дальнейшей пересылки"""
        try:
            strin = ""
            for i in range(0, len(msg)):
                if i == 0:
                    strin += str(msg[i]) + " "+ str(datetime.today().year) +"|"
                    strin += self.get_system()
                else:
                    strin += str(msg[i]) +"|"
            return strin
        except:
            return None

    def del_sent_msg(self, types):
        """Удаляет изсобытий уже разобраные и отпраленые на сервер сообщения"""
        for type in types:
            for line in self.events:
                if line[0] == type:
                    self.events.remove(line)
                    break

    def parsing_events(self):
        """Разбирает имеющиеся события и если они полныет, то отправяет на сервер"""
        su = []
        kdm = []
        for line in self.events:
            if line[1] == 'su':
                if (len(line) == 5 and line[4] == "result=FAILED")or (len(line) == 7):

                    sign = 0
                    Cflag = 0

                    if line[4] != "result=FAILED":
                        sign = 1

                    msg1 = []
                    msg1.append(line[2])
                    msg1.append(line[1])
                    msg1.append(line[3])
                    msg1.append(line[4])

                    if len(line) == 7:
                        msg2 = []
                        msg2.append(line[5])
                        msg2.append(line[1])
                        msg2.append(line[3])
                        msg2.append(line[6])
                        Cflag = 1

                    flag = None
                    if sign ==  Cflag:
                        msg = self.toString(msg1)
                        if msg != None:
                            self.client.send_message(msg)

                            flag = self.client.recv_message()
                            if flag :
                                su.append(line[0])

            elif line[1] == "kdm" :
                for i in range(0,len(line),5):
                    msg = []
                    msg.append(line[i+2])
                    msg.append(line[i+1])
                    msg.append(line[i+3])
                    msg.append(line[i+4])

                    t = self.toString(msg)
                    if t != None:
                        self.client.send_message(t)
                        flag = None
                        flag = self.client.recv_message()
                        if flag :
                            kdm.append(line[0])


        self.del_sent_msg(su)
        self.del_sent_msg(kdm)

    def reading(self):
        """основная функция, объедняет весь процесс считывания логиов"""
        # if not self.rights_root(): #если у нас нет прав рута, то выходим из программы
        #     return
        if not self.client.isConnect: #если у нас нет связи с сервером
            print("error: No connection to the server")
            return
        self.open_log_auth() # открываем файл лого вдля считывания
        self.parsing_events() # разбираем счтаные события и отправляем на сервер

event = Event_OS()
event.reading()
