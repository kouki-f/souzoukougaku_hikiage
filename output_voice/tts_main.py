from style_bert_vits2.nlp.bert_models import load_model
from style_bert_vits2.nlp.bert_models import load_tokenizer
from style_bert_vits2.tts_model import TTSModel
from pathlib import Path
from soundfile import write
from playsound import playsound

def main(output_text):
    #読み込み済のBERTモデルを取得
    load_model("JP", "ku-nlp/deberta-v2-large-japanese-char-wwm")
    load_tokenizer("JP", "ku-nlp/deberta-v2-large-japanese-char-wwm")

    #モデルを指定。ここではデフォルトモデルを指定している。
    #モデル学習が出来次第、差し替え予定
    #model_file = "jvnv-F1-jp/jvnv-F1-jp_e160_s14000.safetensors"
    #config_file = "jvnv-F1-jp/config.json"
    #style_file = "jvnv-F1-jp/style_vectors.npy"

    #安田さんの音声合成モデルに差し替え
    model_file = "yasuda/yasuda_e100_s3462.safetensors"
    config_file = "yasuda/config.json"
    style_file = "yasuda/style_vectors.npy"
    assets_root = Path("model_assets")

    #音声合成
    model = TTSModel(
        model_path=assets_root / model_file,
        config_path=assets_root / config_file,
        style_vec_path=assets_root / style_file,
        device="cpu",
    )

    #生成した音声の保存、再生
    sr, audio = model.infer(text=output_text)
    write(file="playback.wav", data=audio, samplerate=sr)
    #playsound("playback.wav")

if __name__ == '__main__':
    text = "そういうひどい収容所に放り込まれてそれからは次から次とであっちこっち引っ張り回されて農場へ行ったりそれから工場、農場関係の仕事に連れていかれたりね"
    main(text)