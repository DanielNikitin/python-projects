import keyboard
import pymem
import pymem.process
import time
import pygetwindow as gw

dwForceJump = 0x52BBCD8
dwLocalPlayer = 0xDEA98C
m_fFlags = 0x104

def main():
    try:
        print("BunnyMode is Activated")
        pm = pymem.Pymem("csgo.exe")
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

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

            if current_focus_state:
                if keyboard.is_pressed("space"):
                    force_jump = client + dwForceJump
                    player = pm.read_int(client + dwLocalPlayer)
                    if player:
                        on_ground = pm.read_int(player + m_fFlags)
                        if on_ground and on_ground == 257:
                            pm.write_int(force_jump, 5)
                            time.sleep(0.08)
                            pm.write_int(force_jump, 4)

            time.sleep(0.002)
    except KeyboardInterrupt:
        print("Script is Deactivated")

if __name__ == '__main__':
    main()
