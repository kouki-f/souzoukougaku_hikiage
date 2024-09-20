import cv2
from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import messagebox, Canvas
import threading as th

lock = th.Lock()

class VideoPlayer(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, width=1000, height=500)
        master.minsize(width=1000, height=500)
        self.configure(fg_color="#000000")
        self.pack(expand=True, fill=ctk.BOTH)
        self.video = None
        self.playing = False
        self.video_thread = None
        self.create_widgets()

        # 起動時に自動再生する
        self.push_play_button()

    def create_widgets(self):
        # キャンバスを追加して動画フレームを描画
        self.canvas = Canvas(self, bg="#000000", width=800, height=400)
        self.canvas.pack(expand=True, fill=ctk.BOTH)

        # ボタンを追加して動画再生・停止を制御
        self.video_button = ctk.CTkButton(
            self,
            width=100,
            height=25,
            fg_color="#DDDDDD",
            text="Play Video",
            command=self.push_play_button,
        )
        self.video_button.pack(side=ctk.BOTTOM, pady=10)

    def get_video(self, path):
        self.video = cv2.VideoCapture(path)

    def push_play_button(self):
        if self.video is None:
            messagebox.showerror('エラー', '動画データがありません')
            return

        self.playing = not self.playing
        if self.playing:
            self.video_thread = th.Thread(target=self.video_frame_timer)
            self.video_thread.setDaemon(True)
            self.video_thread.start()
            self.video_button.configure(text="Stop Video")
        else:
            self.video_thread = None
            self.video_button.configure(text="Play Video")

    def next_frame(self):
        global lock
        lock.acquire()
        ret, self.frame = self.video.read()
        if not ret:
            messagebox.showerror("エラー", "次のフレームがないので停止します")
            self.playing = False
            self.video_button.configure(text="Play Video")
        else:
            # BGRからRGBに変換し、PILイメージを作成
            rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb)

            # Canvasのサイズに合わせて画像サイズを調整
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            x_ratio = canvas_width / pil_image.width
            y_ratio = canvas_height / pil_image.height
            ratio = min(x_ratio, y_ratio)
            resized_image = pil_image.resize((int(pil_image.width * ratio), int(pil_image.height * ratio)))

            # Tkinter用の画像オブジェクトに変換
            tk_image = ImageTk.PhotoImage(resized_image)

            # Canvasに描画
            self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=tk_image, anchor="center")
            self.canvas.image = tk_image  # 画像が消えないように参照を保持

        lock.release()

    def video_frame_timer(self):
        while self.playing:
            self.next_frame()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # テーマの設定: "dark" または "light"
    ctk.set_default_color_theme("blue")  # カラーテーマの設定

    root = ctk.CTk()
    path = "data/00617.mp4"  # 再生したい動画ファイルのパスを設定
    app = VideoPlayer(master=root)
    app.get_video(path)
    root.mainloop()
