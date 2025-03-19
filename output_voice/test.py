import flet as ft
import sys
from tts_generate import main_thread

class GUIConsole:
    def __init__(self, page: ft.Page):
        """コンソール出力をGUIに表示するクラス"""
        self.page = page
        # コンソール出力を表示するTextウィジェット
        self.output = ft.Text(value="", selectable=True)
        # Textウィジェットを囲むContainerウィジェット
        self.container = ft.Container(
            content=self.output,
            border=ft.border.all(1, ft.Colors.GREY_400), #colorsからColorsに変更
            padding=10,
            expand=True,  # 親ウィジェットのスペースを最大限に利用
        )
        # Containerウィジェットを水平方向に配置するRowウィジェット
        self.row = ft.Row(
            controls=[self.container],
            expand=True,  # 親ウィジェットのスペースを最大限に利用
            vertical_alignment=ft.CrossAxisAlignment.START,  # 上寄せで配置
        )
        # Rowウィジェットをページに追加
        page.add(self.row)
        # 標準出力の元の状態を保存
        self.original_stdout = sys.stdout
        # 標準出力をリダイレクト
        sys.stdout = self.StdoutRedirector(self.output)

    def close(self):
        """標準出力を元の状態に戻す"""
        sys.stdout = self.original_stdout

    class StdoutRedirector:
        """標準出力を指定されたTextウィジェットにリダイレクトするクラス"""
        def __init__(self, text_widget: ft.Text):
            self.text_widget = text_widget

        def write(self, message: str):
            """標準出力に書き込まれた内容をTextウィジェットに追加する"""
            self.text_widget.value += message
            if '\n' in message:
                # 改行が含まれる場合はTextウィジェットを更新
                self.text_widget.update()

        def flush(self):
            pass

def main(page: ft.Page):
    console = GUIConsole(page)
    main_thread("こんにちは")

ft.app(target=main)