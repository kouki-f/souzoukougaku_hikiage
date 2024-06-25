from utils.prompt_making import make_prompt
from utils.generation import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

# download and load all models
preload_models()

make_prompt(name="kuma", audio_prompt_path="00619_1.mp3",
transcript="三分の一ぐらいの量しか貰えん。とても、そんなもん、腹いっぱいになるようなもんでない。")

# generate audio from text
text_prompt = """
そういうひどい収容所に放り込まれてそれからは次から次とであっちこっち引っ張り回されて農場へ行ったりそれから工場、農場関係の仕事に連れていかれたりね
"""
audio_array = generate_audio(text_prompt, language="ja", prompt="kuma")

# save audio to disk
write_wav("playback.wav", SAMPLE_RATE, audio_array)