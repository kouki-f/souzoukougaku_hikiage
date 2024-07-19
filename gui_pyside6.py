from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from voice_stt.run import SpeechRecognizer as sp
from faq_ai.faq_ai_main import search_ans


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.speech = sp()
        self.setWindowTitle("抑留者データベース-安田")
        windowWidth = 500   # ウィンドウの横幅
        windowHeight = 200  # ウィンドウの高さ
        self.resize(windowWidth, windowHeight)

        self.SetLabel1()
        self.SetButton1()
        self.SetButton2()

        layout = QVBoxLayout(self)
        layout.addWidget(self.label1)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)

    def SetLabel1(self):
        self.label1 = QLabel('「音声認識」を押してください', self)

    def SetButton1(self):
        self.button1 = QPushButton('音声認識', self)
        self.button1.clicked.connect(self.import_speech)

    def SetButton2(self):
        self.button2 = QPushButton('検索', self)
        self.button2.clicked.connect(self.on_button2_change)

    def on_label1_change(self, text):
        self.label1.setText(text)

    def on_button2_change(self, text):
        self.button1.setText(text)

    def import_speech(self, sp):
        #マイクで受け取った音声を認識してテキストに出力
        self.label1.setText('認識中…')
        QApplication.processEvents()
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
        return speech

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()