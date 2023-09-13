import keyboard
import pymem
import pymem.process
import time
import datetime
import threading
import re
import configparser
import random
import os
import ctypes
from colorama import Fore, init
from offsets import *

init()  # Запуск colorama

def current_time():
    return datetime.datetime.now().strftime('[%H:%M:%S]')

statusWH = False
statusFlash = False

wh = 0

key1 = "f2"  # WH
key2 = "f2"  # Flash
key3 = "f3"  # Exit


def toggle():
    try:
        pm = pymem.Pymem('csgo.exe')
        client = pymem.process.module_from_name(pm.process_handle, 'client.dll').lpBaseOfDll
        glow = pm.read_int(client + dwGlowObjectManager)
        for i in range(0, 32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)
            if entity:
                entityglowing = pm.read_int(entity + m_iGlowIndex)
                pm.write_float(glow + entityglowing * 0x38 + 0x8, float(1))
                pm.write_float(glow + entityglowing * 0x38 + 0xC, float(0))
                pm.write_float(glow + entityglowing * 0x38 + 0x10, float(1))
                pm.write_float(glow + entityglowing * 0x38 + 0x14, float(1))
                pm.write_int(glow + entityglowing * 0x38 + 0x28, 1)
    except pymem.exception.ProcessNotFound:
        print(Fore.YELLOW + current_time(), Fore.RED + '[test] csgo.exe process is not running!')

def Thread():
    while True:
        toggle()

def test():
    if wh == 1:
        Thread()

# Класс Process
class Process:
    def bhop(self):
        # Если игрок находится на земле, то меняем одно значение на другое
        plr = pm.read_uint(client + dwLocalPlayer)
        if keyboard.is_pressed('space'):
            if pm.read_int(plr + 0x104) == 257:
                pm.write_int((client + dwForceJump), 6)
                time.sleep(0.0001)
                pm.write_int((client + dwForceJump), 4)

    def flash(self):
        plr3 = pm.read_int(client + dwLocalPlayer)
        flash_value = plr3 + m_flFlashMaxAlpha
        pm.write_float(flash_value, float(0))

def exit_program():
    print(Fore.RED + "Exit...")
    os.abort()


start_script = Process()
threading.Thread(target = test).start()

keyboard.add_hotkey(key1, test2)
keyboard.wait()
