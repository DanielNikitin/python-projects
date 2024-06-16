try:
    import requests, time, threading
    import dearpygui.dearpygui as gui
    from colorama import Fore
except:
    import os
    os.system('pip install requests')
    os.system('pip install threading')
    os.system('pip install dearpygui')
    os.system('pip install colorama')
    print('restart')
    import time
    time.sleep(5)

def Thread():
    while True:
        if gui.get_value('on'):
            channeltoken = gui.get_value('id')
            
            api = "https://discord.com/api/v9/channels/" +channeltoken+ "/messages"

            payload = {
            'content': gui.get_value('mes')
            }

            header = {
            'authorization' : gui.get_value('token')
            }

            time.sleep(gui.get_value('dl'))
            requests.post(api, data=payload, headers=header)

            print(Fore.LIGHTBLUE_EX + 'Send Packet', Fore.GREEN + time.strftime("%H:%M:%S"))



gui.create_context()
gui.create_viewport(title='Spammer By Susisus', width=400, height=400)
gui.setup_dearpygui()
gui.set_viewport_always_top(True)
gui.set_viewport_resizable(False)


with gui.window(label='Spammer', width=400,height=400,no_title_bar=True,no_resize=True, no_move=True, show=True):
    with gui.tab_bar(label='Spammer'):
        with gui.tab(label='Packet'):
            gui.add_input_text(label='Account Token', tag='token')
            gui.add_input_text(label='Channel ID', tag='id')
            gui.add_input_text(label='Message', tag='mes')
            gui.add_slider_float(label='Deley', tag='dl', min_value=0.0, max_value=5.0, default_value=1)
            gui.add_checkbox(label='Spamming', tag='on')


gui.show_viewport()
threading.Thread(target=Thread).start()
gui.start_dearpygui()
gui.destroy_context()