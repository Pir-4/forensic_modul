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
         str = "insert into events (date,host,device_vendor,device_product,device_version,event_type,user_id) " \
               "values (%s,%s,%s,%s,%s,%s,%s);"
         try:
             self._curr.execute(str,row)
             self._conn.commit()
             return self.get_id()
         except:
             print("error insert row un table")
             return -1

         return 0
     def get_id(self):
         """возвращяет id последнего события """
         st = "select  * from events order by event_id desc limit 1"
         try:
            self._curr.execute(st)
            row = self._curr.fetchall()
            return row[0][0]
         except:
            row = None
            return row

