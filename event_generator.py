__author__ = 'Valentin'
# -*- coding:utf-8 -*-
# generates event format CEF
import time

def get_time():
    """getting the current time"""
    strin = str(time.ctime(time.time()))[4:]
    return strin

def get_Antivir():
    """the formation of a message format for antivirus CEF"""
    cef = "CEF:0|McAfee|Antivirus|5.2|2|worm successful stopped|10|"
    cef +="src=10.0.0.1 dst=2.1.2.2 spt=1232"
    cef = get_time()+" host "+ cef
    return cef
def get_OS():
    """the formation of a message format for OS CEF"""
    cef = "CEF:0|Microsoft|Windows7|5.3|1|authentication|4|"
    cef +="login=Sweetie result=success"
    cef = get_time()+" host "+ cef
    return cef
def get_OS_ip():
    """the formation of a message format for OS CEF"""
    cef = "CEF:0|Microsoft|Windows7|5.3|1|authentication|4|"
    cef +="login=Sweetie result=success ip=192.168.1.1"
    cef = get_time()+" host "+ cef
    return cef

# print(get_OS())