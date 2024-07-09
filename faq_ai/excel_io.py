import pandas as pd

class ImportData():
    def __init__(self, excel_path, sheet_name) -> None:
        self.data_path = excel_path
        self.sheet_name = sheet_name
        self.df = pd.read_excel(self.data_path) #エクセルファイルの読み込み
        (self.data_index, self.data_columns) = self.df.shape

    def get_data(self, row, column_name): #エクセルファイルから任意のセルの値を取得
        if pd.isna(self.df.at[row, column_name]):
            return None
        return self.df.at[row, column_name]

    def save_data(self, data, row, column_name): #エクセルファイルの任意のセルの値を上書き
        self.df.loc[row, column_name] = data
        self.df.to_excel(self.data_path, sheet_name=self.sheet_name, index=False)

    def get_video_time(self, row):
        start = self.df.at[row, "始まり"]
        stop = self.df.at[row, "終わり"]
        return [start, stop]