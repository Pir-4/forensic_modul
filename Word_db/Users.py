__author__ = 'Valentin'
# -*- coding:utf-8 -*-
#класс для работы с таблицей Users

import psycopg2

class Users():
        def __init__(self):
            """соединения с базой данных"""
            self._dbname = "'forensic'"
            self._user = "'postgres'"
            self._host = "'localhost'"
            self._password = "'valentin'"

            str ="dbname="+self._dbname+" user="+self._user+" host="+self._host+" password="+self._password
            try:
                self._conn = psycopg2.connect(str)
                print("connect in Users table")
                self._curr = self._conn.cursor()
                self.err = 0
            except:
                print("error when connecting to Users table")
                self.err = 1

        def __del__(self):
            #при уничтоении объекта закрывается соедениение
            try:
                self._curr.close()
                self._conn.close()
            except:
                print("error disconnect Users table")


        def out_table(self):
            """получение из таблицы всех строк"""
            try:
                self._curr.execute("""select * from users""")
                rows = self._curr.fetchall()
            except:
                rows = None
            return rows

        def get_id(self,login):
            # """получение id польззователя по логину"""
            st = "select user_id from users where login='"+login+"'"
            try:
                self._curr.execute(st)
                row = self._curr.fetchall()
                return row[0][0]
            except:
                row = 0
                return row
