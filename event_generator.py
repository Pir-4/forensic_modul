__author__ = 'Valentin'
# -*- coding:utf-8 -*-
# генерирует события в формате CEF
import time

def get_time():
    """Получение текущего времени"""
    strin = str(time.ctime(time.time()))[4:]
    return strin

def get_Antivir():
    """Форирование сообщения в CEF формате для антивируса"""
    cef = "CEF:0|McAfee|Antivirus|5.2|2|worm successful stopped|10|"
    cef +="src=10.0.0.1 dst=2.1.2.2 spt=1232"
    cef = get_time()+" host "+ cef
    return cef
def get_OS():
    """Форирование сообщения в CEF формате для ОСа"""
    cef = "CEF:0|Microsoft|Windows7|5.3|1|authentication|4|"
    cef +="login=Sweetie result=success"
    cef = get_time()+" host "+ cef
    return cef
def get_OS_ip():
    """Форирование сообщения в CEF формате для ОСа"""
    cef = "CEF:0|Microsoft|Windows7|5.3|1|authentication|4|"
    cef +="login=Sweetie result=success ip=192.168.1.1"
    cef = get_time()+" host "+ cef
    return cef

# print(get_OS())