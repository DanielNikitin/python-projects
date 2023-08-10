try:
    import requests, time, threading
    import dearpygui.dearpygui as gui
    from colorama import Fore
    import pyautogui
    import pygetwindow as gw
except:
    import os
    os.system('pip install requests')
    os.system('pip install dearpygui')
    os.system('pip install colorama')
    os.system('pip install pyautogui')
    print('restart')
    import time
    time.sleep(2)

def press_mouse_button():
    pyautogui.click(button='left')

def Thread():
    try:
        print("clicker activated")

        while True:
            if gui.get_value('on'):
                delay = gui.get_value('dl')
                press_mouse_button()
                time.sleep(delay)
                #print(Fore.LIGHTBLUE_EX + 'Mouse Button 1 Pressed', Fore.GREEN + time.strftime("%H:%M:%S"))
    except:
        print("something went wrong")

gui.create_context()
gui.create_viewport(title='Clicker by Meow', width=400, height=400)
gui.setup_dearpygui()
gui.set_viewport_always_top(True)
gui.set_viewport_resizable(False)

with gui.window(label='Spammer', width=400, height=400, no_title_bar=True, no_resize=True, no_move=True, show=True):
    with gui.tab_bar(label='Spammer'):
        with gui.tab(label='Packet'):
            gui.add_slider_float(label='Delay', tag='dl', min_value=0.0, max_value=5.0, default_value=1)
            gui.add_checkbox(label='Clicker', tag='on')

gui.show_viewport()
threading.Thread(target=Thread).start()
gui.start_dearpygui()
gui.destroy_context()