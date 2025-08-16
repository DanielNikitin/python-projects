# работает, но не супер, подкачка из файла идет координат

import time
import win32api
import win32con
import keyboard

def smooth_mouse_move(dx, dy, steps=10, step_delay=0.01):
    step_dx = dx / steps
    step_dy = dy / steps
    for _ in range(steps):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(step_dx), int(step_dy), 0, 0)
        time.sleep(step_delay)

def load_spray_pattern(filename):
    with open(filename, "r") as f:
        content = f.read()
        return eval(content)

def main():
    filename = "ak.txt"
    spray_pattern = load_spray_pattern(filename)

    toggle_button = 'num lock'
    enabled = False
    last_state = False

    print("Spray control started. Toggle with Num Lock.")

    while True:
        key_down = keyboard.is_pressed(toggle_button)
        if key_down != last_state:
            last_state = key_down
            if last_state:
                enabled = not enabled
                print(f"Spray control {'ENABLED' if enabled else 'DISABLED'}")

        if enabled and win32api.GetKeyState(0x01) < 0:  # ЛКМ зажата
            for dx, dy in spray_pattern:
                smooth_mouse_move(dx, dy, steps=10, step_delay=0.006)  # плавное движение ~100 мс
                time.sleep(0.01)  # небольшой буфер после движения

                if win32api.GetKeyState(0x01) >= 0:
                    break
        else:
            time.sleep(0.01)

if __name__ == "__main__":
    main()
