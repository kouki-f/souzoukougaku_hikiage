from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtGui import QPixmap, Qt, QImage
from PySide6.QtCore import QTimer
from voice_stt.run import SpeechRecognizer as sp
from faq_ai.faq_ai_main import search_ans
from faq_ai.video import PlayVideoWithSound
from ffpyplayer.player import MediaPlayer
from pygame import mixer as pym
import time
import cv2
#pip install pygame==2.4.0

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.speech = sp()
        self.player = ''
        self.inputted_text = "None"
        self.setWindowTitle("抑留者データベース-安田")


        #ウィンドウサイズの調整
        self.windowWidth = 600   # ウィンドウの横幅
        self.windowHeight = 600  # ウィンドウの高さ
        self.setFixedSize(self.windowWidth, self.windowHeight)

        #動画の取得
        self.video_path = "data/00617.mp4"
        self.cap = cv2.VideoCapture(self.video_path)

        #ウィジェットの呼び出し
        self.SetLabel1()
        self.SetLabel2()
        self.SetLabel3()
        self.SetButton1()
        self.SetButton2()

        #ウィジェットの配置S
        layout = QVBoxLayout(self)
        hlayout = QHBoxLayout(self)
        layout.addWidget(self.label1)
        hlayout.addWidget(self.button1)
        hlayout.addWidget(self.button2)
        layout.insertLayout(1, hlayout)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)

    """
    def get_audio_player(self, video_path):
        return MediaPlayer(video_path)
    """

        #ウィジェットの設定(SetLabel1 ~ SetuButton2)

    def SetLabel1(self):
        self.label1 = QLabel('「音声認識」を押してください', self)
        self.label1.setAlignment(Qt.AlignCenter)

    def SetLabel2(self):
        self.label2 = QLabel('ここに返答が表示されます。', self)
        self.label2.setWordWrap(True)
        self.label2.setMaximumWidth(self.windowWidth)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setStyleSheet("QLabel {font-size: 20px;}")

    def SetLabel3(self):
        self.label3 = QLabel(self)
        self.image = QPixmap(r"data/play_movie.png")
        self.label3.setPixmap(self.image)

    def SetButton1(self):
        self.button1 = QPushButton('音声認識', self)
        self.button1.clicked.connect(self.import_speech)

    def SetButton2(self):
        self.button2 = QPushButton('検索', self)
        self.button2.clicked.connect(self.search_database)

        #音声認識の関数
    def import_speech(self, sp):
        self.button1.setText('話してください…')
        self.label1.setText('')
        QApplication.processEvents()

        #マイクで受け取った音声を認識してテキストに出力
        audio = self.speech.grab_audio()
        speech = self.speech.recognize_audio(audio)
        self.speech.speech.append(speech)

        if speech == 1:
            speech = f"認識できませんでした"
        if speech == 2:
            speech = f"音声認識のリクエストが失敗しました:"

        self.button1.setText('やり直す')
        self.label1.setText(speech)
        print(speech)
        self.inputted_text = speech

        #データベースを参照
    def search_database(self):
        if self.inputted_text == "None":
            self.label1.setText('質問を入力してください')
            QApplication.processEvents()
            return

        self.button2.setText('検索中…')
        QApplication.processEvents()

        [similarity, ans, self.video_time] = search_ans(self.inputted_text)
        if similarity > 0.9:
            self.label2.setText(ans)
            print(self.inputted_text, self.video_time)
            fps = self.cap.get(cv2.CAP_PROP_FPS)

            #動画の再生秒数にシーク
            self.start_frame = int(self.video_time[0] * fps)
            self.end_frame = int(self.video_time[1] * fps)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame)

            #動画,音声を再生
            self.video_seconds = time.time() + 1.15
            self.play_sound(self.video_time[0])
            self.play_video(fps)

            """
            #音声の取得、再生秒数にシーク
            self.player = self.get_audio_player(self.video_path)
            self.player.seek(video_time[0], relative=False)
            #player.seekでクラッシュする
            """

        else:
            self.label2.setText("検索結果が見つかりませんでした。")
        self.button2.setText('検索')

        #動画を再生
    def play_video(self, fps):
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrame)
        self.timer.start(1000. / (fps*1.046))

        #音声を再生
    def play_sound(self, start_time):
        pym.init()
        pym.music.load("data/00617.mp3")
        pym.music.play(loops=-1, start=start_time)

    def nextFrame(self):
        ret, frame = self.cap.read()
        if ret:
            # OpenCVの画像データをPySide6で表示できるように変換
            frame = cv2.resize(frame, None, fx=0.3, fy=0.3)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, c = image.shape
            qimg = QImage(image.data, w, h, w*c, QImage.Format_RGB888)

            #動画を再生
            pixmap = QPixmap.fromImage(qimg)
            self.label3.setPixmap(pixmap)

        #指定した秒数を超えると再生を停止
        if time.time() - self.video_seconds >= self.video_time[1] - self.video_time[0]:
            pym.music.stop()
            self.timer.stop()

            #静止画像に置き換え
            self.label3.setPixmap(self.image)
            QApplication.processEvents()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()