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
    def __init__(self,id):
        self._agent_id = id
        self._system = str(platform.system())
        self._info_system = self.info_sistem()
        self._dist = {}
        self.events = []
        self.last_rec = ""
        self.last_size = 0

        self.client = client.Client()

    def info_sistem(self):
        """returns information about the OS"""
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
        """We receive reports of church's system format cef """
        tmp = ""
        for info in self._info_system:
            tmp += info + "|"
        return tmp

    def rights_root(self):
        """script to request root access if they do not"""
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
            """open the log file auth (until the, test)"""
            if self.rights_root():
                path = "/var/log/auth.log"
            else:
                path = "/home/valentin/projects/git_projects/forensic_modul/Event_security/auth_test.log"
        else:
            path = "C:\\Users\\Valentin\\PycharmProjects\\forensic_modul\\auth_test.txt"

        auth = open(path, 'r')
        self.other = auth.readlines()
        auth.close()
        self.last_event("", 0, 'r')  # We read the last event that will be remembered
        self.control_event()

    def formation_dist(self, msgs):
        """We make available a set of sessions identifying events"""

        for line in msgs:
            type = self.get_type(line)
            if type != None:
                if self._dist.get(type, None) == None:
                    self._dist[type] = 1
                else:
                    self._dist[type] += 1


    def formation_group(self, msgs):
        """returns a list of copied messages in their session number"""
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
        """forimirovanie of received events are grouped in view of inifitsirovanny"""
        for line in groups:
            tmp = self.parsing_msg_su(line)
            if tmp != None:
                self.events.append(tmp)
            else:
                tmp = self.parsing_msg_kdm(line)
                if tmp != None:
                    self.events.append(tmp)

    def get_date(self, msg):
        """returns the date of the incoming messages"""
        # print(msg)
        st = msg.find(" ", 0, len(msg))
        st = msg.find(":", st + 1, len(msg))
        st = msg.find(" ", st + 1, len(msg))
        return msg[:st]

    def get_type(self, msg):
        """returns the session posts"""
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
        """Dismantle the logs (for su) (are grouped) into components time to any right to claim who schaprashival, reultate"""
        if len(gmsg) == 0: return None
        st = gmsg[0].find("su", 0, len(gmsg[0]))
        if st == -1:  #Messages format su or no
            return None

        #and sign checks, if the message of the end of the session is recorded after the main unit
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

        #This part is done, if we have not one but a whole group of messages
        mes = []
        for line in gmsg:
            tmp = self.parsing_one_su(line)
            if tmp != None:
                for elem in tmp:
                    mes.append(elem)
        return mes

    def parsing_one_su(self, o_msg):
        """parse one line"""
        tmp = []
        msg = ""
        msgc = ""

        if o_msg.find("su for", 0, len(o_msg)) != -1: #or o_msg.find("root by ", 0, len(o_msg)) != -1:
            msg = o_msg
        if o_msg.find("session closed", 0, len(o_msg)) != -1:
            msgc = o_msg

        if msg == "" and msgc == "": return None

        if msg != "":
            tmp.append(self.get_type(msg))  #write the number of the session for further work
            tmp.append("su")  # write message type to parse the server side
            tmp.append(self.get_date(msg))  #record the date of the report

            # find someone to claim the user (root-a)
            # st = msg.find("for",0,len(msg))+4
            # end = msg.find(" ",st,len(msg))
            # tmp.append("guser="+msg[st:end])

            #We find a user to apply for rights
            st = msg.find("by", 0, len(msg)) + 3
            end = msg.find(" ", st, len(msg))
            tmp.append("user=" + msg[st:end])

            #check for a successful login
            if -1 != msg.find("Successful", 0, len(msg)):
                tmp.append("result=Successful")
            elif -1 != msg.find("FAILED ", 0, len(msg)):
                tmp.append("result=FAILED")


        # if the session has been completed is highly hypothetical mark in the form of time and the fact that it has been completed
        if msgc != "":
            tmp.append(self.get_date(msgc))
            tmp.append("result=close")

        return tmp

    def parsing_msg_kdm(self, gmsg):
        """Parse Posts formed at logon date, who, result"""
        if len(gmsg) == 0: return None

        st = gmsg[0].find("kdm:", 0, len(gmsg[0]))
        if st == -1:  #Posts kdm format or not
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
        """Write to file the last line of the read last time"""
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
        """It looks whether the file is augmented with new developments"""
        if self.last_rec == "" or len(self.other) < self.last_size:
            """If there was a first run or a file auth overflowed and began to re-enter"""
            self.formation_dist(self.other)  #we form a list of all the events that have (session [number])
            groups = self.formation_group(self.other)
            self.formation_event(groups)
            self.last_event(self.other[len(self.other)-1],len(self.other),'w')

        elif self.other[len(self.other) - 1] == self.last_rec:
            """If the new event does not happen, then just leave"""
            print("====")
            return
        elif self.other[len(self.other) - 1] != self.last_rec:
            """If you have a new side (s) of events"""
            if self.last_rec.find("\n", 0, len(self.last_rec)) == -1:
                self.last_rec += '\n'
            flag = False
            ev = []
            for line in self.other:
                if line == self.last_rec:
                    flag = True
                if flag and line != self.last_rec:
                    ev.append(line)
            if len(ev) != 0:
                self.formation_dist(ev)  #we form a list of all the events that have (session [number])
                groups = self.formation_group(ev)
                self.formation_event(groups)
                self.last_event(ev[len(ev)-1],len(self.other),'w')

    def toString(self, msg):
        """It translates the input message format string to forward"""
        try:
            strin = str(self._agent_id)+"|"
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
        """Removes events already dismantled and sent to the server message"""
        for type in types:
            for line in self.events:
                if line[0] == type:
                    self.events.remove(line)
                    break

    def parsing_events(self):
        """Parses the available events and if complete, it sends to the server"""
        su = []
        kdm = []
        for line in self.events:
            if line[1] == 'su':
                if (len(line) == 5 and line[4] == "result=FAILED")or (len(line) == 7):

                    sign = 0
                    Cflag = 0
                    smsg2 =None

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
                        smsg2 = self.toString(msg2)

                    if sign == Cflag:
                        smsg1 = self.toString(msg1)

                        flag1 = self.send_msg(smsg1)
                        flag2 = True

                        if smsg2 != None:
                            flag2 = False
                            flag2 = self.send_msg(smsg2)

                        if flag1 and flag2:
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
                        if self.send_msg(t) :
                            kdm.append(line[0])


        self.del_sent_msg(su)
        self.del_sent_msg(kdm)

    def send_msg(self,msg):
        """It sends a message to the server, if the message came back that type inchane NONE"""
        self.client.send_message(msg)
        if self.client.recv_message() != None:
            return True
        return False

    def reading(self):
        """the main function, integrates the entire process of reading logins"""
        # if not self.rights_root(): #If you do not have root access, then exit the program
        #     return
        if not self.client.isConnect: #if we have no connection to the server
            print("error: No connection to the server")
            return
        self.open_log_auth() # open the log file for reading
        self.parsing_events() # dismantle a few events and sent to the server


# event = Event_OS()
# event.reading()
