from pydub import AudioSegment

sound_data = AudioSegment.from_file("data\\\\voice\\\\pb_6.wav", "wav")
sound_time = round(sound_data.duration_seconds, 1)
print(sound_time)