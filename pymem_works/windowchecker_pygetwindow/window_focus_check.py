import pygetwindow as gw

def main():
    try:
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


main()