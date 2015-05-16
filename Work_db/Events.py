__author__ = 'Valentin'
# -*- coding:utf-8 -*-
#класс для работы с таблицей Events

import psycopg2


class Events():
     def __init__(self):
         """соединения с базой данных"""
         self._dbname = "'forensic'"
         self._user = "'postgres'"
         self._host = "'localhost'"
         self._password = "'valentin'"

         str ="dbname="+self._dbname+" user="+self._user+" host="+self._host+" password="+self._password
         try:
             self._conn = psycopg2.connect(str)
             print("connect in Events table")
             self._curr = self._conn.cursor()
             self.err = 0
         except:
             print("error when connecting to Event table")
             self.err = 1

     def __del__(self):
         #при уничтоении объекта закрывается соедениение
         try:
            self._curr.close()
            self._conn.close()
         except:
             print("error disconnect Event table")

     def out_table(self):
         """получение из таблицы всех строк"""
         try:
             self._curr.execute("""select * from events""")
             rows = self._curr.fetchall()
         except:
             rows = None
         return rows

     def set_row(self,row):
         """вставка строки в таблицу"""
         str = "insert into events (date,host,device_vendor,device_product,device_version,event_type,user_id,agent_id) " \
               "values (%s,%s,%s,%s,%s,%s,%s,%s);"
         try:
             self._curr.execute(str,row)
             self._conn.commit()
             return self.get_last_id()
         except:
             print("error insert row in Events table")
             return -1

         return 0
     def get_last_id(self):
         """возвращяет id последнего события """
         st = "select  * from events order by event_id desc limit 1"
         try:
            self._curr.execute(st)
            row = self._curr.fetchall()
            return row[0][0]
         except:
            row = None
            return row

     def get_row(self,event_id):
         """Получение строки по event_id"""
         st = "select * from events where event_id="+str(event_id)
         try:
             self._curr.execute(st)
             row = self._curr.fetchall()
             return  row[0]
         except:
             row = None
             return  row

     def get_table_type(self,event_id):
         """Получение информации о типе события по event_id"""
         st = "select evs.event_id,evt.name_table,evt.sevarity,evt.description " \
              "from events as evs join event_type as evt " \
              "on evs.event_type = evt.event_type where evs.event_id ="+str(event_id)
         try:
             self._curr.execute(st)
             row = self._curr.fetchall()
             return row[0]
         except:
             row = None
             return  row

     def get_event_id(self,event_id):
         """Получеам список всех id которые больше или равные заданому"""
         st = "select event_id from events where event_id >="+str(event_id)
         try:
             self._curr.execute(st)
             tmp = self._curr.fetchall()
             row = []
             for elem in tmp:
                 row.append(elem[0])
             return row
         except:
             row = None
             return  row
