import json
import os

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLabel
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt


class VideoPlayer(QWidget):
    def __init__(self, video_path):
        super().__init__()

        self.setWindowTitle("Playback + Bookmarks")
        self.setMinimumSize(900, 500)

        # ---------- MEDIA PLAYER ----------
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)   # ✅ REQUIRED IN Qt6
        self.player.setAudioOutput(self.audio_output)

        self.video_widget = QVideoWidget()
        self.player.setVideoOutput(self.video_widget)

        # ---------- BOOKMARK LIST ----------
        self.bookmark_list = QListWidget()
        self.bookmark_list.setFixedWidth(260)
        self.bookmark_list.itemClicked.connect(self.jump_to_bookmark)

        # ---------- LAYOUT ----------
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Bookmarks"))
        right_layout.addWidget(self.bookmark_list)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.video_widget, stretch=3)
        main_layout.addLayout(right_layout, stretch=1)

        self.setLayout(main_layout)

        # ---------- FILE PATHS ----------
        self.video_path = video_path
        self.bookmark_path = os.path.splitext(video_path)[0] + "_bookmarks.json"

        # ---------- LOAD ----------
        self.load_video()
        self.load_bookmarks()

    # ---------- LOAD VIDEO ----------
    def load_video(self):
        self.player.setSource(QUrl.fromLocalFile(self.video_path))
        self.audio_output.setVolume(1.0)
        self.player.play()   # ✅ NOW IT WILL ACTUALLY PLAY

    # ---------- LOAD BOOKMARKS ----------
    def load_bookmarks(self):
        if not os.path.exists(self.bookmark_path):
            return

        with open(self.bookmark_path, "r") as f:
            bookmarks = json.load(f)

        for bm in bookmarks:
            sec = int(bm["time_seconds"])
            mm = sec // 60
            ss = sec % 60

            text = bm.get("note", "Bookmark")
            item = QListWidgetItem(f"{mm:02d}:{ss:02d}  {text}")
            item.setData(Qt.UserRole, sec)

            self.bookmark_list.addItem(item)

    # ---------- SEEK ----------
    def jump_to_bookmark(self, item):
        seconds = item.data(Qt.UserRole)
        self.player.setPosition(seconds * 1000)
