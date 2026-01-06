import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import threading


class SystemAudioRecorder(threading.Thread):
    def __init__(self, filename="system.wav", samplerate=44100):
        super().__init__()
        self.filename = filename
        self.samplerate = samplerate
        self.frames = []
        self.recording = False
        self.started_ok = False   # 🔑 IMPORTANT FLAG

        self.device = 13  # Stereo Mix
        self.channels = 2

    def callback(self, indata, frames, time_info, status):
        if self.recording:
            self.frames.append(indata.copy())

    def run(self):
        try:
            self.recording = True
            with sd.InputStream(
                samplerate=self.samplerate,
                device=self.device,
                channels=self.channels,
                dtype="float32",
                blocksize=1024,
                callback=self.callback,
            ):
                self.started_ok = True
                while self.recording:
                    sd.sleep(100)
        except Exception as e:
            print("⚠ System audio failed:", e)
            self.started_ok = False

    def stop(self):
        self.recording = False

        if not self.started_ok:
            print("⚠ No system audio captured")
            return

        if not self.frames:
            print("⚠ System audio stream was silent")
            return

        audio = np.concatenate(self.frames, axis=0)
        write(self.filename, self.samplerate, audio)
