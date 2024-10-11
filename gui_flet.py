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
        self.width = 800

        #cv2で動画を読み込む
        self.video_path = "data/00617.mp4"
        self.cap = cv2.VideoCapture(self.video_path)
        self.fps = 29.97

    def main(self, page: ft.Page):
        page.title = "抑留者データベース-安田"
        page.theme_mode = "light"
        #page.update()
        page.window.width = 500
        page.window.height = 800

        self.page_main(page)

        """
        time.sleep(5)
        self.page_sub1(page)
        time.sleep(5)
        self.page_main(page)
        #"""

    #ウィジェットを定義
    def page_main(self, page):
        page.controls.clear()
        self.create_menubar(page)
        self.text1 = ft.Text("  ", size=22)
        self.text2 = ft.Text("字幕表示", size=22)
        self.textbox_text = ft.TextField(label="質問を入力", width=self.width)
        self.textbox = ft.Container(content = self.textbox_text, alignment=ft.alignment.center, width = self.width)
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
        self.image_display = ft.Image(width=self.width, height=400, fit=ft.ImageFit.COVER)

        page.add(ft.Row([self.menubar]))
        page.add(ft.Row([self.text1], alignment=ft.MainAxisAlignment.CENTER))
        self.button_set = ft.Row([self.button1, self.button2], width=self.width, alignment=ft.MainAxisAlignment.SPACE_EVENLY)
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
            width=self.width - 10,
            alignment=ft.alignment.top_center
        )
        page.add(ft.Row([container2], alignment=ft.MainAxisAlignment.CENTER))

        #画面幅に応じてテキストの表示幅を変更
        def on_resized(e):
            if not page.window.width >= self.width:
                container2.width = page.window.width - 20
            else:
                container2.width = self.width - 20
            container2.update()
        page.on_resized = on_resized

        #画像を設定
        self.video_to_image()

    def page_sub1(self, page):
        def on_file_picked(e: ft.FilePickerResultEvent):
            if e.files:
                target_file.current.value = e.files[0].path
                page.update()

        def show_file_picker(_: ft.ControlEvent):
            file_picker.pick_files(
                allow_multiple=False,
                file_type="custom",
                allowed_extensions=image_extensions
            )

        target_file = ft.Ref[ft.Text]()
        image_extensions = ["mp4", "MTS"]
        file_picker = ft.FilePicker(on_result=on_file_picked)
        page.overlay.append(file_picker)

        page.controls.clear()
        self.create_menubar(page)
        self.text1 = ft.Text("Excelにデータを追加", size=22)
        self.text_a = ft.Container(ft.Text("※必須の入力項目です", size=14, color="red"), padding=0, alignment=ft.alignment.center_left, width=800)
        self.textbox1 = ft.Container(ft.TextField(label="回答文", width=800), padding=ft.Padding(0, 20, 0, 0), alignment=ft.alignment.center)
        self.textbox2 = ft.Container(ft.TextField(label="質問文１", width=800), padding=ft.Padding(0, 50, 0, 0), alignment=ft.alignment.center_left, width=800)
        self.textbox3 = ft.Container(ft.TextField(label="質問文２", width=800), padding=ft.Padding(0, 15, 0, 0), alignment=ft.alignment.center)
        self.textbox4 = ft.Container(ft.TextField(label="質問文３", width=800), padding=ft.Padding(0, 39, 0, 20), alignment=ft.alignment.center)

        text_sentence = "※質問文を増やすほど、回答の精度がより高くなります。"
        self.text2 = ft.Container(ft.Text(text_sentence, size=20, color="red"), padding=0, alignment=ft.alignment.center_left, width=800)

        self.button1 = ft.Container(
            ft.ElevatedButton(
                text="保存して戻る",
                width=150,
                on_click=lambda e: self.page_main(page)
                ),
                alignment=ft.alignment.center_right,
                width=800,
            )

        self.dropdown1 = ft.Dropdown(
        width=130,
        label="データ形式",
            options=[
                ft.dropdown.Option("動画"),
                ft.dropdown.Option("文字"),
            ],
            on_change=lambda e: self.select_file_button(page),
        )

        self.button2 = ft.ElevatedButton("動画を指定", on_click=show_file_picker)

        textbox_group = ft.Column([
                self.textbox1,
                self.text_a,
                self.textbox2,
                self.text_a,
                self.textbox3,
                self.textbox4,
                self.text2,
                self.button1],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER)

        page.add(ft.Row([self.menubar]))
        page.add(ft.Row([self.text1], alignment=ft.MainAxisAlignment.CENTER))

        page.add(ft.Row(controls=[
            self.dropdown1,
            self.button2,
            ft.Text(ref=target_file),
        ],
        alignment=ft.MainAxisAlignment.CENTER
        ))

        page.add(textbox_group)

    def select_file_button(self, page: ft.Page):
        print(self.dropdown1.value)
        if self.dropdown1.value == "動画":
            self.button2.visible = True
        else:
            self.button2.visible = False
        page.update()

    def page_sub2(self, page):
        page.controls.clear()
        self.create_menubar(page)
        self.text1 = ft.Text("Excelにデータを追加", size=22)
        self.textbox1 = ft.TextField(label="開始秒数", width=100)
        self.textbox2 = ft.TextField(label="終了秒数", width=100)
        self.textbox3 = ft.TextField(label="回答文", width=500)
        self.textbox4 = ft.TextField(label="質問文１", width=500)
        self.textbox5 = ft.TextField(label="質問文２", width=500)
        self.textbox6 = ft.TextField(label="質問文３", width=500)
        self.button1 = ft.ElevatedButton(text="保存して戻る",
                            width=150,
                            on_click=lambda e: self.page_main(page)
                            )
        self.dropdown1 = ft.Dropdown(
        width=130,
        label="データ形式",
            options=[
                ft.dropdown.Option("動画"),
                ft.dropdown.Option("文字"),
            ],
        )
        page.add(ft.Row([self.menubar]))
        page.add(ft.Row([self.text1], alignment=ft.MainAxisAlignment.CENTER))
        page.add(ft.Row([
                self.textbox1,
                self.textbox2,
                self.dropdown1
                ],
                alignment=ft.MainAxisAlignment.CENTER))

        page.add(ft.Column([
                self.textbox3,
                self.textbox4,
                self.textbox5,
                self.textbox6],
                alignment=ft.MainAxisAlignment.CENTER))

        page.add(ft.Row([self.button1], alignment=ft.MainAxisAlignment.END))

    def page_list(self, page):
        page.controls.clear()
        self.create_menubar(page)

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

    def create_menubar(self, page):
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
                            on_click=lambda e: self.page_sub1(page),
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("データの追加-詳細モード"),
                            #leading=ft.Icon(ft.icons.INFO),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.colors.GREEN_100}
                            ),
                            on_click=lambda e: self.page_sub2(page),
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
        self.inputted_text = self.textbox_text.value
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