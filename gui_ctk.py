import customtkinter as ctk
import CTkMenuBar
import CTkMessagebox
import darkdetect
import cv2
from PIL import Image, ImageTk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Windowsのテーマ色設定。"Light" or "Dark"
        self.color_mode = darkdetect.theme()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        #動画の取得
        self.video_path = "data/00617.mp4"
        self.cap = cv2.VideoCapture(self.video_path)

        """
        try:
            ctk.set_default_color_theme("theme.json")
        except FileNotFoundError:
            ctk.set_default_color_theme("blue")
        """

        self.fonts = ("游ゴシック", 15)
        self.title("抑留者データベース-安田")
        self.geometry("600x600")
        #self.iconbitmap("icon.ico")

        self.setup()

    def button_function(self):
        print("button pressed")

    def setup(self):
        self.toplevel_window = None
        button = ctk.CTkButton(self, text="CTkButton", command = self.button_function)
        button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.canvas = ctk.CTkCanvas(self, width=640, height=480)
        self.canvas.pack()

    def update_frame(self):
        ret, self.frame = self.cap.read()
        if ret:
            rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            pil = Image.fromarray(rgb)
            x = self.video_button.winfo_width()/pil.width
            y = self.video_button.winfo_height()/pil.height
            ratio = x if x<y else y #三項演算子 xとyを比較して小さい方を代入
            pil = pil.resize((int(ratio*pil.width),int(ratio*pil.height)))
            image = ImageTk.PhotoImage(pil)
            self.video_button.config(image=image)
            self.video_button.image = image
        app.after(10, self.update_frame)

    def video_frame_timer(self):
        while self.playing:
            self.next_frame()

if __name__ == "__main__":
    app = App()
    app.mainloop()