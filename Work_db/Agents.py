__author__ = 'Valentin'
# -*- coding:utf-8 -*-
#class to work with the table agent

import psycopg2


class Agents():
     def __init__(self):
         """a database connection"""
         self._dbname = "'forensic'"
         self._user = "'us_agents'"
         self._host = "'localhost'"
         self._password = "'us_agents'"

         str ="dbname="+self._dbname+" user="+self._user+" host="+self._host+" password="+self._password
         try:
             self._conn = psycopg2.connect(str)
             print("connect in Agetns table")
             self._curr = self._conn.cursor()
             self.err = 0
         except:
             print("error when connecting to Agents table")
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
             self._curr.execute("""select * from agents""")
             rows = self._curr.fetchall()
         except:
             rows = None
         return rows

     def isAgent(self,agent_id):
         """Check whether this agent_id"""
         st = "select * from agents where agent_id="+str(agent_id)
         row = None
         try:
             self._curr.execute(st)
             row = self._curr.fetchall()
         except:
             return False

         if row != None and len(row) > 0:
            return True

         return False




