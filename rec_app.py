import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

from screen_recorder import ScreenRecorder
from system_audio_recorder import SystemAudioRecorder


class RecorderUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Screen Recorder")
        self.setFixedSize(300, 180)

        self.video = None
        self.audio = None

        self.recorder = None

        self.status_label = QLabel("Status: Idle")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.start_btn = QPushButton("▶ Start Recording")
        self.stop_btn = QPushButton("■ Stop Recording")
        self.stop_btn.setEnabled(False)

        self.start_btn.clicked.connect(self.start_recording)
        self.stop_btn.clicked.connect(self.stop_recording)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)

        self.setLayout(layout)

    def start_recording(self):
        self.recorder = ScreenRecorder()
        self.audio = SystemAudioRecorder()
        self.recorder.start()

        self.status_label.setText("Status: Recording...")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop_recording(self):
        if self.recorder:
            self.recorder.stop()
            self.recorder.join()

        if self.audio:
            self.audio.stop()
            if self.audio.is_alive():
                self.audio.join()
        
        if self.video:
            self.video.stop()
            if self.video.is_alive():
                self.video.join()
    

        self.status_label.setText("Status: Saved")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecorderUI()
    window.show()
    sys.exit(app.exec())
