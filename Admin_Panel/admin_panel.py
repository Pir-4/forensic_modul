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
        self.info_prod = []
        self.info_type = []
        self.info_exten = []

    def create_widgets(self):
        """Создание виджета, в будущем расположение фильтров"""
        self.but_update = Button(self,text="Обновить таблицу",command=self.update_server,anchor='center')
        self.but_clear = Button(self,text="Очистить таблицу",command=self.clear_table,anchor='center')

        self.leb_filter = Label(self, text="Филтры", anchor='center')

        self.leb_date = Label(self, text="Дата", anchor='center')
        self.chekbox_val = IntVar()
        self.checkbox = Checkbutton(self,variable = self.chekbox_val,command=self.date2,onvalue=True,offvalue=False)


        self.leb_ip = Label(self, text="Ip", anchor='center')
        self.leb_version = Label(self, text="Версия", anchor='center')
        self.but_product = Button(self,text = "Список ПО",command = self.filling_listbox_prod)
        self.lis_prod = None
        self.but_type = Button(self,text = "Тип",command = self.filling_listbox_type)
        self.lis_type = None
        self.leb_severity = Label(self, text="Уровень угрозы", anchor='center')
        self.but_exten = Button(self,text = "Дополнительно",command = self.filling_listbox_exten)
        self.lis_exten = None
        self.leb_agent = Label(self, text="Агент id", anchor='center')


        self.but_apply_filter = Button(self,text="Применить фильтры",command=self.apply_filter,anchor='center')
        self.but_clear_filter = Button(self,text="Очистить фильтры",command=self.clear_filter,anchor='center')

        self.en_date = Entry(self,width=10)
        self.en_date2 = None

        self.en_ip = Entry(self, width=10)
        self.en_version = Entry(self, width=10)
        self.en_product = Label(self, anchor='center')
        self.en_type = Label(self, anchor='center')
        self.en_severity = Entry(self, width=10)
        self.en_exten = Label(self, anchor='center')
        self.en_agent = Entry(self, width=10)

        self.but_update.grid(row=0,column=1)
        self.but_clear.grid(row=0,column=2)

        pos = 1
        self.leb_filter.grid(row=pos,column=1,columnspan=2)
        self.leb_date.grid(row=pos+1,column=1)
        self.checkbox.grid(row=pos+1,column=3)
        self.leb_ip.grid(row=pos+3,column=1)
        self.leb_version.grid(row=pos+4,column=1)
        self.but_product.grid(row=pos+5,column=1)
        self.but_type.grid(row=pos+6,column=1)
        self.leb_severity.grid(row=pos+7,column=1)
        self.but_exten.grid(row=pos+8,column=1)
        self.leb_agent.grid(row=pos+9,column=1)

        self.en_date.grid(row=pos+1,column=2)
        self.en_ip.grid(row=pos+3,column=2)
        self.en_version.grid(row=pos+4,column=2)
        self.en_product.grid(row=pos+5,column=2,columnspan=4)
        self.en_type.grid(row=pos+6,column=2,columnspan=4)
        self.en_severity.grid(row=pos+7,column=2)
        self.en_exten.grid(row=pos+8,column=2,columnspan=4)
        self.en_agent.grid(row=pos+9,column=2)

        self.but_apply_filter.grid(row=pos+12,column=1)
        self.but_clear_filter.grid(row=pos+12,column=2)
    def date2(self):
        """Отвечает за отображение вторго поля даты"""
        if self.chekbox_val.get():
            self.leb_date['text'] = "Дата (от)"
            self.leb_date2 = Label(self, text="Дата (до)", anchor='center')
            self.en_date2 = Entry(self,width=10)
            self.leb_date2.grid(row=3,column=1)
            self.en_date2.grid(row=3,column=2)
        else:
            self.leb_date['text'] = "Дата"
            self.leb_date2.destroy()
            self.en_date2.destroy()
            self.en_date2 = None

    def update_server(self):
        """отправляет и принимает запрос с сервара"""
        self.send()
        self.recv()
        self._table_req.detach()


    def del_events(self):
        """Очищает список событий"""
        while len(self.events) != 0:
            item = self.events.pop()

    def del_info(self):
        """Очищает список ПО для фильтра"""
        while len(self.info_prod) != 0:
            item = self.info_prod.pop()

        while len(self.info_type) != 0:
            item = self.info_type.pop()

        while len(self.info_exten) != 0:
            item = self.info_exten.pop()

    def clear_table(self):
        """очистка таблицы"""
        self._table_req.destroy()
        self.table()
        self.del_events()
        self.del_info()

    def apply_filter(self):
        """Применение фильтров и вывод информации на таблицу"""
        tmp = self.filter_date(self.events)
        tmp = self.filter_ip(tmp)
        tmp = self.filter_version(tmp)
        tmp = self.filter_product(tmp)
        tmp = self.filter_type(tmp)
        tmp = self.filter_severity(tmp)
        tmp = self.filter_extension(tmp)
        tmp = self.filter_agent(tmp)

        self._table_req.destroy()
        self.table()
        self.insert_table(tmp)

    def find_date(self,string,size):
        """Ищет месяц/день/время/год и возвращает его"""
        if string == None:
            return None
        tmp = []
        valu = None
        for line in string:
            if len(line) == size:
                valu = line
            else:
                tmp.append(line)
        return valu,tmp

    def parsing_date(self,date):
        """Принимает строку с датой и разбирает ее"""
        c = date.count(" ",0,len(date)) #подсчет количексва пробелов
        st = 0
        tmp = []
        #раздел строки на сотавляющие
        for i in range(-1,c):
            end = date.find(" ",st,len(date))
            if end== -1:
                end=len(date)
            tmp.append(date[st:end])
            st = end+1

        #определение необходимых значений
        month,tmp =self.find_date(tmp,3)
        day,tmp =self.find_date(tmp,2)
        time,tmp =self.find_date(tmp,8)
        year,tmp =self.find_date(tmp,4)

        return  month,day,time,year

    def filter_date(self,events):
        """Филрътрация по месяцу"""
        date = self.en_date.get()
        if date == "" or date==" ":
            return events

        month,day,time,year = self.parsing_date(date)

        if month != None and day != None and time != None and year != None:

            date1 = month+" "+day+" "+time+" "+year
            date1 = datetime.strptime(date1,"%b %d %H:%M:%S %Y")

            if self.chekbox_val.get():
                date2 = self.en_date2.get()
                if date2 == "" or date2 ==" ":
                    date2 = None
                else:
                    month,day,time,year = self.parsing_date(date2)
                    date = month+" "+day+" "+time+" "+year
                    date2 = datetime.strptime(date,"%b %d %H:%M:%S %Y")
            else:
                date2 = None

            return self.filter_dates(events,date1,date2)


        else:
            tmp = events
            if month != None:
                tmp = self.filter(tmp,month,0)
            if day != None:
                tmp = self.filter(tmp,int(day),1)
            if time != None:
                time = datetime.strptime(time,"%H:%M:%S").time()
                tmp = self.filter(tmp,time,2)
            if year != None:
                tmp = self.filter(tmp,int(year),3)
            return tmp

        # try:
        #     month = int(self.en_month.get())
        #     return events
        # except:
        #     month = self.en_month.get()[:3]
        #     if month =="" or month == " ":
        #         return events
        #
        # return self.filter(events,month,0)

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


    def filter_product(self,events):
        """Филрътрация по продукту"""
        prod = self.en_product['text']
        if prod =="" or prod == " ":
                return events

        return self.filter(events,prod,6)


    def filter_type(self,events):
        """Фильтрует значение по типу"""
        type = self.en_type['text']
        if type =="" or type == " ":
            return events

        return self.filter(events,type,7)

    def filter_severity(self,events):
        """Фильтрует значение по уровню угрозы"""
        try:
            sev = int(self.en_severity.get())
        except:
            return events

        return self.filter(events,sev,11)

    def filter_extension(self,events):
        """Фильтрация по дополнительному полю"""
        exten = self.en_exten["text"]
        if exten == "" or exten== " ":
            return events

        return self.filter(events,exten,12)

    def filter_agent(self,events):
        """Фильтрует значение по уровню угрозы"""
        try:
            agent = int(self.en_agent.get())
        except:
            return events

        return self.filter(events,agent,13)

    def filter(self,events,sign,pos):
        """Фильтрация списка по признаку"""
        tmp = []
        for line in events:
            si = line[pos]

            if pos == 2:
                si = datetime.strptime(si,"%H:%M:%S").time()
            elif pos==6:
                si = line[6]+" "+line[7]+" "+line[8]
            elif pos==7:
                si = str(line[9])+": "+line[10]

            if sign == si:
                tmp.append(line)

        return tmp

    def filter_dates(self,events,date1,date2):
        """Фильтрует события по дате(либо равно дате либо промежуток)"""
        print(date1,date2)
        tmp = []
        for line in events:
            date = line[0]+" "+str(line[1])+" "+line[2]+" "+str(line[3])
            date = datetime.strptime(date,"%b %d %H:%M:%S %Y")
            if date2 != None and date1 <= date and date <= date2:
                tmp.append(line)
            elif date2 == None and date1 == date:
                tmp.append(line)

        return tmp



    def clear_filter(self):
        """Очищает параметры фильтрации"""
        self.en_date.delete(0,len(self.en_date.get()))
        if self.en_date2 != None:
            self.en_date2.delete(0,len(self.en_date2.get()))
        self.en_ip.delete(0,len(self.en_ip.get()))
        self.en_version.delete(0,len(self.en_version.get()))
        self.en_product['text'] =""
        self.en_type['text'] =""
        self.en_severity.delete(0,len(self.en_severity.get()))
        self.en_exten['text'] =""
        self.en_agent.delete(0,len(self.en_agent.get()))

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
        self.filling_info(tmp)

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

    def filling_info(self,events):
        """Заполняет списоков для  фильтрации"""
        if ""  not in  self.info_prod:
            self.info_prod.append("")
            self.info_type.append("")
            self.info_exten.append("")

        for line in events:
            string = line[6]+" "+line[7]+" "+line[8]
            type = str(line[9])+": "+line[10]
            exten = line[12]

            if string   not in  self.info_prod:
                self.info_prod.append(string)

            if type   not in  self.info_type:
                self.info_type.append(type)

            if exten   not in  self.info_exten:
                self.info_exten.append(exten)



    def filling_listbox_prod(self):
        """Заполнение значениями linsbox"""
        if self.lis_prod == None:
            self.top = Toplevel(self)
            self.top.title("Список ПО")
            self.lis_prod = Listbox(self.top,selectmode=SINGLE)
            self.lis_prod['height'] = len(self.info_prod)
            for line in self.info_prod:
                self.lis_prod.insert(END,line)

            yscroll =ttk.Scrollbar(self.top)
            yscroll.pack( side = RIGHT, fill=Y )

            xscroll =ttk.Scrollbar(self.top,orient=HORIZONTAL)
            xscroll.pack(side = BOTTOM, fill=X )

            self.lis_prod.config(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

            yscroll.config(command=self.lis_prod.yview)
            xscroll.config(command=self.lis_prod.xview)

            self.lis_prod.pack(side = LEFT, fill = BOTH)
            self.lis_prod.bind('<ButtonRelease>',self.filling_leb_prod)
        else:
            self.top.destroy()
            self.top=None

            self.lis_prod.destroy()
            self.lis_prod=None

    def filling_leb_prod(self,event):
        """Заполенение lab По значением"""
        self.en_product['text'] = self.lis_prod.get(self.lis_prod.curselection())

    def filling_listbox_type(self):
        """Заполнение значениями linsbox"""
        if self.lis_type == None:
            self.top_type = Toplevel(self)
            self.top_type.title("Список типов")
            self.lis_type = Listbox(self.top_type,selectmode=SINGLE)
            self.lis_type['height'] = len(self.info_type)
            for line in self.info_type:
                self.lis_type.insert(END,line)

            yscroll =ttk.Scrollbar(self.top_type)
            yscroll.pack( side = RIGHT, fill=Y )

            xscroll =ttk.Scrollbar(self.top_type,orient=HORIZONTAL)
            xscroll.pack(side = BOTTOM, fill=X )

            self.lis_type.config(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

            yscroll.config(command=self.lis_type.yview)
            xscroll.config(command=self.lis_type.xview)

            self.lis_type.pack(side = LEFT, fill = BOTH)
            self.lis_type.bind('<ButtonRelease>',self.filling_leb_type)
        else:
            self.top_type.destroy()
            self.top_type=None

            self.lis_type.destroy()
            self.lis_type=None

    def filling_leb_type(self,event):
        """Заполенение lab По значением"""
        self.en_type['text'] = self.lis_type.get(self.lis_type.curselection())

    def filling_listbox_exten(self):
        """Заполнение значениями linsbox"""
        if self.lis_exten == None:
            self.top_exten = Toplevel(self)
            self.top_exten.title("Дополнительная инфо.")
            self.lis_exten = Listbox(self.top_exten,selectmode=SINGLE)
            self.lis_exten['height'] = len(self.info_exten)
            for line in self.info_exten:
                self.lis_exten.insert(END,line)

            yscroll =ttk.Scrollbar(self.top_exten)
            yscroll.pack( side = RIGHT, fill=Y )

            xscroll =ttk.Scrollbar(self.top_exten,orient=HORIZONTAL)
            xscroll.pack(side = BOTTOM, fill=X )

            self.lis_exten.config(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

            yscroll.config(command=self.lis_exten.yview)
            xscroll.config(command=self.lis_exten.xview)

            self.lis_exten.pack(side = LEFT, fill = BOTH)
            self.lis_exten.bind('<ButtonRelease>',self.filling_leb_exten)
        else:
            self.top_exten.destroy()
            self.top_exten = None

            self.lis_exten.destroy()
            self.lis_exten = None

    def filling_leb_exten(self,event):
        """Заполенение lab exten значением"""
        self.en_exten['text'] = self.lis_exten.get(self.lis_exten.curselection())

root = Tk()
app = Panel(root)
root.mainloop()