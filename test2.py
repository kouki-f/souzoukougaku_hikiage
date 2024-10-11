import flet as ft
import faq_ai.excel_io as excel_io

# 簡易DataTableのクラス、Columnコントロールを継承
class FixedHeaderDataTable(ft.Column):

    def __init__(self, headers, rows, column_widths):
        super().__init__()
        self.headers = headers
        self.rows = rows
        self.column_widths = column_widths
        self.expand = True  # ページに対して自動伸縮

        # ヘッダ部の作成
        header_controls = [
            ft.Container(ft.Text(header, weight=ft.FontWeight.BOLD), width=width, alignment=ft.alignment.center, bgcolor=ft.colors.GREY_200) \
                for header, width in zip(self.headers, self.column_widths)
        ]
        header_row = ft.Row(header_controls, alignment=ft.alignment.center, height=50)

        # データ部の作成
        row_controls = []
        for row in self.rows:
            row_cells = [
                ft.Container(ft.Text(cell), width=width, alignment=ft.alignment.center) \
                    for cell, width in zip(row, self.column_widths)
            ]
            row_controls.append(ft.Row(row_cells, alignment=ft.alignment.center))
        # スクロールできるようにColumnコントロールを用意
        scrollable_data = ft.Column(
            controls=row_controls,
            scroll=ft.ScrollMode.ALWAYS,
            expand=True  # 親のColumn内で自動伸縮
        )

        # ヘッダ部とデータ部を配置
        self.controls =[
            header_row,
            scrollable_data
        ]


def main(page: ft.Page):
    page.theme_mode = "light"
    page.title = "固定行のデータ表"
    page.window_top = 100
    page.window_left = 200
    page.window_width = 1000
    page.window_height = 600

    # ヘッダのリストを用意
    headers = ["開始秒数", "終了秒数", "回答文", "質問文1", "質問文2", "質問文3", "データ元"]
    # 列幅のリストを用意
    column_widths = [50, 50, 400, 300, 300, 300, 50]
    # データ部で表示したい2次元配列を用意
    rows = sorted(excel_io.ImportData("data/question_test.xlsx", "Sheet1").all_data_to_list(), key=lambda x: x[0])

    for i in range(len(rows)):
        for j in range(len(rows[0])):
            if type(rows[i][j]) is float:
                rows[i][j] = ""

    # 簡易DataTableを生成しページへ配置、ヘッダ／列幅／データのリストを渡します
    data_table = FixedHeaderDataTable(headers, rows, column_widths)
    page.add(data_table)

# アプリ開始
ft.app(target=main)
