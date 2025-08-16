# FPS 25-30

import win32api, win32con, winsound

import tkinter as tk
import numpy as np

import ultralytics
import cv2, math, time
import mss

import multiprocessing, threading

import sys, os

from queue import Queue, Full, Empty

from fps import FPS

# CONFIG
class Config:
    def __init__(self):

        self.width = 1920  # Main window Size not Game
        self.height = 1080
        
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        
        # small window
        self.capture_width = 160  # Area for detecting X
        self.capture_height = 160  # Area for detecting Y

        self.capture_left = self.center_x - self.capture_width // 2
        self.capture_top = self.center_y - self.capture_height // 2
        self.crosshairX = self.capture_width // 2
        self.crosshairY = self.capture_height // 2
        
        # Rectangle area for AI detecting and after sending to mss.grab(config.region)
        self.region = {
            "top": self.capture_top,
            "left": self.capture_left,
            "width": self.capture_width,
            "height": self.capture_height + 100
        }

        self.Running = True
        self.AimToggle = True

        self.delay = 0 # shoot delay
        self.radius = 10 # crosshair size

        self.target_offset_y = 0

        self.detect_classes = [0, 2]  # CT / T
        self.target_name = "T"

        self.toggle_key = {'ctrl': 162, 't': 84}  # virtual key codes

config = Config()

is_firing = False

def CreateOverlay(q):

    print("Overlay is Started")

    root = tk.Tk()
    root.title("Menu Ai")
    root.geometry('250x450')  # Size
    tk.Label(root, text="AI menu title", font=("Helvetica", 14)).pack()
    
    def quitProgram():
        config.AimToggle = False
        config.Running = False
        root.quit()
    
    def send_updates_to_queue(q):
        if not q.full():
            q.put({
                'delay': config.delay,
                'target_offset_y': config.target_offset_y,
            })


    # DELAY
    def DelayConfigurator(Delay):
        config.delay = float(Delay)
        send_updates_to_queue(q)


    def OffsetYConfigurator(val):
        config.target_offset_y = int(val)
        send_updates_to_queue(q)


    # MANUAL CENTER X
    def ManualCenterConfiguratorX(ValueX):
        config.crosshairX =  config.capture_width // 2 + int(ValueX)
        config.center_x = config.width // 2 + int(ValueX)
        overlay.geometry(f'150x150+{str(config.center_x - config.radius)}+{str(config.center_y - config.radius)}')

    # MANUAL CENTER Y
    def ManualCenterConfiguratorY(ValueY):
        config.crosshairY = config.capture_height // 2 + int(ValueY)
        config.center_y = config.height // 2 + int(ValueY)
        overlay.geometry(f'150x150+{str(config.center_x - config.radius)}+{str(config.center_y - config.radius)}')
        
    # CREATE SLIDER
    def CreateSlider(root, LabelText, fromV, toV, resolution, command, setValue):
        tk.Label(root, text=LabelText).pack()
        Slider = tk.Scale(root, from_=fromV, to=toV, resolution=resolution, orient=tk.HORIZONTAL, command = command)
        Slider.pack()
        Slider.set(setValue)

    #Manual Center Offset Sliders
    CreateSlider(root, "Offset CenterX Manually", -100, 100, 1, ManualCenterConfiguratorX, 0)
    CreateSlider(root, "Offset CenterY Manually", -100, 100, 1, ManualCenterConfiguratorY, 0)

    #Delay Slider
    CreateSlider(root, "Delay after shot", 0.003, 1.5, 0.001, DelayConfigurator, config.delay)
    
    #Trigger Slider
    CreateSlider(root, "Trigger offset Y", -10, 10, 1, OffsetYConfigurator, config.target_offset_y)

    #Quit Button
    QuitButton = tk.Button(root, text="Quit", command=quitProgram)
    QuitButton.pack()

    #Ingame Overlay
    overlay = tk.Toplevel(root)
    overlay.geometry(f'150x150+{str(config.center_x - config.radius)}+{str(config.center_y - config.radius)}')
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-transparentcolor', 'blue')
    
    # Canvas
    canvas = tk.Canvas(overlay, width=150, height=150, bg='blue', bd=0, highlightthickness=0)
    canvas.pack()

    config.canvas = canvas  # saving Canvas to config.canvas
    config.fovC = canvas.create_oval(0, 0, config.radius*2, config.radius*2, outline='purple')  # round in center

    overlay.mainloop()

# FIRE
def start_fire(config):
    global is_firing
    if is_firing:
        return
    is_firing = True

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    time.sleep(config.delay)  # задержка перед выстрелом

    is_firing = False



