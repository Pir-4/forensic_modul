__author__ = 'valentin'
# -*- coding:utf-8 -*-

# !/usr/bin/env python
import sys
import platform
import os
import getpass


class Event_OS():
    def __init__(self):
        self._system = str(platform.system())
        self._info_system = self.info_sistem()
        self._dist = {}
        self.events = []
        self.last_rec = ""
        self.last_size = 0

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
        if self._system == "Windows": path = "C:\\Users\\Valentin\\PycharmProjects\\forensic_modul\\auth_last.txt"
        if self._system == "Linux": path = "/home/valentin/projects/git_projects/forensic_modul/Event_security/auth_last.txt"

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
                strin += str(msg[i]) + "|"
                if i == 0: strin += self.get_system()
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

    def Events(self):  #подумать над названием
        """Разбирает имеющиеся события и если они полныет, то отправяет на сервер"""
        su = []
        kdm = []
        for line in self.events:
            if line[1] == 'su':
                if (len(line) == 5 and line[4] == "result=FAILED")or (len(line) == 7):
                    su.append(line[0])

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
                        # print(self.toString(msg2))

                    # print(self.toString(msg1))
                    # print("------------")

            elif line[1] == "kdm" :
                for i in range(0,len(line),5):
                    msg = []
                    msg.append(line[i+2])
                    msg.append(line[i+1])
                    msg.append(line[i+3])
                    msg.append(line[i+4])
                    # print(self.toString(msg))
                    # print("-----------------")
                    kdm.append(line[0])


        self.del_sent_msg(su)
        self.del_sent_msg(kdm)

    def tmp_dist(self):
        self.events.append([3715, 'Apr 27 20:22:12', 'guser=root', 'user=valentin', 'result=Successful'])
        self._dist = {7722: 4, 3130: 3, 3942: 1, 10581: 4, 6496: 4,
                      3699: 4, 4086: 2, 7089: 4, 3133: 3, 5027: 4, 5527: 2,
                      3081: 2, 9277: 1, 7380: 4, 3099: 3, 5647: 2, 3006: 3,
                      6491: 4, 4556: 1, 3101: 3, 4305: 4, 3941: 1, 4359: 4,
                      9244: 3, 7028: 2, 5270: 3, 2689: 3, 3144: 5, 11355: 1,
                      5248: 4, 3147: 3, 3159: 3, 3143: 3, 7398: 3, 7184: 3,
                      2666: 6, 5322: 3, 17504: 2, 5012: 4, 9677: 1, 3761: 1,
                      4997: 4, 3017: 3, 7405: 4, 5271: 4, 11331: 4, 3154: 3,
                      6479: 4, 4101: 4, 8819: 4, 2991: 3, 12565: 4, 2681: 3,
                      7262: 4, 6497: 4, 12385: 2, 12977: 4, 6513: 4, 10210: 4,
                      4046: 1, 6326: 4, 6805: 2, 7285: 4, 2441: 3, 12991: 4,
                      7175: 3, 7494: 4, 4981: 4, 3138: 3, 5652: 2, 9254: 1,
                      6314: 4, 7168: 3, 8797: 4, 3801: 2, 8452: 2, 7738: 4,
                      5196: 2, 9259: 1, 3065: 3, 3140: 3, 4047: 1, 2995: 2,
                      2674: 3, 3715: 3, 9262: 1, None: 126, 11363: 4, 2458: 3,
                      9248: 1, 3550: 2, 5642: 4, 8835: 4, 4996: 4, 3131: 3,
                      3724: 4, 7129: 4, 3958: 1, 9668: 3, 8095: 1, 2442: 3,
                      3090: 3, 7401: 3, 11379: 4, 13110: 4, 3024: 3, 4835: 2,
                      4375: 4, 4044: 5, 2448: 3, 2453: 3, 2467: 3, 13607: 4,
                      3708: 4, 2447: 3, 9672: 1, 3141: 7, 11387: 1, 3152: 3,
                      9682: 1, 12291: 4, 13045: 4}


event = Event_OS()
event.rights_root()
event.open_log_auth()
event.Events()
