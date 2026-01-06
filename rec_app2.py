import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QFileDialog
)
from PySide6.QtCore import Qt

from screen_recorder import ScreenRecorder
from system_audio_recorder import SystemAudioRecorder
from bookmark_manager import BookmarkManager
from video_player import VideoPlayer


class RecorderUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Screen Recorder")
        self.setFixedSize(360, 500)

        # Recorder objects
        self.recorder = None
        self.audio = None
        self.bookmarks = None

        # -------- UI ELEMENTS --------

        self.status_label = QLabel("Status: Idle")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.start_btn = QPushButton("▶ Start Recording")
        self.stop_btn = QPushButton("■ Stop Recording")
        self.bookmark_btn = QPushButton("🔖 Add Bookmark")
        self.open_btn = QPushButton("📂 Open Recording")

        self.stop_btn.setEnabled(False)
        self.bookmark_btn.setEnabled(False)

        self.start_btn.clicked.connect(self.start_recording)
        self.stop_btn.clicked.connect(self.stop_recording)
        self.bookmark_btn.clicked.connect(self.add_bookmark)
        self.open_btn.clicked.connect(self.open_recording)

        # Bookmark list panel
        self.bookmark_list = QListWidget()

        # -------- LAYOUT --------

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.bookmark_btn)
        layout.addWidget(QLabel("Bookmarks"))
        layout.addWidget(self.bookmark_list)
        layout.addWidget(self.open_btn)

        self.setLayout(layout)

    # -------- RECORDING --------

    def start_recording(self):
        self.recorder = ScreenRecorder()
        self.audio = SystemAudioRecorder()

        self.recorder.start()
        self.audio.start()

        # Initialize bookmarks
        self.bookmarks = BookmarkManager("recording")
        self.bookmark_list.clear()

        self.status_label.setText("Status: Recording...")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.bookmark_btn.setEnabled(True)

    def stop_recording(self):
        if self.recorder:
            self.recorder.stop()
            self.recorder.join()

        if self.audio:
            self.audio.stop()
            if self.audio.is_alive():
                self.audio.join()

        if self.bookmarks:
            self.bookmarks.save()

        self.status_label.setText("Status: Saved")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.bookmark_btn.setEnabled(False)

    # -------- BOOKMARKING --------

    def add_bookmark(self):
        if not self.bookmarks:
            return

        self.bookmarks.add("Bookmark")

        last = self.bookmarks.bookmarks[-1]
        sec = int(last["time_seconds"])
        mm = sec // 60
        ss = sec % 60

        label = f"{mm:02d}:{ss:02d}  Bookmark"
        self.bookmark_list.addItem(QListWidgetItem(label))

        self.status_label.setText("Bookmark added ✔")

    # -------- PLAYBACK --------

    def open_recording(self):
        video_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Recording",
            "",
            "Video Files (*.mp4)"
        )

        if video_path:
            self.player_window = VideoPlayer(video_path)
            self.player_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecorderUI()
    window.show()
    sys.exit(app.exec())
