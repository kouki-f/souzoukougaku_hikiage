def main(output_text):
    from style_bert_vits2.nlp import bert_models
    from style_bert_vits2.tts_model import TTSModel
    from pathlib import Path
    import soundfile as sf
    from playsound import playsound

    #読み込み済のBERTモデルを取得
    bert_models.load_model("JP", "ku-nlp/deberta-v2-large-japanese-char-wwm")
    bert_models.load_tokenizer("JP", "ku-nlp/deberta-v2-large-japanese-char-wwm")
    assets_root = Path("model_assets")

    #モデルを指定。ここではデフォルトモデルを指定している。
    #モデル学習が出来次第、差し替え予定
    #model_file = "jvnv-F1-jp/jvnv-F1-jp_e160_s14000.safetensors"
    #config_file = "jvnv-F1-jp/config.json"
    #style_file = "jvnv-F1-jp/style_vectors.npy"

    #安田さんの音声合成モデルに差し替え
    model_file = "yasuda/yasuda_e100_s3462.safetensors"
    config_file = "yasuda/config.json"
    style_file = "yasuda/style_vectors.npy"

    #音声合成
    model = TTSModel(
        model_path=assets_root / model_file,
        config_path=assets_root / config_file,
        style_vec_path=assets_root / style_file,
        device="cpu",
    )

    #生成した音声の保存、再生
    sr, audio = model.infer(text=output_text)
    sf.write(file="playback.wav", data=audio, samplerate=sr)
    playsound("playback.wav")

if __name__ == '__main__':
    main()