# FPS 100

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
import sys, os

# CONFIG
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

        self.Running = multiprocessing.Value('b', True)
        self.AimToggle = multiprocessing.Value('b', True)
        self.delay = multiprocessing.Value('d', 0) # DELAY
        self.radius = 10

        self.target_offset_y = multiprocessing.Value('i', 0)
        self.aim_threshold_x = multiprocessing.Value('d', 0.2)
        self.aim_threshold_y = multiprocessing.Value('d', 0.3)

config = Config()

# FIRE
def fire(config):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(config.delay.value)

# AI
def detection_worker(frame_queue, result_queue, config):
    model = ultralytics.YOLO("yolov8n.pt")

    while config.Running.value:
        
        if not frame_queue.empty():
            frame = frame_queue.get()
            results = model.predict(source=frame, conf=0.35, classes=[0], verbose=False, max_det=10)
            boxes = results[0].boxes.xyxy
            result_queue.put((frame, boxes.tolist() if len(boxes) > 0 else []))
        time.sleep(0.001)

# MSS / ACTIONS
def gui_worker(frame_queue, result_queue, config):
    screenCapture = mss.mss()
    is_firing = False
    prev_time = time.time()

    while config.Running.value:
        if win32api.GetAsyncKeyState(0x05) & 1:
            config.AimToggle.value = not config.AimToggle.value
            winsound.Beep(1000 if config.AimToggle.value else 500, 50)
            time.sleep(0.1)

        if not config.AimToggle.value:
            continue

        GameFrame = np.array(screenCapture.grab(config.region))
        GameFrame = cv2.cvtColor(GameFrame, cv2.COLOR_BGRA2BGR)

        if frame_queue.empty():
            frame_queue.put(GameFrame.copy())

        if not result_queue.empty():
            GameFrame, boxes = result_queue.get()
            if boxes:
                x1, y1, x2, y2 = boxes[0]
                displacementX = x2 - x1
                displacementY = y2 - y1
                target_x = int(x1 + displacementX / 2)
                target_y = int(y1 + displacementY / 3) + config.target_offset_y.value

                moveX = target_x - config.crosshairX
                moveY = target_y - config.crosshairY

                aim_threshold_x = displacementX * config.aim_threshold_x.value
                aim_threshold_y = displacementY * config.aim_threshold_y.value

                cv2.rectangle(GameFrame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 1)
                cv2.circle(GameFrame, (target_x, target_y), 3, (255, 0, 0), -1)

                if abs(moveX) <= aim_threshold_x and abs(moveY) <= aim_threshold_y:
                    if not is_firing:
                        is_firing = True
                        multiprocessing.Process(target=fire, args=(config,), daemon=True).start()
                        time.sleep(config.delay.value)
                        is_firing = False

        fps = 1 / (time.time() - prev_time)
        prev_time = time.time()
        cv2.putText(GameFrame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 255, 0), 2)

        cv2.imshow("Game Frame", GameFrame)
        del GameFrame

        if cv2.waitKey(1) & 0xFF == ord('q'):
            config.Running.value = False
            break

    cv2.destroyAllWindows()


# START
if __name__ == '__main__':

    frame_queue = multiprocessing.Queue(maxsize=2)
    result_queue = multiprocessing.Queue(maxsize=2)

    gui = multiprocessing.Process(target=gui_worker, args=(frame_queue, result_queue, config))

    detector = multiprocessing.Process(target=detection_worker, args=(frame_queue, result_queue, config))

    detector.start()
    gui.start()

    while True:
        if not detector.is_alive():
            #cv2.destroyAllWindows()
            print("Shutting Down all Processes")
            sys.exit()