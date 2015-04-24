__author__ = 'valentin'
# -*- coding:utf-8 -*-
#поределяет вид операционной системы и работает с ее событиями безопасности

import sys
import platform

class Event_OS():
    def __init__(self):
        self._system = str(platform.system())
        self._dist = platform.dist()
        self._version = str(platform.version())
        if self._system == 'Linux':
            self.flagOS = True
        else:
            """если ос это windows"""
            self.flagOS = False

    def get_cef(self):
        """получем сообщение в формате cef"""
        self._cef = self._system + '|' + self._dist[0]+self._dist[1]+'|'+self._version +'|'
        return  self._cef


event = Event_OS()
print(event.get_cef())