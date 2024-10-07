from voice_stt.run import SpeechRecognizer as sp
from faq_ai.faq_ai_main import search_ans
from pygame import mixer as pym
import faq_ai.excel_io as excel_io
import cv2
import flet as ft
import time
from PIL import Image
import io
import base64

class GUI():
    def __init__(self):
        self.speech = sp()
        self.player = ''
        self.play_run = 0
        self.inputted_text = ""

        #cv2で動画を読み込む
        self.video_path = "data/00617.mp4"
        self.cap = cv2.VideoCapture(self.video_path)
        self.fps = 29.97

    def main(self, page: ft.Page):
        page.theme_mode = "light"
        #page.update()
        page.window.width = 500
        page.window.height = 800

        #ウィジェットを定義
        self.create_menubar(page)
        self.text1 = ft.Text("  ", size=22)
        self.text2 = ft.Text("字幕表示", size=22)
        self.textbox = ft.TextField(label="質問を入力", width=640)
        self.button1 = ft.ElevatedButton(text="音声認識",
                                    width=150,
                                    on_click=self.import_speech
                                    )
        self.button2 = ft.ElevatedButton(text="検索",
                                    width=150,
                                    on_click=self.search
                                    )
        self.button3 = ft.ElevatedButton(text=" ",
                                    height=300,
                                    width=500,
                                    opacity=0.0,
                                    on_click=self.video_start
                                    )
        self.image_display = ft.Image(width=640, height=400, fit=ft.ImageFit.SCALE_DOWN)

        page.add(ft.Row([self.menubar]))
        page.add(ft.Row([self.text1], alignment=ft.MainAxisAlignment.CENTER))
        self.button_set = ft.Row([self.button1, self.button2], width=640, alignment=ft.MainAxisAlignment.SPACE_EVENLY)
        #page.add(ft.Row([self.button1, self.button2], width=640, alignment=ft.MainAxisAlignment.SPACE_EVENLY))
        #page.add(ft.Row([self.textbox], alignment=ft.MainAxisAlignment.CENTER))

        container1 = ft.Container(
            content = self.image_display,
            alignment=ft.alignment.top_center,
        )

        container2 = ft.Container(
            content = self.button_set,
            alignment=ft.alignment.top_center,
        )

        page.add(container2)

        page.add(ft.Row([self.textbox], alignment=ft.MainAxisAlignment.CENTER))

        video_view = ft.Stack([container1,
                        ft.Row([self.button3],
                                height=350,
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER
                            )])

        page.add(video_view)

        container2 = ft.Container(
            content=self.text2,
            width=470,
            alignment=ft.alignment.top_center
        )
        page.add(ft.Row([container2], alignment=ft.MainAxisAlignment.CENTER))

        #画面幅に応じてテキストの表示幅を変更
        def on_resized(e):
            if not page.window.width >= 640:
                container2.width = page.window.width - 20
            else:
                container2.width = 620
            container2.update()
        page.on_resized = on_resized

        #画像を設定
        self.video_to_image()

    def import_speech(self, e):
        self.text1.value = "話してください…"
        self.button1.text = "　"
        self.text1.update()
        self.button1.update()

        #マイクで受け取った音声を認識してテキストに出力
        audio = self.speech.grab_audio()
        speech = self.speech.recognize_audio(audio)
        self.speech.speech.append(speech)

        if speech == 1:
            speech = f"認識できませんでした"
        if speech == 2:
            speech = f"音声認識のリクエストが失敗しました:"

        self.button1.text = "やり直す"
        self.text1.value = speech
        self.text1.update()
        self.button1.update()

        print(speech)
        self.inputted_text = speech
        self.search_database()

    def create_menubar(self, page: ft.Page):
        def go_to_sub1(e):
            page.go("/sub1")

        self.menubar = ft.MenuBar(
            expand=True,
            style=ft.MenuStyle(
                alignment=ft.alignment.top_center,
                mouse_cursor={
                    ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
                    ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
                }
            ),
            controls=[
                ft.SubmenuButton(
                    content=ft.Text("機能"),
                    #on_open=handle_submenu_open,
                    #on_close=handle_submenu_close,
                    #on_hover=handle_submenu_hover,
                    controls=[
                        ft.MenuItemButton(
                            content=ft.Text("もう一度再生"),
                            #leading=ft.Icon(ft.icons.INFO),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.colors.GREEN_100}
                            ),
                            on_click=self.video_start,
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("データの追加"),
                            #leading=ft.Icon(ft.icons.CLOSE),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.colors.GREEN_100}
                            ),
                            # Zon_click=go_to_sub1,
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("データの参照"),
                            #leading=ft.Icon(ft.icons.INFO),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.colors.GREEN_100}
                            ),
                            #on_click=self.video_start,
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("質問テンプレート"),
                            #leading=ft.Icon(ft.icons.INFO),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.colors.GREEN_100}
                            ),
                            #on_click=self.video_start,
                        ),
                    ],
                ),
                #"""
                ft.SubmenuButton(
                    content=ft.Text(" "),
                    #on_open=handle_submenu_open,
                    #on_close=handle_submenu_close,
                    #on_hover=handle_submenu_hover,
                    controls=[
                        ft.SubmenuButton(
                            content=ft.Text("Zoom"),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Text("Magnify"),
                                    leading=ft.Icon(ft.icons.ZOOM_IN),
                                    close_on_click=False,
                                    style=ft.ButtonStyle(
                                        bgcolor={
                                            ft.ControlState.HOVERED: ft.colors.PURPLE_200
                                        }
                                    ),
                                    #on_click=handle_menu_item_click,
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("Minify"),
                                    leading=ft.Icon(ft.icons.ZOOM_OUT),
                                    close_on_click=False,
                                    style=ft.ButtonStyle(
                                        bgcolor={
                                            ft.ControlState.HOVERED: ft.colors.PURPLE_200
                                        }
                                    ),
                                    #on_click=handle_menu_item_click,
                                ),
                            ],
                        )
                    ],
                ),
                
            ],
        )

    def search_database(self):
        if self.inputted_text == "None":
            self.text1.value = "質問を入力してください"
            self.text1.update()
            return

        self.button2.text = "検索中…"
        self.button2.update()

        print(search_ans(self.inputted_text))
        [value, similarity, ans, self.video_time] = search_ans(self.inputted_text)
        if not value:
            return
        if similarity > 0.9:
            self.ans_list = list(ans)
            self.text2.text = "　"
            self.text2.update()
            print(self.inputted_text, self.video_time)
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)

            #動画の再生開始
            self.video_start(None)

        else:
            self.text2.value = "検索結果が見つかりませんでした。"
        self.button2.text = "検索"
        self.text2.update()
        self.button2.update()

    #動画の再生準備を行う
    def video_start(self, e):
        self.loop_num = 0
        self.loop_len = 0
        self.ans_charactor = ""
        self.exit_flag = True
        self.left_time = time.time()
        self.play_sound()
        self.play_video()

    #テキストボックス入力後の検索時に関数に値を入れるために経由
    def search(self, e):
        self.inputted_text = self.textbox.value
        self.search_database()

    #音声再生
    def play_sound(self):
        pym.init()
        pym.music.load("data/00617.mp3")
        pym.music.play(loops=-1, start=self.video_time[0])

    # 動画再生関数
    def play_video(self):
        #動画の再生秒数にシーク
        start_frame = int(self.video_time[0] * self.fps)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        #動画が終了するまでループ
        while self.cap.isOpened() and self.exit_flag:
            ret, frame = self.cap.read()
            if not ret:
                break

            self.loop_num += 1

            #OpenCVのフレームをPIL画像に変換
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img)

            #PIL画像をbase64エンコード
            buffered = io.BytesIO()
            pil_img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            #FletのImageウィジェットを更新
            self.image_display.src_base64 = img_str
            self.image_display.update()

            #動画の秒数に合わせて字幕を一文字づつ表示
            if (self.video_time[1] - self.video_time[0]) * self.fps / len(self.ans_list)* 0.5 <= self.loop_num:
                if not len(self.ans_list) <= self.loop_len:
                    self.ans_charactor += self.ans_list[self.loop_len]
                self.loop_num = 0
                self.loop_len += 1
                self.text2.value = self.ans_charactor
                self.text2.update()

            # 少し待つ（フレームレート調整）
            time.sleep((1 / 1.1) / self.fps)

            #再生秒数を超えると再生停止
            if time.time() - self.left_time >= self.video_time[1] - self.video_time[0]:
                self.video_to_image()
                pym.music.stop()

    #再生停止
    def video_to_image(self):
        self.exit_flag = False
        self.image_display.src_base64 = self.image_file_to_base64("data/play_movie3.png")
        self.image_display.update()

    #画像を表示させる際、base64に変換しないと表示が更新されない
    def image_file_to_base64(self, file_path):
        with open(file_path, "rb") as image_file:
            data = base64.b64encode(image_file.read())

        return data.decode('utf-8')


if __name__ == "__main__":
    gui = GUI()
    ft.app(target=gui.main)