#pip install style-bert-vits2
from style_bert_vits2.nlp import bert_models
from style_bert_vits2.constants import Languages

# BERTモデルをロード,モデルが無ければダウンロード
bert_models.load_model(Languages.JP, "ku-nlp/deberta-v2-large-japanese-char-wwm")
bert_models.load_tokenizer(Languages.JP, "ku-nlp/deberta-v2-large-japanese-char-wwm")

# Hugging Faceからデフォルトモデルをダウンロード
# モデル学習が完成次第、差し替える予定
# model_assetsディレクトリにダウンロードされる
from pathlib import Path
from huggingface_hub import hf_hub_download

model_file = "jvnv-F1-jp/jvnv-F1-jp_e160_s14000.safetensors"
config_file = "jvnv-F1-jp/config.json"
style_file = "jvnv-F1-jp/style_vectors.npy"

for file in [model_file, config_file, style_file]:
    print(file)
    hf_hub_download("litagin/style_bert_vits2_jvnv", file, local_dir="model_assets")