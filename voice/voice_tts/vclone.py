from utils.prompt_making import make_prompt
from utils.generation import SAMPLE_RATE, generate_audio, preload_models
import soundfile as sf
from playsound import playsound
from time import time
timeprint = time()

def tts(in_prompt, in_prompt_text, out_prompt_text):
    # 全てのモデルをダウンロードして読み込む
    print(str(round(time() - timeprint, 2)) + " : start")
    preload_models()
    print(str(round(time() - timeprint, 2)) + " : download")
    make_prompt(name="empty", audio_prompt_path = in_prompt, transcript = in_prompt_text)
    print(str(round(time() - timeprint, 2)) + " : make")

    #文章を基に合成音声を生成
    audio_array = generate_audio(out_prompt_text, prompt="empty")
    print(str(round(time() - timeprint, 2)) + " : generate")

    #音声ファイルを保存、再生
    sf.write(file="playback.wav", data=audio_array, samplerate=SAMPLE_RATE)
    print(str(round(time() - timeprint, 2)) + " : save")
    playsound("playback.wav")