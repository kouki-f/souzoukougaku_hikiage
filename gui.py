import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
from voice_stt.run import SpeechRecognizer
from faq_ai.faq_ai_main import search_ans

class gui():
    def __init__(self):
        self.window = tk.Tk()
        self.speech = SpeechRecognizer()
        self.window.title("引き揚げ証言データベース")
        self.window.geometry("1400x1300")
        # Create a canvas that can fit the video source size
        # self.canvas = tk.Canvas(self.window, width=1080, height=1440)
        # self.canvas.pack()
        self.layer()
        # Update the image in the canvas
        #self.update()
        self.window.mainloop()
        

    def import_speech(self, sp):
        #マイクで受け取った音声を認識してテキストに出力
        while True:
            audio = sp.grab_audio()
            speech = sp.recognize_audio(audio)
            sp.speech.append(speech)

            if speech == 1:
                speech = f"認識できませんでした"
            elif speech == 2:
                speech = f"音声認識のリクエストが失敗しました:"
            else:
                break

            print(speech)
        return speech
    
    def layer(self):
        def on_button_click():
            self.inputted_text = self.import_speech(self.speech)
            update_label(self.inputted_text)
            
        def update_label(text):
            label2.config(text=text)

        def update_label3(text):
            label3.config(text=text)

        def on_button2_click():
            [similarity, ans, video_time] = search_ans(self.inputted_text)
            if similarity > 0.9:
                update_label3(ans)
                print(self.inputted_text, video_time)
            else:
                update_label3("検索結果が見つかりませんでした。")

        def on_button3_click():
            self.inputted_text = self.import_speech(self.speech)
            update_label(self.inputted_text)

        label1 = tk.Label(self.window, text="安田さんの証言検索ソフト", font=("Arial", 20))
        label1.grid(row=0, column=0, columnspan=2)  # ラベルをウィンドウに配置
        button1 = tk.Button(self.window, text="クリックしてスタート", command=on_button_click)
        button1.grid(row=1, column=0, columnspan=2)
        label2 = tk.Label(self.window, text="")
        label2.grid(row=2, column=0, columnspan=2)
        button2 = tk.Button(self.window, text="検索", command=on_button2_click)
        button3 = tk.Button(self.window, text="やり直す", command=on_button3_click)
        button2.grid(row=3, column=0)
        button3.grid(row=3, column=1)
        label3 = tk.Label(self.window, text="")
        label3.grid(row=4, column=0)

gui = gui()
