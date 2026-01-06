import subprocess
import os
from datetime import datetime


class FFmpegRecorder:
    def __init__(self):
        # Always save recordings here
        self.output_dir = os.path.join(
            os.path.expanduser("~"),
            "Documents",
            "ScreenRecordings"
        )

        os.makedirs(self.output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output = os.path.join(
            self.output_dir,
            f"recording_pyapp_{timestamp}.mp4"
        )

        self.process = None

    def start(self):
        cmd = [
            "ffmpeg",
            "-y",
            "-f", "gdigrab",
            "-framerate", "15",
            "-i", "desktop",
            "-f", "wasapi",
            "-i", "default",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-c:a", "aac",
            self.output
        ]

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
