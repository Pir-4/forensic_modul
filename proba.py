import hashlib
# -*- coding:utf-8 -*-
# def gethash(str):
#     #
#     h = hashlib.sha1()
#     str = str.encode("utf8")
#     h.update(str)
#     return h.hexdigest()
# def del_row(self,sing):
     #     #удаление
     #     field = sing[0]
     #     value = sing[1]
     #     str  = "delete from events where "+field+"='"+value+"';"
     #     try:
     #         self._curr.execute(str)
     #         self._conn.commit()
     #     except:
     #         print("error 'execute' in table")
     #         return 1
     #
     #     return 0

     # def correct_row(self,sing):
     #     """изменение строки"""
     #     field1 = sing[0]
     #     value1 = sing[1]
     #     field2 = sing[2]
     #     value2 = sing[3]
     #     str = "update events set " +field1+ "='" +value1+ "' where " +field2+ "='" +value2+ "';"
     #     try:
     #         self._curr.execute(str)
     #         self._conn.commit()
     #     except:
     #         print("error 'execute' in table")
     #         return 1
     #
     #     return 0
     # def get_row(self,sing):
     #     """получение отдельной строки из таблицы по признаку"""
     #     field = sing [0]
     #     value = sing [1]
     #     str = "select id,name,salary from events where " +field+ "='" +value+ "'"
     #     try:
     #         self._curr.execute(str)
     #         row = self._curr.fetchall()
     #     except:
     #         row = None
     #
     #     return row
from libxml2 import libxmlError

import sys
import  platform
print("system:",platform.system())
print("distribut:",platform.dist())
print("version:",platform.version())

