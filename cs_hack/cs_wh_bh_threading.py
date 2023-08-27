import pymem.process
from threading import *
import keyboard
import time


#offsets
dwForceJump = 0x52BBCD8
dwLocalPlayer = 0xDEA98C
dwEntityList = 0x4DFFF7C
dwGlowObjectManager = 0x535AA08
m_iGlowIndex = 0x10488
dwForceAttack = 0x322EE5C
m_iCrosshairId = 0x11838
m_iTeamNum = 0xF4
m_iDefaultFOV = 0x333C
m_flFlashMaxAlpha = 0x1046C
dwClientState = 0x59F19C

try:
    pm = pymem.Pymem('csgo.exe')
    client = pymem.pymem.process.module_from_name(pm.process_handle, 'client.dll').lpBaseOfDll
except:
    print('turn on cs:go')
    exit(0)


def main():
    glow()

def bhop():
    # Если игрок находится на земле, то меняем одно значение на другое
    while True:
        plr = pm.read_uint(client + dwLocalPlayer)
        if keyboard.is_pressed('space'):
            if pm.read_int(plr + 0x104) == 257:
                pm.write_int((client + dwForceJump), 6)
                time.sleep(0.0001)
                pm.write_int((client + dwForceJump), 4)

def glow():
    while True:
        try:
            glow = pm.read_int(client + dwGlowObjectManager)
            # Вычитывает значение из памяти по адресу client + dwGlowObjectManager
            # с помощью функции pm.read_int() и присваивает его переменной glow.
            for i in range(0, 32):  # запуска цикла от 0 до 32 раз
                entity = pm.read_int(client + dwEntityList + i * 0x10)
                # Вычитывает значение из памяти по адресу client + dwEntityList + i * 0x10
                # и присваивает его переменной entity.
                if entity:  # проверяет, существует ли значение переменной entity
                    entityglowing = pm.read_int(entity + m_iGlowIndex)
                    # Вычитывает значение из памяти по адресу entity + m_iGlowIndex
                    # и присваивает его переменной entityglowing.
                    pm.write_float(glow + entityglowing * 0x38 + 0x8, float(0))  # R
                    pm.write_float(glow + entityglowing * 0x38 + 0xC, float(0))  # G
                    pm.write_float(glow + entityglowing * 0x38 + 0x10, float(1))  # B
                    pm.write_float(glow + entityglowing * 0x38 + 0x14, float(1))  # Alfa (прозрачность)
                    pm.write_int(glow + entityglowing * 0x38 + 0x28, 1)
                    # Записывает значение 1 в память по адресу
                    # glow + entityglowing * 0x38 + 0x28
        except:
            print("restart")

t1 = Thread(target = glow)
t2 = Thread(target = bhop)

if __name__ == '__main__':
    t1.start()
    t2.start()