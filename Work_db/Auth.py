__author__ = 'Valentin'
# -*- coding:utf-8 -*-
#class to work table auth

import psycopg2


class Auth():
     def __init__(self):
         """a database connection"""
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
         #when an object is destroyed the connection is closed
         try:
            self._curr.close()
            self._conn.close()
         except:
             print("error disconnect Auth table")

     def out_table(self):
         """getting all the rows from a table"""
         try:
             self._curr.execute("""select * from auth""")
             rows = self._curr.fetchall()
         except:
             rows = None
         return rows

     def set_row(self,row):
         """Inserting a row in a table"""
         str = "insert into auth (event_id,user_id,ip,result) " \
               "values (%s,%s,%s,%s);"
         try:
             self._curr.execute(str,row)
             self._conn.commit()
         except:
             print("error insert row in Auth table")
             return -1

         return 0

     def get_info(self,event_id):
         """Getting information about the authorization of event_id"""
         st = "select us.login,au.result,au.ip " \
              "from auth as au join users as us " \
              "on au.user_id = us.user_id where au.event_id ="+str(event_id)
         try:
             self._curr.execute(st)
             row = self._curr.fetchall()
             return  row[0]
         except:
             row = None
             return  row

     def get_cef(self,event_id):
         """getting table fields in the format of cef event_id"""
         row = self.get_info(event_id)
         if row != None:
             cef = "user="+str(row[0])
             if row[2] != "NULL":
                 cef += " ip="+str(row[2])
             cef += " result="+str(row[1])
             return str(cef)
         return None


