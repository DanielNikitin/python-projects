import win32api
import win32con
import win32gui
import tkinter as tk
import numpy as np
import ultralytics
import threading
import math
import time 
import cv2
import mss
import random
import winsound


class Config:
    def __init__(self):
        
        
        self.width = 1920  # Main window Size not Game
        self.height = 1080
        
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        
        # small window
        self.capture_width = 140  # Area for detecting X
        self.capture_height = 140  # Area for detecting Y

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
        self.delay = 0.60
        self.radius = 10

        self.target_dot = None  # точка в дебаге

config = Config()


def CreateOverlay():

    root = tk.Tk()
    root.title("Menu Window")
    root.geometry('250x650')  # Size
    tk.Label(root, text="AI menu title", font=("Helvetica", 14)).pack()
    
    def quitProgram():
        
        config.AimToggle = False
        config.Running = False
        root.quit()

    # DELAY
    def DelayConfigurator(Delay):
        config.delay = float(Delay)

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

# CROSSHAIR COLOR SWITCH MODE
def UpdateCrosshairColor():
    while config.Running:
        if hasattr(config, 'canvas') and hasattr(config, 'fovC'):
            color = 'hotpink' if config.AimToggle else 'red'
            try:
                config.canvas.itemconfig(config.fovC, outline=color)
            except tk.TclError:
                break  # close and delete
        time.sleep(1)  # обновляем цвет каждые 50 мс

def UpdateTargetDot(x, y):
    if hasattr(config, 'canvas') and hasattr(config, 'target_dot'):
        try:
            config.canvas.coords(config.target_dot, x-3, y-3, x+3, y+3)
        except tk.TclError:
            pass
    
def main():

    # FPS COUNTER
    prev_time = time.time()
    fps = 0
    
    # MAIN MOUSE
    x1 = y1 = x2 = y2 = 0
    moveX = moveY = 0
    displacementX = displacementY = -1
    noDetectionIteration = 1
    
    # AI
    #model = ultralytics.YOLO("Fortnite by hogthewog.onnx", task = 'detect')
    model = ultralytics.YOLO("yolov8n.pt")  # best.pt
    screenCapture = mss.mss()
    
    overlayThread = threading.Thread(target=CreateOverlay)
    overlayThread.start()

    # Запускаем поток для обновления цвета прицела
    threading.Thread(target=UpdateCrosshairColor, daemon=True).start()
    
    while config.Running:
        #time.sleep(0.001)

        # ACTIVATE / DEACTIVATE BY MOUSE BUTTON
        if win32api.GetAsyncKeyState(0x05) & 1:
            config.AimToggle = not config.AimToggle
            winsound.Beep(1000 if config.AimToggle else 500, 50)
            time.sleep(0.1)

        if not config.AimToggle:
            continue
        
        GameFrame = np.array(screenCapture.grab(config.region))
        GameFrame = cv2.cvtColor(GameFrame, cv2.COLOR_BGRA2BGR)

        results = model.predict(source = GameFrame, conf = 0.45, classes=[0], verbose=False, max_det = 10)
        # in best.pt {0: 'CT', 1: 'CT_HEAD', 2: 'T', 3: 'T_HEAD'}   
        boxes = results[0].boxes.xyxy

        if len(boxes) > 0:
            x1, y1, x2, y2 = boxes[0].tolist()

            displacementX = x2-x1
            displacementY = y2-y1
            
            moveX = int((displacementX // 2 + x1 - config.crosshairX))
            moveY = int((displacementY //2 + y1 - config.crosshairY))

            noDetectionIteration = 0

            # Рисуем прямоугольник цели при обнаружении ИИ
            cv2.rectangle(GameFrame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 1)

            # Отладочная точка прицеливания
            cv2.circle(GameFrame, (moveX, moveY), 3, (255, 0, 0), -1)
            UpdateTargetDot(config.crosshairX + moveX, config.crosshairY + moveY)  # обновление позиции из GUI

        else:
            # Сброс при отсутствии цели
            x1 = y1 = x2 = y2 = 0
            displacementX = displacementY = -1
            moveX = moveY = 9999
            noDetectionIteration += 1
            UpdateTargetDot(-10, -10)

        # Условие для выстрела
        if (
            abs(moveX) <= displacementX//2 and
            abs(moveY) <= displacementY//2 and
            noDetectionIteration <= 1
        ):
            noDetectionIteration += 1

            # Выстрел
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.001)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(config.delay)

        # FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        cv2.putText(GameFrame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.50, (0, 255, 0), 2)
        
        # DEBUGGING WINDOW
        cv2.imshow("Game Frame", GameFrame)
        del GameFrame
        
        # Quit?
        if cv2.waitKey(1) & 0xFF == ord('q'):
            config.Running = False
            break
            
    overlayThread.join()
    cv2.destroyAllWindows()
                 
if __name__ == "__main__":
    main()







    #FOR DEBUGGING             
        #cv2.rectangle(GameFrame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
        #cv2.imshow("Game Frame", GameFrame)        
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #config.Running = False
            #break       
    #cv2.destroyAllWindows()
