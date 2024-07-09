import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft

filename = 'yasuda/raw/voice_1.wav'
sample_rate, data = wavfile.read(filename)
# ステレオオーディオの場合はモノラルに変換
if len(data.shape) > 1:
    data = data[:, 0]  # 左チャネルを使用

plt.figure(figsize=(12, 4))
plt.plot(data)
plt.title("オリジナルの波形")
plt.xlabel("サンプル")
plt.ylabel("振幅")
plt.show()

data_fft = fft(data)
frequencies = np.fft.fftfreq(len(data_fft), 1/sample_rate)

threshold_frequency_low = 1000
threshold_frequency_high = 3000
noise_indices = (np.abs(frequencies) > threshold_frequency_low) & (np.abs(frequencies) < threshold_frequency_high)
data_fft[noise_indices] = 0

# 逆FFT（IFFT）を適用して時間領域のデータに戻す
noise_signal = np.real(ifft(data_fft * noise_indices))

plt.figure(figsize=(12, 4))
plt.plot(data, label='Original', alpha=0.5)
plt.plot(np.real(ifft(data_fft)), label='Cleaned', alpha=0.5)
plt.plot(noise_signal, label='Noise', color='red')
plt.title("ノイズ除去後の波形")
plt.xlabel("サンプル")
plt.ylabel("振幅")
plt.legend()
plt.show()

from IPython.display import Audio
# 元の音声データをファイルとして保存
original_file = 'original_adventurers.wav'
wavfile.write(original_file, sample_rate, data)
# ノイズ除去後の音声データをファイルとして保存
cleaned_file = 'cleaned_adventurers.wav'
wavfile.write(cleaned_file, sample_rate, np.real(ifft(data_fft)).astype(np.int16))