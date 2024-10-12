import spacy

# spaCyの英語モデルをロード
nlp = spacy.load("_internal/ja_core_news_md/ja_core_news_md-3.7.0")

def find_most_similar_sentence(sentences, target_sentence): #sentences=list, target_sentence=str
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
    
    #most_similar_sentence=最も似ている文章 highest_similarity=似ている度合
    return most_similar_sentence, highest_similarity