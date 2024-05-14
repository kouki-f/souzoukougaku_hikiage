#参考サイトより直接コピペしたプログラム
#参考のために残してる
import os
import speech_recognition as sr
from datetime import datetime

class SpeechRecognizer():
    def __init__(self):
        """出力フォルダの作成と保存先の設定，マイク入力と認識エンジンの初期化
        """
        os.makedirs("./out", exist_ok=True)
        self.path = f"./out/asr.txt"

        self.rec = sr.Recognizer()
        self.mic = sr.Microphone()
        self.speech = []
        return

    def grab_audio(self) -> sr.AudioData:
        """マイクで音声を受け取る関数
        Returns:
            speech_recognition.AudioData: 音声認識エンジンで受け取った音声データ
        """
        print("何か話してください...")
        with self.mic as source:
            self.rec.adjust_for_ambient_noise(source)
            audio = self.rec.listen(source)
        return audio

    def recognize_audio(self, audio: sr.AudioData) -> str:
        print ("認識中...")
        try:
            speech = self.rec.recognize_google(audio, language='ja-JP')
        except sr.UnknownValueError:
            speech = f"#認識できませんでした"
            print(speech)
        except sr.RequestError as e:
            speech = f"#音声認識のリクエストが失敗しました:{e}"
            print(speech)
        return speech

    def run(self):
        """マイクで受け取った音声を認識してテキストに出力
        """
        while True:
            audio = self.grab_audio()
            speech = self.recognize_audio(audio)

            if speech == "終わり":
                print("音声認識終了")
                break
            else:
                self.speech.append(speech)
                print(speech)

        with open(self.path, mode='w', encoding="utf-8") as out:
            out.write(datetime.now().strftime('%Y%m%d_%H:%M:%S') + "\n\n")
            out.write("\n".join(self.speech) + "\n")

    def run_once(self):
        """マイクで受け取った音声を認識してテキストに出力
        """
        audio = self.grab_audio()
        speech = self.recognize_audio(audio)
        self.speech.append(speech)

        with open(self.path, mode='w', encoding="utf-8") as out:
            out.write(datetime.now().strftime('%Y%m%d_%H:%M:%S') + "\n\n")
            out.write("\n".join(self.speech) + "\n")
        
        return speech

if __name__ == '__main__':
    my = SpeechRecognizer()
    my.run_once()
