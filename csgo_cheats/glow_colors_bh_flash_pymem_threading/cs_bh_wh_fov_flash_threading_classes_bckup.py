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

init()  # запуск colorama


#offsets 13.09.2023
dwForceJump = 0x52BBCD8
dwLocalPlayer = 0xDEB99C
dwEntityList = 0x4E0102C
dwGlowObjectManager = 0x535BAD0
m_iGlowIndex = 0x10488
dwForceAttack = 0x322EE98
m_iCrosshairId = 0x11838
m_iTeamNum = 0xF4
m_flFlashMaxAlpha = 0x1046C
m_iDefaultFOV = 0x333C
m_iHealth = 0x100
m_vecOrigin = 0x138
dwViewMatrix = 0x4DF1E74
m_fFlags = 0x104

bh = 1
wh = 1
color = 4
flash = 1

print(f"bh = {bh}")
print(f"wh = {wh}")
print(f"flash = {flash}")

try:
    pm = pymem.Pymem('csgo.exe')
    client = pymem.process.module_from_name(pm.process_handle, 'client.dll').lpBaseOfDll
except:
    print('turn on cs:go')
    exit(0)


class Process:
    def glow(self):
        if color == 4:  # cyan
            try:
                glow = pm.read_int(client + dwGlowObjectManager)
                for i in range(0, 32):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)
                    if entity:
                        entityglowing = pm.read_int(entity + m_iGlowIndex)
                        pm.write_float(glow + entityglowing * 0x38 + 0x8, float(0))
                        pm.write_float(glow + entityglowing * 0x38 + 0xC, float(1))
                        pm.write_float(glow + entityglowing * 0x38 + 0x10, float(1))
                        pm.write_float(glow + entityglowing * 0x38 + 0x14, float(1))
                        pm.write_int(glow + entityglowing * 0x38 + 0x28, 1)
            except:
                print("cyan error")

        elif color == 7 or color == '7':  # pink
            try:
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
            except:
                print("pink error")

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


def Thread():
    while True:
        if bh == 1 or bh == '1':
            start_script.bhop()
        if wh == 1 or wh == '1':
            start_script.glow()
        if flash == 1 or flash == '1':
            start_script.flash()
    # --- END BUTTON ---
        if keyboard.is_pressed("end"):
            exit(0)


start_script = Process()
threading.Thread(target = Thread).start()