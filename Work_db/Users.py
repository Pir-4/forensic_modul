__author__ = 'Valentin'
# -*- coding:utf-8 -*-
#class to work with the Users table

import psycopg2

class Users():
        def __init__(self):
            """a database connection"""
            self._dbname = "'forensic'"
            self._user = "'us_users'"
            self._host = "'localhost'"
            self._password = "'us_users'"

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
            #when an object is destroyed the connection is closed
            try:
                self._curr.close()
                self._conn.close()
            except:
                print("error disconnect Users table")


        def out_table(self):
            """getting all the rows from a table"""
            try:
                self._curr.execute("""select * from users""")
                rows = self._curr.fetchall()
            except:
                rows = None
            return rows

        def get_id(self,login):
            # """obtain a login user id"""
            st = "select user_id from users where login='"+login+"'"
            try:
                self._curr.execute(st)
                row = self._curr.fetchall()
                return row[0][0]
            except:
                row = 0
                return row
