__author__ = 'Valentin'
# -*- coding:utf-8 -*-
#класс для работы с таблицей Event_type

import psycopg2

class Event_type():
        def __init__(self):
            """соединения с базой данных"""
            self._dbname = "'forensic'"
            self._user = "'postgres'"
            self._host = "'localhost'"
            self._password = "'valentin'"

            str ="dbname="+self._dbname+" user="+self._user+" host="+self._host+" password="+self._password
            try:
                self._conn = psycopg2.connect(str)
                print("connect in Event_type table")
                self._curr = self._conn.cursor()
                self.err = 0
            except:
                print("error when connecting to Event_type table")
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
                self._curr.execute("""select * from event_type""")
                rows = self._curr.fetchall()
            except:
                rows = None
            return rows

        def check_type(self,type):
            # """получение имя таблицы по типу"""
            st = "select name_table from event_type where event_type="+str(type)
            try:
                self._curr.execute(st)
                row = self._curr.fetchall()
                return str(row[0][0])
            except:
                row = None
                return row

        def find_type(self,sign):
            """Поиск по признаку в бд. для опередения типа поступившего события"""
            rows = self.out_table()
            for row in rows:
                strin = row[4]
                st =strin.find(sign+";",0,len(strin))
                if st != -1:
                    return row

            return None
