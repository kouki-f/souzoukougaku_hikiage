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

    # 最終行にデータを追加するメソッド
    def save_data_to_last_row(self, data, column_name):
        # 現在の最終行のインデックスを取得（データが存在する行の数）
        last_row_index = len(self.df)

        # 新しい行を作成してデータを挿入
        self.df.loc[last_row_index, "始まり"] = data[0]
        self.df.loc[last_row_index, "終わり"] = data[1]
        self.df.loc[last_row_index, "原文"] = data[2]
        self.df.loc[last_row_index, "質問1"] = data[3]
        self.df.loc[last_row_index, "質問2"] = data[4]
        self.df.loc[last_row_index, "質問3"] = data[5]
        self.df.loc[last_row_index, "データ元"] = data[6]

        # Excelファイルに上書き保存
        self.df.to_excel(self.data_path, sheet_name=self.sheet_name, index=False)

    def is_video_data(self, row):
        if self.df.at[row, "データ元"] == "動画":
            return True
        else:
            return False

    def get_video_time(self, row):
        start = self.df.at[row, "始まり"]
        stop = self.df.at[row, "終わり"]
        return [start, stop]
    
    # 全データをリストで取得
    def all_data_to_list(self):
        return self.df.values.tolist()
    

# data = ImportData("data/question_test.xlsx", "sheet1")
# print(data.all_data_to_list())