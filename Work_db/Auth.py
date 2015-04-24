__author__ = 'Valentin'
# -*- coding:utf-8 -*-
#класс для работы с таблицей auth

import psycopg2


class Auth():
     def __init__(self):
         """соединения с базой данных"""
         self._dbname = "'forensic'"
         self._user = "'postgres'"
         self._host = "'localhost'"
         self._password = "'valentin'"

         str ="dbname="+self._dbname+" user="+self._user+" host="+self._host+" password="+self._password
         try:
             self._conn = psycopg2.connect(str)
             print("connect in Auth table")
             self._curr = self._conn.cursor()
             self.err = 0
         except:
             print("error when connecting to Auth table")
             self.err = 1

     def __del__(self):
         #при уничтоении объекта закрывается соедениение
         try:
            self._curr.close()
            self._conn.close()
         except:
             print("error disconnect Auth table")

     def out_table(self):
         """получение из таблицы всех строк"""
         try:
             self._curr.execute("""select * from auth""")
             rows = self._curr.fetchall()
         except:
             rows = None
         return rows

     def set_row(self,row):
         """вставка строки в таблицу"""
         str = "insert into auth (event_id,user_id,ip,result) " \
               "values (%s,%s,%s,%s);"
         try:
             self._curr.execute(str,row)
             self._conn.commit()
         except:
             print("error insert row un table")
             return -1

         return 0

