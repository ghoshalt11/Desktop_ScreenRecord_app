import cv2
import numpy as np
import mss
import time
import threading


class ScreenRecorder(threading.Thread):
    def __init__(self, output_file="screen_recording.mp4", fps=15):
        super().__init__()
        self.output_file = output_file
        self.fps = fps
        self.running = False

    def run(self):
        self.running = True

        with mss.mss() as sct:
            monitor = sct.monitors[1]
            width = monitor["width"]
            height = monitor["height"]

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(self.output_file, fourcc, self.fps, (width, height))

            while self.running:
                start_time = time.time()

                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                out.write(frame)

                elapsed = time.time() - start_time
                time.sleep(max(0, (1 / self.fps) - elapsed))

            out.release()

    def stop(self):
        self.running = False
