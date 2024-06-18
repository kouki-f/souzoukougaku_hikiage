import pandas as pd

class ImportData():
    def __init__(self) -> None:
        self.data_path = 'data\sampleData.xlsx'
        self.sheet_name = 'data1'
        self.df = pd.read_excel(self.data_path) #エクセルファイルの読み込み
        (self.data_index, self.data_columns) = self.df.shape

    def get_data(self, row, column_name): #エクセルファイルから任意のセルの値を取得
        return self.df.at[row, column_name]

    def save_data(self, data, row, column_name): #エクセルファイルの任意のセルの値を上書き
        self.df.loc[row, column_name] = data
        self.df.to_excel(self.data_path, sheet_name=self.sheet_name, index=False)