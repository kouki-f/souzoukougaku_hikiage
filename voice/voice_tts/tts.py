from utils.generation import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

# download and load all models
preload_models()

# generate audio from text
text_prompt = """
プロンプトとして音声を与えて音声合成
"""
audio_array = generate_audio(text_prompt)

# save audio to disk
write_wav("vallex_generation.wav", SAMPLE_RATE, audio_array)