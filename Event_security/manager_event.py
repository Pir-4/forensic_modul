__author__ = 'valentin'
# -*- coding:utf-8 -*-

import thread as thread
import event_OS

class Manger():
    """It controls the flow of information gathering events"""
    def __init__(self):
        self._os = event_OS.Event_OS(3451)

    def dispecher(self):
        """multithreading"""
        # while True:
        #     thread.start_new(self._os.reading,())
        self._os.reading()


mg = Manger()
mg.dispecher()