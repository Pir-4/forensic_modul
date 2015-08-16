__author__ = 'Valentin'
# -*- coding:utf-8 -*-
#class to work with the table Event_type

import psycopg2

class Event_type():
        def __init__(self):
            """a database connection"""
            self._dbname = "'forensic'"
            self._user = "'us_ev_type'"
            self._host = "'localhost'"
            self._password = "'us_ev_type'"

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
            #when an object is destroyed the connection is closed
            try:
                self._curr.close()
                self._conn.close()
            except:
                print("error disconnect Event table")


        def out_table(self):
            """getting all the rows from a table"""
            try:
                self._curr.execute("""select * from event_type""")
                rows = self._curr.fetchall()
            except:
                rows = None
            return rows

        def check_type(self,type):
            # """getting the name of the table by type"""
            st = "select name_table from event_type where event_type="+str(type)
            try:
                self._curr.execute(st)
                row = self._curr.fetchall()
                return str(row[0][0])
            except:
                row = None
                return row

        def find_type(self,sign):
            """Search on the grounds of the database. to determine the type of events entered"""
            rows = self.out_table()
            if rows != None:
                for row in rows:
                    strin = row[4]
                    st =strin.find(sign+";",0,len(strin))
                    if st != -1:
                        return row
            return None
