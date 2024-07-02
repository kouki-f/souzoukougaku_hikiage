from pprint import pprint
import nltk
#nltk.download('stopwords')
from Questgen import main

from faq_ai.excel_io import ImportData

data = ImportData()
qg = main.QGen()

#文章から質問を生成してリターンする関数
def create_questions(text):
    # すべてのidのQuestionを取得する関数
    def get_all_questions(data):
        questions = []
        if data.get('questions', None) is not None:#質問が生成されなかったら飛ばす
            for question in data['questions']:
                questions.append(question['Question'])
        return questions
    
    payload = {
        "input_text": text,
        "max_questions": 5
    }
    output = qg.predict_shortq(payload)
    all_question = get_all_questions(output)

    return all_question

#1行ずつ質問を生成してExcelに保存する関数
for i in range(data.data_index):
    text = data.get_data(i, '英語訳')
    Qs = create_questions(text)
    if Qs != None:
        for idx, question in enumerate(Qs):
            column_name = '質問'+str(idx+1)
            data.save_data(question, i, column_name)
    print('saved-'+str(i))