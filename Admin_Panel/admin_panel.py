 #__author__ = 'Valentin'
 # -*- coding:utf-8 -*-
#панель администратора

from Tkinter import *
import ttk
import client


class Panel(Frame):
    """Реализация панели администратора"""
    def __init__(self,master):
        Frame.__init__(self,master)
        self._client = client.Client()
        self.grid()
        self.table()
        self.create_widgets()

        self.events = []

    def create_widgets(self):
        """Создание виджета, в будущем расположение фильтров"""

    def table(self):
        """Создание таблицы"""
        fr = ttk.Frame(self)
        fr.grid(row=2, column = 0, columnspan = 4)

        #создаем таблицу Treeview
        self._table_req = ttk.Treeview(fr, show='headings', selectmode='browse', height=10)

        # задаем заголовки колонкам
        self._table_req["columns"]=("Month","Day","Time","Year","IP","Version","Device Vendor","Device Product","Device Version",
                              "Signature ID","Name","Severity","Extension")
        #выводим необходимые столбцы
        self._table_req["displaycolumns"] = ("Month","Day","Time","Year","IP","Version","Device Vendor","Device Product","Device Version",
                                       "Signature ID","Name","Severity","Extension")

        self._table_req.heading("Month",text="Month",anchor='w')
        self._table_req.heading("Day",text="Day",anchor='w')
        self._table_req.heading("Time",text="Time",anchor='w')
        self._table_req.heading("Year",text="Year",anchor='w')
        self._table_req.heading("IP",text="Ip",anchor='w')
        self._table_req.heading("Version",text="Version(cef)",anchor='w')
        self._table_req.heading("Device Vendor",text="Vendor",anchor='w')
        self._table_req.heading("Device Product",text="Product",anchor='w')
        self._table_req.heading("Device Version",text="Version",anchor='w')
        self._table_req.heading("Signature ID",text="Signature ID",anchor='w')
        self._table_req.heading("Name",text="Name",anchor='w')
        self._table_req.heading("Severity",text="Severity",anchor='w')
        self._table_req.heading("Extension",text="Extension",anchor='w')

        self._table_req.column("Month",stretch=0, width=50)
        self._table_req.column("Day",stretch=0, width=30)
        self._table_req.column("Time",stretch=0, width=65)
        self._table_req.column("Year",stretch=0, width=40)
        self._table_req.column("IP",stretch=0, width=40)
        self._table_req.column("Version",stretch=0, width=57)
        self._table_req.column("Device Vendor",stretch=0, width=60)
        self._table_req.column("Device Product",stretch=0, width=60)
        self._table_req.column("Device Version",stretch=0, width=60)
        self._table_req.column("Signature ID",stretch=0, width=65)
        self._table_req.column("Name",stretch=0, width=100)
        self._table_req.column("Severity",stretch=0, width=60)
        self._table_req.column("Extension",stretch=0, width=200)

        scroll =ttk.Scrollbar(fr)
        self._table_req.config(yscrollcommand=scroll.set)
        scroll.config(command=self._table_req)
        scroll.grid(row=0, column=1, sticky=N + S)

        self._table_req.grid(row=0, column=0, sticky=NSEW)
    def insert_table(self,events):
        """Вставка в таблицу значений"""
        for line in events:
            self._table_req.insert('','end',values=line)

    def send(self):
        """Отправка сообщение серверу"""
        if self._client.isConnect:
            msg = "admin_panel:"+str(len(self.events)+1)
            # msg = "admin_panel:"+str(1000+1)
            self._client.send_message(msg)

        else:
            print("Not connect server")

    def recv(self):
        """Полуение ответа от сервера"""
        tmp = []
        msg = self._client.recv_message()
        l = int(msg)
        for i in range(0,l):
            msg = self._client.recv_message()
            tmp.append(self.parsing_CEF(msg))

        self.insert_table(tmp)

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


root = Tk()
app = Panel(root)
app.send()
app.recv()
root.mainloop()