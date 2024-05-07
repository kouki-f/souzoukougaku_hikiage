import spacy

# spaCyの英語モデルをロード
nlp = spacy.load("ja_core_news_md")

def find_most_similar_sentence(sentences, target_sentence):
    # ターゲットの文章をspaCyのドキュメントオブジェクトに変換
    target_doc = nlp(target_sentence)
    
    # 最も類似度が高い文章とその類似度を初期化
    most_similar_sentence = None
    highest_similarity = 0.0
    
    # 文章群の中から最も類似度が高い文章を探す
    for sentence in sentences:
        # 比較する文章をspaCyのドキュメントオブジェクトに変換
        doc = nlp(sentence)
        
        # 類似度を計算
        similarity = doc.similarity(target_doc)
        
        # 最も高い類似度とそれに対応する文章を更新
        if similarity > highest_similarity:
            highest_similarity = similarity
            most_similar_sentence = sentence
    
    return most_similar_sentence, highest_similarity

# 文章群
sentences = [
    "ブラゴヴェとはどういうところだったのですか。",
    "部隊内ではどのような仕事をしていましたか。",
    "帰ってきて初めて日本を見たときはどのように感じましたか",
]

# 指定した文章
target_sentence = "ブラゴヴェはどんな場所ですか。"

# 最も類似度が高い文章とその類似度を求める
most_similar, similarity = find_most_similar_sentence(sentences, target_sentence)

print("指定した文章:", target_sentence)
print("最も類似度が高い文章:", most_similar)
print("類似度:", similarity)
