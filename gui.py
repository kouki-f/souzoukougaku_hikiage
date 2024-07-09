import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

class gui():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("引き揚げ証言データベース")
        self.window.geometry("1400x1300")
        # Create a canvas that can fit the video source size
        # self.canvas = tk.Canvas(self.window, width=1080, height=1440)
        # self.canvas.pack()
        self.layer()
        # Update the image in the canvas
        #self.update()
        self.window.mainloop()
    def layer(self):
        def on_button_click():
            print("a")
        label = tk.Label(self.window, text="Hello, tkinter!", font=("Arial", 20))
        label.pack(pady=20)  # ラベルをウィンドウに配置
        button = tk.Button(self.window, text="クリックしてスタート", command=on_button_click)
        button.pack(pady=20)

gui = gui()
