#import keyboard
import pymem
import pymem.process
import time
import pygetwindow as gw

dwEntityList = 0x4DFFF7C
dwGlowObjectManager = 0x535AA08
m_iGlowIndex = 0x10488
m_iTeamNum = 0xF4
m_iHealth = 0x100
dwLocalPlayer = 0xDEA98C

def main():
    try:
        print("Diamond has launched.")
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

            glow_manager = pm.read_int(client + dwGlowObjectManager)

            for i in range(1, 32):  # Entities 1-32 are reserved for players.
                entity = pm.read_int(client + dwEntityList + i * 0x10)

                if entity:
                    entity_team_id = pm.read_int(entity + m_iTeamNum)
                    entity_glow = pm.read_int(entity + m_iGlowIndex)

                    if entity_team_id == 2:  # Terrorist
                        print("Terrorist Entity:", i)
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))   # R
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))   # B
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow

                    elif entity_team_id == 3:  # Counter-terrorist
                        print("Counter-Terrorist Entity:", i)
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))   # R
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))   # B
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow

            player = pm.read_int(client + dwLocalPlayer)
            health = pm.read_int(player + m_iHealth)
            #print("Player Health:", health)

    except KeyboardInterrupt:
        print("Deactivated")


if __name__ == '__main__':
    main()
