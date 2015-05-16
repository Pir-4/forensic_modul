 #__author__ = 'Valentin'
 # -*- coding:utf-8 -*-
#панель администратора

from Tkinter import *
import ttk
from datetime import*
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
        self.but_update = Button(self,text="Обновить таблицу",command=self.update_server,anchor='center')
        self.but_clear = Button(self,text="Очистить таблицу",command=self.clear_table,anchor='center')

        self.leb_filter = Label(self, text="Филтры", anchor='center')
        self.leb_month = Label(self, text="Месяц", anchor='center')
        self.leb_day = Label(self, text="День", anchor='center')
        self.leb_time = Label(self, text="Время", anchor='center')
        self.leb_year = Label(self, text="Год", anchor='center')
        self.leb_ip = Label(self, text="Ip", anchor='center')
        self.leb_version = Label(self, text="Версия", anchor='center')
        self.leb_vendor = Label(self, text="Производитель", anchor='center')
        self.leb_product = Label(self, text="Продукт", anchor='center')
        self.leb_versionSW = Label(self, text="Версия ПО", anchor='center')
        self.leb_type = Label(self, text="Тип", anchor='center')
        self.leb_severity = Label(self, text="Уровень угрозы", anchor='center')


        self.but_apply_filter = Button(self,text="Применить фильтры",command=self.apply_filter,anchor='center')
        self.but_clear_filter = Button(self,text="Очистить фильтры",command=self.clear_filter,anchor='center')

        self.en_month = Entry(self,width=10)
        self.en_day = Entry(self,width=10)
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
        self.leb_month.grid(row=pos+1,column=1)
        self.leb_day.grid(row=pos+2,column=1)
        self.leb_time.grid(row=pos+3,column=1)
        self.leb_year.grid(row=pos+4,column=1)
        self.leb_ip.grid(row=pos+5,column=1)
        self.leb_version.grid(row=pos+6,column=1)
        self.leb_vendor.grid(row=pos+7,column=1)
        self.leb_product.grid(row=pos+8,column=1)
        self.leb_versionSW.grid(row=pos+9,column=1)
        self.leb_type.grid(row=pos+10,column=1)
        self.leb_severity.grid(row=pos+11,column=1)

        self.en_month.grid(row=pos+1,column=2)
        self.en_day.grid(row=pos+2,column=2)
        self.en_time.grid(row=pos+3,column=2)
        self.en_year.grid(row=pos+4,column=2)
        self.en_ip.grid(row=pos+5,column=2)
        self.en_version.grid(row=pos+6,column=2)
        self.en_vendor.grid(row=pos+7,column=2)
        self.en_product.grid(row=pos+8,column=2)
        self.en_versionSW.grid(row=pos+9,column=2)
        self.en_type.grid(row=pos+10,column=2)
        self.en_severity.grid(row=pos+11,column=2)

        self.but_apply_filter.grid(row=pos+12,column=1)
        self.but_clear_filter.grid(row=pos+12,column=2)

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

    def apply_filter(self):
        """Применение фильтров и вывод информации на таблицу"""
        tmp = self.filter_month(self.events)
        tmp = self.filter_day(tmp)
        tmp = self.filter_time(tmp)
        tmp = self.filter_year(tmp)
        tmp = self.filter_ip(tmp)
        tmp = self.filter_version(tmp)
        tmp = self.filter_vendor(tmp)
        tmp = self.filter_product(tmp)
        tmp = self.filter_vesionSW(tmp)
        tmp = self.filter_type(tmp)
        tmp = self.filter_severity(tmp)

        self._table_req.destroy()
        self.table()
        self.insert_table(tmp)

    def filter_month(self,events):
        """Филрътрация по месяцу"""
        try:
            month = int(self.en_month.get())
            return events
        except:
            month = self.en_month.get()[:3]
            if month =="" or month == " ":
                return events

        return self.filter(events,month,0)

    def filter_day(self,events):
        """Фильтрует значение по дню"""
        try:
            day = int(self.en_day.get())
        except:
            return events

        return self.filter(events,day,1)

    def filter_time(self,events):
        """Фильтрация по времмени"""
        tmp = self.en_time.get()
        try:
            Time = datetime.strptime(tmp,"%H:%M:%S").time()
        except:
            return events

        return self.filter(events,Time,2)

    def filter_year(self,events):
        """Фильтрует значение по году"""
        try:
            year = int(self.en_year.get())
        except:
            return events

        return self.filter(events,year,3)

    def filter_ip(self,events):
        """Филрътрация по ip"""
        try:
            ip = int(self.en_ip.get())
            return events
        except:
            ip = self.en_ip.get()
            if ip =="" or ip == " ":
                return events
        return self.filter(events,ip,4)

    def filter_version(self,events):
        """Фильтрует значение по версии cef"""
        try:
            ver = int(self.en_version.get())
        except:
            return events

        return self.filter(events,ver,5)

    def filter_vendor(self,events):
        """Филрътрация по производителю"""
        try:
            ven = int(self.en_vendor.get())
            return events
        except:
            ven = self.en_vendor.get()
            if ven =="" or ven == " ":
                return events

        return self.filter(events,ven,6)

    def filter_product(self,events):
        """Филрътрация по продукту"""
        try:
            prod = int(self.en_product.get())
            return events
        except:
            prod = self.en_product.get()
            if prod =="" or prod == " ":
                return events

        return self.filter(events,prod,7)

    def filter_vesionSW(self,events):
        """Филрътрация по версии продукта"""
        try:
            ver = int(self.en_versionSW.get())
            return events
        except:
            ver = self.en_versionSW.get()
            if ver =="" or ver == " ":
                return events

        return self.filter(events,ver,8)

    def filter_type(self,events):
        """Фильтрует значение по типу"""
        try:
            type = int(self.en_type.get())
        except:
            return events

        return self.filter(events,type,9)

    def filter_severity(self,events):
        """Фильтрует значение по уровню угрозы"""
        try:
            sev = int(self.en_severity.get())
        except:
            return events

        return self.filter(events,sev,11)

    def filter(self,events,sign,pos):
        """Фильтрация списка по признаку"""
        tmp = []
        for line in events:
            si = line[pos]

            if pos == 2:
                si = datetime.strptime(si,"%H:%M:%S").time()

            if sign == si:
                tmp.append(line)

        return tmp

    def clear_filter(self):
        """Очищает параметры фильтрации"""
        self.en_month.delete(0,len(self.en_month.get()))
        self.en_day.delete(0,len(self.en_day.get()))
        self.en_time.delete(0,len(self.en_time.get()))
        self.en_year.delete(0,len(self.en_year.get()))
        self.en_ip.delete(0,len(self.en_ip.get()))
        self.en_version.delete(0,len(self.en_version.get()))
        self.en_vendor.delete(0,len(self.en_vendor.get()))
        self.en_product.delete(0,len(self.en_product.get()))
        self.en_versionSW.delete(0,len(self.en_versionSW.get()))
        self.en_type.delete(0,len(self.en_type.get()))
        self.en_severity.delete(0,len(self.en_severity.get()))

        self._table_req.destroy()
        self.table()
        self.insert_table(self.events)

    def table(self):
        """Создание таблицы"""
        fr = ttk.Frame(self)
        fr.grid(row=0, column = 0,rowspan=20)

        #создаем таблицу Treeview
        self._table_req = ttk.Treeview(fr, show='headings', selectmode='browse', height=10)

        # задаем заголовки колонкам
        self._table_req["columns"]=("Month","Day","Time","Year","IP","Version","Device Vendor","Device Product","Device Version",
                              "Signature ID","Name","Severity","Extension","Agent_id")
        #выводим необходимые столбцы
        self._table_req["displaycolumns"] = ("Month","Day","Time","Year","IP","Version","Device Vendor","Device Product","Device Version",
                                       "Signature ID","Name","Severity","Extension","Agent_id")

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
        self._table_req.heading("Agent_id",text="Agent_id",anchor='center')

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
        self._table_req.column("Agent_id",stretch=0, width=60)

        yscroll =ttk.Scrollbar(orient="vertical")

        self._table_req.config(yscrollcommand=yscroll.set)

        yscroll.config(command=self._table_req.yview)
        yscroll.grid(row=0, column=1, sticky='ns')


        self._table_req.grid(row=0, column=0, sticky=NSEW)

    def insert_table(self,events):
        """Вставка в таблицу значений"""
        if events:
            for line in events:
                self._table_req.insert('','end',values=line)

    def send(self):
        """Отправка сообщение серверу"""
        if self._client.isConnect:
            msg = "admin_panel:"+str(len(self.events)+1)
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

        self.events.extend(tmp)
        self.insert_table(tmp)

    def parsing_CEF(self,str_cef):
         #Парсинг формата CEF на составляющие
        tmp = []
        tmp.append(str_cef[:3]) # месяц

        if str_cef[4] == " ":
           day = '0'+str_cef[5:6] #день
        else:
            day = str_cef[4:6]#день

        tmp.append(int(day))
        tmp.append(str_cef[7:15]) # время
        tmp.append(int(str_cef[16:20])) # год
        tmp.append(str_cef[21:30]) # хост

        ln = len(str_cef)
        st = str_cef.find(':',30,ln)+1
        for i in  range(0,7):
            end = str_cef.find('|',st,ln)
            if i == 4 or i== 6 or i == 0:
                tmp.append(int(str_cef[st:end]))
            elif i == 3:
                tmp.append(str(str_cef[st:end]))
            else:
                tmp.append(str_cef[st:end])
            st = end+1
        # tmp.append(str_cef[st:])
        end = str_cef.find('|',st+1,ln)
        tmp.append(str_cef[st:end])
        tmp.append(int(str_cef[end+1:]))
        return tmp


root = Tk()
app = Panel(root)
root.mainloop()