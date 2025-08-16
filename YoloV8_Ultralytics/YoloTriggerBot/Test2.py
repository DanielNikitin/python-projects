# GOVNO

import win32api
import win32con
import win32gui
import tkinter as tk
import numpy as np
import ultralytics
import multiprocessing
import math
import time 
import cv2
import mss
import random
import winsound

class Config:
    def __init__(self):
        self.width = 1920
        self.height = 1080
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.capture_width = 140
        self.capture_height = 140
        self.capture_left = self.center_x - self.capture_width // 2
        self.capture_top = self.center_y - self.capture_height // 2
        self.crosshairX = self.capture_width // 2
        self.crosshairY = self.capture_height // 2
        self.region = {
            "top": self.capture_top,
            "left": self.capture_left,
            "width": self.capture_width,
            "height": self.capture_height + 100
        }
        self.Running = True
        self.AimToggle = True
        self.delay = 0.65
        self.radius = 10
        self.target_offset_y = 0
        self.aim_threshold_x = 0.2
        self.aim_threshold_y = 0.3
        self.target_dot = None
        self.canvas = None
        self.fovC = None

global_config = Config()

def fire():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(global_config.delay)

def CreateOverlay():
    root = tk.Tk()
    root.title("Menu Window")
    root.geometry('250x650')

    def quitProgram():
        global_config.AimToggle = False
        global_config.Running = False
        root.quit()

    def DelayConfigurator(val):
        global_config.delay = float(val)

    def ManualCenterConfiguratorX(val):
        global_config.crosshairX = global_config.capture_width // 2 + int(val)
        global_config.center_x = global_config.width // 2 + int(val)
        overlay.geometry(f'150x150+{global_config.center_x - global_config.radius}+{global_config.center_y - global_config.radius}')

    def ManualCenterConfiguratorY(val):
        global_config.crosshairY = global_config.capture_height // 2 + int(val)
        global_config.center_y = global_config.height // 2 + int(val)
        overlay.geometry(f'150x150+{global_config.center_x - global_config.radius}+{global_config.center_y - global_config.radius}')

    def TargetOffsetY(val):
        global_config.target_offset_y = int(float(val))

    def AimThresholdX(val):
        global_config.aim_threshold_x = float(val)

    def AimThresholdY(val):
        global_config.aim_threshold_y = float(val)

    def CreateSlider(root, label, f, t, r, cmd, setVal):
        tk.Label(root, text=label).pack()
        s = tk.Scale(root, from_=f, to=t, resolution=r, orient=tk.HORIZONTAL, command=cmd)
        s.pack()
        s.set(setVal)

    CreateSlider(root, "Offset CenterX Manually", -100, 100, 1, ManualCenterConfiguratorX, 0)
    CreateSlider(root, "Offset CenterY Manually", -100, 100, 1, ManualCenterConfiguratorY, 0)
    CreateSlider(root, "Delay after shot", 0.003, 1.5, 0.001, DelayConfigurator, global_config.delay)
    CreateSlider(root, "Target Offset Y", -100, 100, 1, TargetOffsetY, 0)
    CreateSlider(root, "Aim Threshold X", 0.01, 1.0, 0.01, AimThresholdX, global_config.aim_threshold_x)
    CreateSlider(root, "Aim Threshold Y", 0.01, 1.0, 0.01, AimThresholdY, global_config.aim_threshold_y)

    QuitButton = tk.Button(root, text="Quit", command=quitProgram)
    QuitButton.pack()

    overlay = tk.Toplevel(root)
    overlay.geometry(f'150x150+{global_config.center_x - global_config.radius}+{global_config.center_y - global_config.radius}')
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-transparentcolor', 'blue')
    canvas = tk.Canvas(overlay, width=150, height=150, bg='blue', bd=0, highlightthickness=0)
    canvas.pack()
    global_config.canvas = canvas
    global_config.fovC = canvas.create_oval(0, 0, global_config.radius * 2, global_config.radius * 2, outline='purple')

    def update_dot():
        try:
            while not update_queue.empty():
                x, y = update_queue.get_nowait()
                if global_config.target_dot:
                    canvas.coords(global_config.target_dot, x - 3, y - 3, x + 3, y + 3)
                else:
                    global_config.target_dot = canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")
        except:
            pass
        root.after(50, update_dot)

    def update_crosshair():
        try:
            color = 'hotpink' if global_config.AimToggle else 'red'
            canvas.itemconfig(global_config.fovC, outline=color)
        except:
            pass
        root.after(500, update_crosshair)

    update_dot()
    update_crosshair()
    root.mainloop()

def model_worker(update_queue, stop_event):
    model = ultralytics.YOLO("best.pt")
    screen = mss.mss()
    prev_time = time.time()

    while not stop_event.is_set():
        if not global_config.AimToggle:
            time.sleep(0.1)
            continue

        frame = np.array(screen.grab(global_config.region))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        results = model.predict(source=frame, conf=0.4, classes=[0, 2], verbose=False, max_det=10)
        boxes = results[0].boxes.xyxy

        if len(boxes) > 0:
            x1, y1, x2, y2 = boxes[0].tolist()
            dx, dy = x2 - x1, y2 - y1
            target_x = int(x1 + dx / 2)
            target_y = int(y1 + dy / 3) + global_config.target_offset_y
            moveX = target_x - global_config.crosshairX
            moveY = target_y - global_config.crosshairY
            update_queue.put((global_config.crosshairX + moveX, global_config.crosshairY + moveY))

            aim_threshold_x = dx * global_config.aim_threshold_x
            aim_threshold_y = dy * global_config.aim_threshold_y

            if abs(moveX) <= aim_threshold_x and abs(moveY) <= aim_threshold_y:
                fire()

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imshow("Game Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    update_queue = multiprocessing.Queue()
    stop_event = multiprocessing.Event()
    gui_process = multiprocessing.Process(target=CreateOverlay)
    model_process = multiprocessing.Process(target=model_worker, args=(update_queue, stop_event))
    gui_process.start()
    model_process.start()
    gui_process.join()
    stop_event.set()
    model_process.join()
