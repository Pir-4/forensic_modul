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
        self.but_update = Button(self,text="Обновить",command=self.update_server,anchor='center')
        self.but_clear = Button(self,text="Очистить",command=self.clear_table,anchor='center')

        self.leb_filter = Label(self, text="Филтры", anchor='center')
        self.leb_mont = Label(self, text="Месяц", anchor='center')
        self.leb_time = Label(self, text="Время", anchor='center')
        self.leb_year = Label(self, text="Год", anchor='center')
        self.leb_ip = Label(self, text="Ip", anchor='center')
        self.leb_version = Label(self, text="Версия", anchor='center')
        self.leb_vendor = Label(self, text="Производитель", anchor='center')
        self.leb_product = Label(self, text="Продукт", anchor='center')
        self.leb_versionSW = Label(self, text="Версия ПО", anchor='center')
        self.leb_type = Label(self, text="Тип", anchor='center')
        self.leb_severity = Label(self, text="Уровень угрозы", anchor='center')

        self.en_mont = Entry(self,width=10)
        self.en_time = Entry(self,width=10)
        self.en_year = Entry(self,width=10)
        self.en_ip = Entry(self, width=10)
        self.en_version = Entry(self, width=10)
        self.en_vendor = Entry(self, width=10)
        self.en_product = Entry(self, width=10)
        self.en_versionSW = Entry(self, width=10)
        self.en_type = Entry(self, width=10)
        self.en_severity = Entry(self, width=10)

        self.but_update.grid(row=0,column=1)
        self.but_clear.grid(row=0,column=2)

        pos = 1
        self.leb_filter.grid(row=pos,column=1,columnspan=2)
        self.leb_mont.grid(row=pos+1,column=1)
        self.leb_time.grid(row=pos+2,column=1)
        self.leb_year.grid(row=pos+3,column=1)
        self.leb_ip.grid(row=pos+4,column=1)
        self.leb_version.grid(row=pos+5,column=1)
        self.leb_vendor.grid(row=pos+6,column=1)
        self.leb_product.grid(row=pos+7,column=1)
        self.leb_versionSW.grid(row=pos+8,column=1)
        self.leb_type.grid(row=pos+9,column=1)
        self.leb_severity.grid(row=pos+10,column=1)

        self.en_mont.grid(row=pos+1,column=2)
        self.en_time.grid(row=pos+2,column=2)
        self.en_year.grid(row=pos+3,column=2)
        self.en_ip.grid(row=pos+4,column=2)
        self.en_version.grid(row=pos+5,column=2)
        self.en_vendor.grid(row=pos+6,column=2)
        self.en_product.grid(row=pos+7,column=2)
        self.en_versionSW.grid(row=pos+8,column=2)
        self.en_type.grid(row=pos+9,column=2)
        self.en_severity.grid(row=pos+10,column=2)

    def update_server(self):
        """отправляет и принимает запрос с сервара"""
        self.send()
        self.recv()
        self._table_req.detach()


    def del_events(self):
        """Очищает список событий"""
        while len(self.events) != 0:
            item = self.events.pop()

    def clear_table(self):
        """очистка таблицы"""
        self._table_req.destroy()
        self.table()
        self.del_events()

    def table(self):
        """Создание таблицы"""
        fr = ttk.Frame(self)
        fr.grid(row=0, column = 0,rowspan=12)

        #создаем таблицу Treeview
        self._table_req = ttk.Treeview(fr, show='headings', selectmode='browse', height=10)

        # задаем заголовки колонкам
        self._table_req["columns"]=("Month","Day","Time","Year","IP","Version","Device Vendor","Device Product","Device Version",
                              "Signature ID","Name","Severity","Extension")
        #выводим необходимые столбцы
        self._table_req["displaycolumns"] = ("Month","Day","Time","Year","IP","Version","Device Vendor","Device Product","Device Version",
                                       "Signature ID","Name","Severity","Extension")

        self._table_req.heading("Month",text="Month",anchor='center')
        self._table_req.heading("Day",text="Day",anchor='center')
        self._table_req.heading("Time",text="Time",anchor='center')
        self._table_req.heading("Year",text="Year",anchor='center')
        self._table_req.heading("IP",text="Ip",anchor='center')
        self._table_req.heading("Version",text="Version(cef)",anchor='center')
        self._table_req.heading("Device Vendor",text="Vendor",anchor='center')
        self._table_req.heading("Device Product",text="Product",anchor='center')
        self._table_req.heading("Device Version",text="Version",anchor='center')
        self._table_req.heading("Signature ID",text="Signature ID",anchor='center')
        self._table_req.heading("Name",text="Name",anchor='center')
        self._table_req.heading("Severity",text="Severity",anchor='center')
        self._table_req.heading("Extension",text="Extension",anchor='center')

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
        self._table_req.column("Extension",stretch=0, width=300)

        yscroll =ttk.Scrollbar(orient="vertical")
        # xscroll =ttk.Scrollbar(orient="horizontal")

        self._table_req.config(yscrollcommand=yscroll.set)
        # self._table_req.config(xscrollcommand=xscroll.set)

        yscroll.config(command=self._table_req)
        yscroll.grid(row=0, column=1, sticky='ns')

        # xscroll.config(command=self._table_req)
        # xscroll.grid(row=1, column=0, sticky='ew')

        self._table_req.grid(row=0, column=0, sticky=NSEW)
    def insert_table(self,events):
        """Вставка в таблицу значений"""
        for line in events:
            self._table_req.insert('','end',values=line)
        self.events.extend(events)

    def send(self):
        """Отправка сообщение серверу"""
        if self._client.isConnect:
            msg = "admin_panel:"+str(len(self.events)+1)
            # msg = "admin_panel:"+str(172)
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
root.mainloop()