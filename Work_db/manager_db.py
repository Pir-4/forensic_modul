__author__ = 'Valentin'
# -*- coding:utf-8 -*-
#Менеджер для работы с базами данных, принимает сообщение от сервера и записывает его в базу данных
from Work_db import Users, Event_type, Auth, Events
from Work_db import Auth

class Manager():
    def __init__(self):
        self._event = Events.Events()
        self._event_type = Event_type.Event_type()
        self._users = Users.Users()
        self._auth = Auth.Auth()

    def dispatcher(self,str_cef):

        if str_cef.find("CEF:",0,len(str_cef)) == -1: #если прило не cef а событие, то отправлем на преобразование в cef
            self.event_to_cef(str_cef)

        else:# если пришло cef то записываем данное событие в бд
            list_cef = self.parsing_CEF(str_cef) # получаем из строки лист

            table = self.change_type_event(list_cef[9]) #получаем имя таблицу для дальнейшей работы по типу осбытия
            event_id,user_id = self.set_event(list_cef)

            if table == 'auth':
                self.set_auth(event_id,user_id,list_cef[12])

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
         """получение из CEF формат времени"""

         if cef[0]=="Jan": month ='0'+str(1)
         elif cef[0]=="Feb": month ='0'+str(2)
         elif cef[0]=="Mar": month ='0'+str(3)
         elif cef[0]=="Apr": month ='0'+str(4)
         elif cef[0]=="May": month ='0'+str(5)
         elif cef[0]=="Jun": month ='0'+str(6)
         elif cef[0]=="Jul": month ='0'+str(7)
         elif cef[0]=="Aug": month ='0'+str(8)
         elif cef[0]=="Sep": month ='0'+str(9)
         elif cef[0]=="Oct": month = str(10)
         elif cef[0]=="Nov": month = str(11)
         elif cef[0]=="Dec": month = str(12)

         string = str(cef[3])+"-"+month+"-"+str(cef[1])+" "+cef[2]

         return string

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
        return event_id,list_event[6] #возвращает id события и id пользователя (если нет то вернет 0)

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
        list_auth = []

        list_auth.append(event_id)
        list_auth.append(user_id)

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
        print(event)
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
        # print(cef)
        self.dispatcher(cef)