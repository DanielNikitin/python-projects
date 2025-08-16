from multiprocessing import Process, Manager
import win32api
import winsound

import tkinter as tk
import numpy as np
import time

import ultralytics
import cv2
import mss

# GUI overlay function (moved outside to run as a process)
def CreateOverlay(shared):
    root = tk.Tk()
    root.title("Menu Window 2")
    root.geometry('250x450')

    def quitProgram():
        shared["AimToggle"] = False
        shared["Running"] = False
        root.quit()

    def DelayConfigurator(value):
        shared["delay"] = float(value)

    def ManualCenterConfiguratorX(val):
        shared["offsetX"] = int(val)

    def ManualCenterConfiguratorY(val):
        shared["offsetY"] = int(val)

    def Update_Trigger_Radius(val):
        shared["trigger_radius"] = int(val)

    def CreateSlider(parent, text, from_, to, res, command, default):
        tk.Label(parent, text=text).pack()
        s = tk.Scale(parent, from_=from_, to=to, resolution=res, orient=tk.HORIZONTAL, command=command)
        s.pack()
        s.set(default)

    CreateSlider(root, "Offset Center X", -100, 100, 1, ManualCenterConfiguratorX, 0)
    CreateSlider(root, "Offset Center Y", -100, 100, 1, ManualCenterConfiguratorY, 0)
    CreateSlider(root, "Delay after shot", 0.003, 1.5, 0.001, DelayConfigurator, shared["delay"])
    CreateSlider(root, "Trigger Radius", -10, 10, 1, Update_Trigger_Radius, 0)

    tk.Button(root, text="Quit", command=quitProgram).pack()

    root.mainloop()

# MAIN AI + OpenCV
def run_ai(shared):

    # YOLO
    model = ultralytics.YOLO("yolov8n.pt")
    screen = mss.mss()

    # FPS
    prev_time = time.time()

    while shared["Running"]:
        if win32api.GetAsyncKeyState(0x05) & 1:
            shared["AimToggle"] = not shared["AimToggle"]
            winsound.Beep(1000 if shared["AimToggle"] else 500, 50)
            time.sleep(0.1)

        if not shared["AimToggle"]:
            continue

        # Adjust capture area with center offsets
        center_x = 1920 // 2 + shared["offsetX"]
        center_y = 1080 // 2 + shared["offsetY"]

        region = {
            "top": center_y - 70,
            "left": center_x - 70,
            "width": 140,
            "height": 140 + 100
        }

        frame = np.array(screen.grab(region))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        results = model.predict(source=frame, conf=0.45, classes=[0], verbose=False, max_det=10)

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 1)
        
        # FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 1)


        cv2.imshow("Frame", frame)
        del frame

        if cv2.waitKey(1) & 0xFF == ord('q'):
            shared["Running"] = False
            break

    cv2.destroyAllWindows()

# MAIN ENTRY
if __name__ == "__main__":
    with Manager() as manager:
        shared = manager.dict()

        # HERE IS CONFIG VALUES
        shared["Running"] = True
        shared["AimToggle"] = True
        shared["delay"] = 0.60
        shared["offsetX"] = 0
        shared["offsetY"] = 0
        shared["trigger_radius"] = 0

        gui_process = Process(target=CreateOverlay, args=(shared,))
        gui_process.start()

        run_ai(shared)  # main process runs AI

        gui_process.join()
