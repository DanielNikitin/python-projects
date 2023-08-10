import keyboard
import pymem.process
import time
import threading

#offsets
dwForceJump = 0x52BBCD8
dwLocalPlayer = 0xDEA98C
dwEntityList = 0x4DFFF7C
dwGlowObjectManager = 0x535AA08
m_iGlowIndex = 0x10488
dwForceAttack = 0x322DDE8
m_iCrosshairId = 0x11838
m_iTeamNum = 0xF4
m_flFlashMaxAlpha = 0x1046C
m_iDefaultFOV = 0x333C
m_iHealth = 0x100
m_vecOrigin = 0x138
dwViewMatrix = 0x4DF0DC4
m_fFlags = 0x104

bh = int(input("bh 1 - on / 0 - off :"))
wh = int(input("wh 1 - on / 0 - off :"))
fov = int(input("fov 1 - on / 0 - off :"))
flash = int(input("flash 1 - on / 0 - off :"))

try:
    if wh > 0:
        color = int(input("color | green = 1, blue = 2, red = 3, cyan = 4, white = 5, yellow = 6, pink = 7 | :"))
    else:
        print("enything choised")
except:
    print("error")

try:
    pm = pymem.Pymem('csgo.exe')
    client = pymem.pymem.process.module_from_name(pm.process_handle, 'client.dll').lpBaseOfDll
except:
    print('turn on cs:go')
    exit(0)

class Process:
    def glow(self):
        if color == 1 or color == '1':  # color равенство 1 или строке '1'
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
                        pm.write_float(glow + entityglowing * 0x38 + 0xC, float(1))  # G
                        pm.write_float(glow + entityglowing * 0x38 + 0x10, float(0))  # B
                        pm.write_float(glow + entityglowing * 0x38 + 0x14, float(1))  # Alfa
                        pm.write_int(glow + entityglowing * 0x38 + 0x28, 1) # Activation
                        # Записывает значение 1 в память по адресу
                        # glow + entityglowing * 0x38 + 0x28
            except:
                print("restart")
        elif color == 2 or color == '2':
            try:
                glow = pm.read_int(client + dwGlowObjectManager)
                for i in range(0, 32):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)
                    if entity:
                        entityglowing = pm.read_int(entity + m_iGlowIndex)
                        pm.write_float(glow + entityglowing * 0x38 + 0x8, float(0))
                        pm.write_float(glow + entityglowing * 0x38 + 0xC, float(0))
                        pm.write_float(glow + entityglowing * 0x38 + 0x10, float(1))
                        pm.write_float(glow + entityglowing * 0x38 + 0x14, float(1))
                        pm.write_int(glow + entityglowing * 0x38 + 0x28, 1)
            except:
                print("restart")
        elif color == 3 or color == '3':
            try:
                glow = pm.read_int(client + dwGlowObjectManager)
                for i in range(0, 32):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)
                    if entity:
                        entityglowing = pm.read_int(entity + m_iGlowIndex)
                        pm.write_float(glow + entityglowing * 0x38 + 0x8, float(1))
                        pm.write_float(glow + entityglowing * 0x38 + 0xC, float(0))
                        pm.write_float(glow + entityglowing * 0x38 + 0x10, float(0))
                        pm.write_float(glow + entityglowing * 0x38 + 0x14, float(1))
                        pm.write_int(glow + entityglowing * 0x38 + 0x28, 1)
            except:
                print("restart")
        elif color == 4 or color == '4':
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
                print("restart")
        elif color == 5 or color == '5':
            try:
                glow = pm.read_int(client + dwGlowObjectManager)
                for i in range(0, 32):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)
                    if entity:
                        entityglowing = pm.read_int(entity + m_iGlowIndex)
                        pm.write_float(glow + entityglowing * 0x38 + 0x8, float(1))
                        pm.write_float(glow + entityglowing * 0x38 + 0xC, float(1))
                        pm.write_float(glow + entityglowing * 0x38 + 0x10, float(1))
                        pm.write_float(glow + entityglowing * 0x38 + 0x14, float(1))
                        pm.write_int(glow + entityglowing * 0x38 + 0x28, 1)
            except:
                print("restart")
        elif color == 6 or color == '6':
            try:
                glow = pm.read_int(client + dwGlowObjectManager)
                for i in range(0, 32):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)
                    if entity:
                        entityglowing = pm.read_int(entity + m_iGlowIndex)
                        pm.write_float(glow + entityglowing * 0x38 + 0x8, float(1))
                        pm.write_float(glow + entityglowing * 0x38 + 0xC, float(1))
                        pm.write_float(glow + entityglowing * 0x38 + 0x10, float(0))
                        pm.write_float(glow + entityglowing * 0x38 + 0x14, float(1))
                        pm.write_int(glow + entityglowing * 0x38 + 0x28, 1)
            except:
                print("restart")
        elif color == 7 or color == '7':
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
                print("restart")

    def bhop(self):
        # Если игрок находится на земле, то меняем одно значение на другое
            plr = pm.read_uint(client + dwLocalPlayer)
            if keyboard.is_pressed('space'):
                if pm.read_int(plr + 0x104) == 257:
                    pm.write_int((client + dwForceJump), 6)
                    time.sleep(0.0001)
                    pm.write_int((client + dwForceJump), 4)

    def fov(self):
        player = pm.read_uint(client + dwLocalPlayer)
        pm.write_int(player + m_iDefaultFOV)

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
        if fov == 1 or fov == '1':
            start_script.fov()
        if flash == 1 or flash == '1':
            start_script.flash()
    # --- END BUTTON ---
        if keyboard.is_pressed("end"):
            exit(0)

start_script = Process()
threading.Thread(target = Thread).start()