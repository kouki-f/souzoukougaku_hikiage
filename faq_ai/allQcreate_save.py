import create_questions as CQ
import excel_io as data


for i in range(data.data_index):
    text = data.get_data(i, '英語訳')
    Qs = CQ.create_questions(text)
    if Qs != None:
        for idx, question in enumerate(Qs):
            column_name = '質問'+str(idx+1)
            data.save_data(question, i, column_name)
    print('saved-'+str(i))