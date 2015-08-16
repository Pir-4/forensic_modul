__author__ = 'Valentin'
# -*- coding:utf-8 -*-
#Manager to work with databases, receives a message from the server and stores it in the database
from Work_db import Users, Event_type, Auth, Events,Agents
# from Work_db import Auth
from datetime import datetime

class Manager():
    def __init__(self):
        self._event = Events.Events()
        self._event_type = Event_type.Event_type()
        self._users = Users.Users()
        self._auth = Auth.Auth()
        self._agents = Agents.Agents()

    def dispatcher(self,str_cef):
        if str_cef.find("CEF:",0,len(str_cef)) == -1 \
           and str_cef.find("|",0,len(str_cef)) != -1 : #If it's not a cef event, sent to convert to cef
            self.event_to_cef(str_cef)

        elif str_cef.find("admin_panel:",0,len(str_cef)) != -1: # if the message came from the admin panel

            return self.processing_admin_panel(str_cef)

        elif str_cef.find("CEF:",0,len(str_cef)) != -1 :# if it is cef write the event to the database
            return self.processing_cef(str_cef)

        return "Not"

    def processing_cef(self,str_cef):
        """The function of handling the event, if it came in the form CEF"""
        list_cef = self.parsing_CEF(str_cef) # obtain from a string list
        if list_cef == None:
            return
        table = self.change_type_event(list_cef[9]) #get the name of the table for further work by event type
        event_id,user_id = self.set_event(list_cef)

        if table == 'auth':
            self.set_auth(event_id,user_id,list_cef[12])
        return "OK"

    def parsing_CEF(self,str_cef):
         #Parsing CEF format into components
        tmp = []
        tmp.append(str_cef[:3]) # month
        if str_cef[4] == " ":
            tmp.append('0'+str_cef[5:6]) #day
        else:
            tmp.append(str_cef[4:6])#day

        tmp.append(str_cef[7:15]) # time
        tmp.append(int(str_cef[16:20])) # year
        tmp.append(str_cef[21:30]) # host

        ln = len(str_cef)
        st = str_cef.find(':',30,ln)+1
        for i in  range(0,7):
            end = str_cef.find('|',st,ln)
            if i == 4 or i== 6:
                tmp.append(int(str_cef[st:end]))
            elif i == 3:
                tmp.append(str(str_cef[st:end]))
            else:
                tmp.append(str_cef[st:end])
            st = end+1
        end = str_cef.find('|',st+1,ln)
        tmp.append(str_cef[st:end])
        tmp.append(int(str_cef[end+1:]))
        if not self._agents.isAgent(tmp[len(tmp)-1]):
             return None
        return tmp

    def get_timestamp(self,cef):
         """get of CEF format for time database"""
         string = str(cef[3])+" "+str(cef[0])+" "+str(cef[1])+" "+str(cef[2])
         date = datetime.strptime(string,"%Y %b %d %H:%M:%S")
         return string

    def get_date(self,date):
        """Getting out of time while the database cef"""
        string = datetime.strftime(date,"%c")
        return string[4:]

    def change_type_event(self,type):
        """is a request to the table type, and returns the name of the table where you want to record"""
        str = self._event_type.check_type(type)
        return str

    def get_event(self,time,cef):
         """Creating a structure for recording in Events"""
         tmp = []
         tmp.append(time)
         tmp.append(cef[4])
         tmp.append(cef[6])
         tmp.append(cef[7])
         tmp.append(cef[8])
         tmp.append(cef[9])
        #processing field extension, to find the login, if available.
         result = self.find_value('user',cef[12])
         if result == None:
             tmp.append(0)
         else:
             tmp.append(self._users.get_id(result))
         tmp.append(cef[len(cef)-1])
         return tmp

    def set_event(self,cef):
        """Write event in the Events table"""
        time = self.get_timestamp(cef) #We find the time of the event
        list_event = self.get_event(time,cef) #structure formation in a table for recording events
        event_id = self._event.set_row(list_event)#event record to the table events
        return event_id,list_event[6] #id returns the user id and events (if the user does not return 0)

    def find_value(self,sign,extension):
        """Search the desired value on the basis of field Extension"""
        ln = len(extension)
        st = extension.find(sign,0,ln)
        if st == -1 :
            return None
        else:
            st = extension.find('=',st,ln)
            end = extension.find(' ',st,ln)
            if end == -1: end=ln
            return extension[st+1:end]

    def set_auth(self,event_id,user_id,extension):
        """Write the event to a table auth"""
        list_auth = []

        list_auth.append(event_id)
        list_auth.append(user_id)#enters user id

        result = self.find_value('ip',extension)
        if result == None:
            list_auth.append("NULL")

        else:  list_auth.append(result)

        result = self.find_value('result',extension)
        if result == None:
            list_auth.append("NULL")
        else:
            list_auth.append(result)

        self._auth.set_row(list_auth)
        return 0

    def event_to_cef(self,event):
        """It converts the original event format cef for further entries in the database"""
        cef = ""
        idst = event.find("|",0,len(event))#id search agent
        agent_id = int(event[:idst])

        if  not self._agents.isAgent(agent_id):
            return None

        event = event[idst+1:]

        st1 = event.find("|",0,len(event)) # Search in event time
        st2 = event.find("|",st1+1,len(event)) #search ip (start)

        stmp = st2
        for i in range(0,3):
            st3 = event.find("|",stmp+1,len(event))# Search for the beginning of the event type
            stmp = st3

        st4 = event.find("|",st3+1,len(event))# Search the end of the event type

        type = self._event_type.find_type(event[st3+1:st4]) #Search the database of this type of posts
        if type == None:
            return None

        #selection of events to record in the meanest extension
        tmp = event[st4+1:]
        extens = ""
        for let in tmp:
            if let == '|': let = " "
            extens += let

        cef += event[:st1] +" " + event[st1+1:st2]
        cef += " CEF:0" + event[st2:st3+1]
        cef += str(type[0])+"|"+str(type[3])+"|"+str(type[1])+"|"+extens[:len(extens)-1]+"|"+str(agent_id)
        self.dispatcher(cef)

    def toCEF(self,event_id):
        """Formation posts by CEF event_id"""
        events = self._event.get_row(event_id)
        event_type = self._event.get_table_type(event_id)

        if event_type[1] == "auth":
            extension = self._auth.get_cef(event_id)

        date = self.get_date(events[1])
        host = events[2]
        vendor = events[3]
        product = events[4]
        version = events[5]
        signature = str(events[6])
        name = event_type[3]
        severity = str(event_type[2])
        agent_id = str(events[8])

        cef = date +" "+ host +" CEF:0|"+ \
              vendor +"|"+ product +"|"+ version +"|"+ signature +"|"+ name +"|"+ severity +"|"+ str(extension)+"|"\
              +agent_id
        return cef

    def print_event_cef(self,event_id):
        """Gets the events in a certain format CEF event_id (greater than or equal)"""
        events = self._event.get_event_id(event_id)
        if events == None:
            return None

        cef = []
        for id in events:
            cef.append(self.toCEF(id))
        return cef

    def processing_admin_panel(self,msg):
        """message processing from the admin panel"""
        st = msg.find(":",0,len(msg))+1
        id = int(msg[st:len(msg)])
        cef = self.print_event_cef(id)
        return cef