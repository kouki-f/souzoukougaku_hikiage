from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtGui import QPixmap, Qt
from voice_stt.run import SpeechRecognizer as sp
from faq_ai.faq_ai_main import search_ans
from faq_ai.video import PlayVideoWithSound

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.speech = sp()
        self.inputted_text = "None"
        self.setWindowTitle("抑留者データベース-安田")
        self.windowWidth = 600   # ウィンドウの横幅
        self.windowHeight = 500  # ウィンドウの高さ
        self.setFixedSize(self.windowWidth, self.windowHeight)

        #ウィジェットの呼び出し
        self.SetLabel1()
        self.SetLabel2()
        self.SetLabel3()
        self.SetButton1()
        self.SetButton2()

        #ウィジェットの配置
        layout = QVBoxLayout(self)
        hlayout = QHBoxLayout(self)
        layout.addWidget(self.label1)
        hlayout.addWidget(self.button1)
        hlayout.addWidget(self.button2)
        layout.insertLayout(1, hlayout)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)

    def SetLabel1(self):
        self.label1 = QLabel('「音声認識」を押してください', self)
        self.label1.setAlignment(Qt.AlignCenter)

    def SetLabel2(self):
        self.label2 = QLabel('', self)
        self.label2.setWordWrap(True)
        self.label2.setMaximumWidth(self.windowWidth)
        self.label2.setAlignment(Qt.AlignCenter)

    def SetLabel3(self):
        self.label3 = QLabel(self)
        self.label3.setAlignment(Qt.AlignCenter)
        image = QPixmap(r"image.png")

        width = image.size().width() / 2
        height = image.size().height() / 2
        image = image.scaled(width, height)

        self.label3.setPixmap(image)

    def SetButton1(self):
        self.button1 = QPushButton('音声認識', self)
        self.button1.clicked.connect(self.import_speech)

    def SetButton2(self):
        self.button2 = QPushButton('検索', self)
        self.button2.clicked.connect(self.search_database)

    def import_speech(self, sp):
        self.button1.setText('話してください…')
        self.label1.setText('')
        QApplication.processEvents()

        #マイクで受け取った音声を認識してテキストに出力
        while True:
            audio = self.speech.grab_audio()
            speech = self.speech.recognize_audio(audio)
            self.speech.speech.append(speech)

            if speech == 1:
                speech = f"認識できませんでした"
            elif speech == 2:
                speech = f"音声認識のリクエストが失敗しました:"
            else:
                break

        self.button1.setText('やり直す')
        self.label1.setText(speech)
        print(speech)
        self.inputted_text = speech

    def search_database(self):
        if self.inputted_text == "None":
            self.label1.setText('質問を入力してください')
            QApplication.processEvents()
            return

        self.button2.setText('検索中…')
        QApplication.processEvents()

        [similarity, ans, video_time] = search_ans(self.inputted_text)
        if similarity > 0.9:
            self.label2.setText(ans)
            print(self.inputted_text, video_time)
            PlayVideoWithSound("data/00617.mp4", video_time[0], video_time[1], ans)
        else:
            self.label2.setText("検索結果が見つかりませんでした。")

        self.button2.setText('検索')

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()