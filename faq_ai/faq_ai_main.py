import faq_ai.excel_io as data
import faq_ai.search_question as SQ

def search_ans(text):
    excel_path = "data/question_test.xlsx"
    sheet_name = "sheet1"
    io = data.ImportData(excel_path, sheet_name)
    i_question = text

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
    is_video = io.is_video_data(most_similar_index)

    if is_video:
        video_time = io.get_video_time(most_similar_index)
        print(most_similar_index + 1, highest_similarity, most_similar_sentence)
        return [is_video, highest_similarity, most_similar_sentence, video_time]
    else:
        print(most_similar_index + 1, highest_similarity, most_similar_sentence)
        return [is_video, highest_similarity, most_similar_sentence, [-1, -1]] # 動画データでない場合は開始終了時間に[-1, -1]を返す