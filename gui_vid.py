import cv2
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QTimer

class VideoPlayer(QWidget):
    def __init__(self, video_path):
        super().__init__()
        self.cap = cv2.VideoCapture(video_path)
        self.initUI()

    def initUI(self):
        self.label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # タイマー設定
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrame)
        self.timer.start(1000. / 29.97)  # 30fps

    def nextFrame(self):
        ret, frame = self.cap.read()
        if ret:
            # OpenCVの画像データをPySide6で表示できるように変換
            frame = cv2.resize(frame, None, fx=0.2, fy=0.2)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, c = image.shape
            qimg = QImage(image.data, w, h, w*c, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            self.label.setPixmap(pixmap)

app = QApplication([])
player = VideoPlayer('data/00617.mp4')
player.show()
app.exec()