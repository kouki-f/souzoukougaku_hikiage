import excel_io as data
import search_question as SQ


excel_path = "data/question_test.xlsx"
sheet_name = "sheet1"

io = data.ImportData(excel_path, sheet_name)

i_question = "誰が看病してくれたのですか？"

highest_similarity = 0
most_similar_index = 0
for idx in range(io.data_index):
    sentences = []
    for i in range(3):
        column_name = "質問" + str(i+1)
        question = io.get_data(idx, column_name)
        if question is not None:
            sentences.append(question)
        else:
            break
    (_, similarity) = SQ.find_most_similar_sentence(sentences, i_question)
    #print(idx, similarity)
    if highest_similarity < similarity:
        highest_similarity = similarity
        most_similar_index = idx

most_similar_sentence = io.get_data(most_similar_index, "原文")

print(most_similar_index + 1, highest_similarity, most_similar_sentence)