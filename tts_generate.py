from style_bert_vits2.nlp.bert_models import load_model
from style_bert_vits2.nlp.bert_models import load_tokenizer
from style_bert_vits2.tts_model import TTSModel
from pathlib import Path
from soundfile import write
import sys
import os

def main_thread(output_text):
    #読み込み済のBERTモデルを取得
    load_model("JP", "ku-nlp/deberta-v2-large-japanese-char-wwm")
    load_tokenizer("JP", "ku-nlp/deberta-v2-large-japanese-char-wwm")

    #安田さんの音声合成モデルを指定
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

    DIR = "./data/voice"
    dir_filenum = sum(os.path.isfile(os.path.join(DIR, name)) for name in os.listdir(DIR)) + 1
    write(file=f"data/voice/pb_{dir_filenum}.wav", data=audio, samplerate=sr)

    return dir_filenum