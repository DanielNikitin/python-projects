import pymem
import pygetwindow as gw

dwEntityList = 0x81788796
dwGlowObjectManager = 0x87403016
m_iGlowIndex = 0x66696

pm = pymem.Pymem("csgo.exe")
cliencatach = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll


def main():
    try:
        print("glow activated")
        prev_focus_state = None

        while True:
            active_window = gw.getActiveWindow()
            if active_window and "Counter-Strike: Global Offensive" in active_window.title:
                current_focus_state = True
            else:
                current_focus_state = False

            if current_focus_state != prev_focus_state:
                if current_focus_state:
                    print("CS:GO is in focus.")
                else:
                    print("CS:GO is not in focus.")
                prev_focus_state = current_focus_state
    except:
        pass


def glowmodule():
    while True:
        glow = pm.read_int(cliencatach + dwGlowObjectManager)

        for i in range(0, 32):
            entity = pm.read_int(cliencatach + dwEntityList + i *0x10)
            if entity:
                entityglowing = pm.read_int(entity+m_iGlowIndex)

                pm.write_float(glow + entityglowing * 0x38 + 0x8, float(0))
                pm.write_float(glow + entityglowing * 0x38 + 0xC, float(1))
                pm.write_float(glow + entityglowing * 0x38 + 0x10, float(0))
                pm.write_float(glow + entityglowing * 0x38 + 0x14, float(1))
                pm.write_float(glow + entityglowing * 0x38 + 0x28, 1)

if __name__ == '__main__':
    main()