def detection_worker(q, cv_q):
    # FIRE CONSTANT
    global is_firing

    model = ultralytics.YOLO("best.pt")
    screenCapture = mss.mss()

    print("Detection Worker Yolo is Started")  # START LOG

    while True:
        GameFrame = np.array(screenCapture.grab(config.region))
        GameFrame = cv2.cvtColor(GameFrame, cv2.COLOR_BGRA2BGR)

        try:
            while not q.empty():
                update = q.get_nowait()
                if 'delay' in update:
                    config.delay = update['delay']
                if 'target_offset_y' in update:
                    config.target_offset_y = update['target_offset_y']
        except:
            pass

        # Переключения цели по Ctrl + T
        if win32api.GetAsyncKeyState(config.toggle_key['ctrl']) and win32api.GetAsyncKeyState(config.toggle_key['t']):
            if config.target_name == "CT":
                config.detect_classes = [2]  # T
                config.target_name = "T"
            else:
                config.detect_classes = [0]  # CT
                config.target_name = "CT"

            time.sleep(0.1)  # debounce

        results = model.predict(
            source=GameFrame,
            conf=0.4,
            classes=config.detect_classes,
            verbose=False,
            max_det=5,
            device='cuda:0',
            half=False)

        try:
            boxes_data = []
            if len(results) > 0 and len(results[0].boxes.xyxy) > 0:
                boxes = results[0].boxes
                boxes_data = []
                for box in boxes:
                    x1 = int(box.xyxy[0][0])
                    y1 = int(box.xyxy[0][1])
                    x2 = int(box.xyxy[0][2])
                    y2 = int(box.xyxy[0][3])
                    conf = float(box.conf[0])

                    boxes_data.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'conf': conf})

                    # --- Вот здесь проверяем, близка ли цель к центру ---
                    # Центр бокса
                    box_center_x = (x1 + x2) // 2
                    box_center_y = (y1 + y2) // 2

                    # Центр захвата (capture region)
                    center_x = config.crosshairX
                    center_y = config.crosshairY

                    # Допустимый порог близости (например, 15 пикселей)
                    threshold = 15

                    dist_x = abs(box_center_x - center_x)
                    dist_y = abs(box_center_y - center_y)

                    if dist_x < threshold and dist_y < threshold:
                        # Цель близко к центру — стреляем
                        if config.AimToggle:
                            threading.Thread(target=start_fire, args=(config,)).start()

            if not cv_q.full():
                cv_q.put({
                    'frame': GameFrame,
                    'boxes': boxes_data,
                    'target_name': config.target_name
                })

        except Exception as e:
            print("Detection error:", e)



def cv2_process(cv_q):
    fps = FPS()

    target_name = "" # дефолт выбор

    while True:
        if not cv_q.empty():
            try:
                data = cv_q.get_nowait() # получаем данные

                # распаковываем
                frame = data['frame']
                boxes = data.get('boxes', [])
                target_name = data.get('target_name', target_name)

                if boxes:
                    for box in boxes:
                        x1, y1, x2, y2 = box['x1'], box['y1'], box['x2'], box['y2']
                        conf = box['conf']

                        # Рамка цели
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)

                        # Уверенность в процентах
                    #    label = f"{conf * 100:.1f}%"
                    #    cv2.putText(frame, label, (x1, y1 - 10),
                    #                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # FPS COUNTER
                fps_font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText(frame, f"FPS: {fps():.2f}", (10, 20), fps_font,
                            0.50, (0, 255, 0), 1)
                
                cv2.putText(frame, f"Target: {target_name}", (10, 40), fps_font,
                            0.50, (0, 255, 255), 1)

                cv2.imshow("Game Frame", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            except Exception as e:
                print("Error in cv2_process:", e)

    cv2.destroyAllWindows()



# START
if __name__ == "__main__":

    print("Starting processes.")

    q = multiprocessing.JoinableQueue()
    cv_q = multiprocessing.JoinableQueue()

    # AI
    p1 = multiprocessing.Process(target=detection_worker, args=(q, cv_q), daemon = True)
    # CV2
    p2 = multiprocessing.Process(target=cv2_process, args=(cv_q,), daemon = True)
    # OVERLAY
    p3 = multiprocessing.Process(target=CreateOverlay, args=(q,), daemon = True)

    p1.start()
    p2.start()
    p3.start()

    while True:
        if not p3.is_alive(): #or not p2.is_alive():
            #cv2.destroyAllWindows()
            print("Shutting Down all Processes")
            sys.exit()


# CSGO-EGXxy-zmyWw-ph2Bs-5hzat-Z4OtQ