__author__ = 'Valentin'
# -*- coding:utf-8 -*-
#Менеджер для работы с базами данных, принимает сообщение от сервера и записывает его в базу данных
from Work_db import Users, Event_type, Auth, Events
from Work_db import Auth
from datetime import datetime

class Manager():
    def __init__(self):
        self._event = Events.Events()
        self._event_type = Event_type.Event_type()
        self._users = Users.Users()
        self._auth = Auth.Auth()

    def dispatcher(self,str_cef):
        if str_cef.find("CEF:",0,len(str_cef)) == -1 \
           and str_cef.find("|",0,len(str_cef)) != -1 : #если прило не cef а событие, то отправлем на преобразование в cef
            self.event_to_cef(str_cef)

        elif str_cef.find("admin_panel:",0,len(str_cef)) != -1: # если прило ссообщени с панели администратора

            return self.processing_admin_panel(str_cef)

        elif str_cef.find("CEF:",0,len(str_cef)) != -1 :# если пришло cef то записываем данное событие в бд
            return self.processing_cef(str_cef)

        return "Not"

    def processing_cef(self,str_cef): #Праоверить правильность для CEF и для сырых
        """Функция обработки события, если оно пришло в формате CEF"""
        list_cef = self.parsing_CEF(str_cef) # получаем из строки лист

        table = self.change_type_event(list_cef[9]) #получаем имя таблицы для дальнейшей работы по типу осбытия
        event_id,user_id = self.set_event(list_cef)

        if table == 'auth':
            self.set_auth(event_id,user_id,list_cef[12])
        return "OK"

    def parsing_CEF(self,str_cef):
         #Парсинг формата CEF на составляющие
        tmp = []
        tmp.append(str_cef[:3]) # месяц
        if str_cef[4] == " ":
            tmp.append('0'+str_cef[5:6]) #день
        else:
            tmp.append(str_cef[4:6])#день

        tmp.append(str_cef[7:15]) # время
        tmp.append(int(str_cef[16:20])) # год
        tmp.append(str_cef[21:30]) # хост

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
        tmp.append(str_cef[st:])
        return tmp

    def get_timestamp(self,cef):
         """получение из CEF формат времени для бд"""
         string = str(cef[3])+" "+str(cef[0])+" "+str(cef[1])+" "+str(cef[2])
         date = datetime.strptime(string,"%Y %b %d %H:%M:%S")
         return string

    def get_date(self,date):
        """Получение из времени бд время cef"""
        string = datetime.strftime(date,"%c")
        return string[4:]

    def change_type_event(self,type):
        """идет запрос в таблицу типов, и возвращяется имя таблицы куда нужно записать"""
        str = self._event_type.check_type(type)
        return str

    def get_event(self,time,cef):
         """Создание структуры для записи в Events"""
         tmp = []
         tmp.append(time)
         tmp.append(cef[4])
         tmp.append(cef[6])
         tmp.append(cef[7])
         tmp.append(cef[8])
         tmp.append(cef[9])
        #обработка поля extension, для нахожения логина, если имеется.
         result = self.find_value('user',cef[12])
         if result == None:
             tmp.append(0)
         else:
             tmp.append(self._users.get_id(result))
         return tmp

    def set_event(self,cef):
        """Записываем событие в таблицу Events"""
        time = self.get_timestamp(cef) #находим время события
        list_event = self.get_event(time,cef) #формирования струкруры для записи в таблицу events
        event_id = self._event.set_row(list_event)#запись события в таблицу events
        return event_id,list_event[6] #возвращает id события и id пользователя (если пользователя нет то вернет 0)

    def find_value(self,sign,extension):
        """Поиск необходимого значения по признаку в поле Extension"""
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
        """Записываем событие в таблицу auth"""
        list_auth = []

        list_auth.append(event_id)
        list_auth.append(user_id)#заноси id ползователя

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
        """Преобразовывает входное событие в формат cef для дальнейшей записи в БД"""
        cef = ""

        st1 = event.find("|",0,len(event)) # поиск в событии времени
        st2 = event.find("|",st1+1,len(event)) # для поиска ip (начала)

        stmp = st2
        for i in range(0,3):
            st3 = event.find("|",stmp+1,len(event))# поиск начала типа события
            stmp = st3

        st4 = event.find("|",st3+1,len(event))# поиск конца типа события

        type = self._event_type.find_type(event[st3+1:st4]) #поиск в бд тип данного сообщения
        if type == None:
            return None

        #выделение из события подлей для записи в extension
        tmp = event[st4+1:]
        extens = ""
        for let in tmp:
            if let == '|': let = " "
            extens += let

        cef += event[:st1] +" " + event[st1+1:st2]
        cef += " CEF:0" + event[st2:st3+1]
        cef += str(type[0])+"|"+str(type[3])+"|"+str(type[1])+"|"+extens
        self.dispatcher(cef)

    def toCEF(self,event_id):
        """Формирование сообщения CEF по event_id"""
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

        cef = date +" "+ host +" CEF:0|"+ \
              vendor +"|"+ product +"|"+ version +"|"+ signature +"|"+ name +"|"+ severity +"|"+ str(extension)
        return cef

    def print_event_cef(self,event_id):
        """Возвращает события в формате cef с отпределеного event_id (большего или равного)"""
        events = self._event.get_event_id(event_id)
        if events == None:
            return None

        cef = []
        for id in events:
            cef.append(self.toCEF(id))
        return cef

    def processing_admin_panel(self,msg):
        """обработка сообщения от панели администратора"""
        st = msg.find(":",0,len(msg))+1
        id = int(msg[st:len(msg)])
        cef = self.print_event_cef(id)
        return cef