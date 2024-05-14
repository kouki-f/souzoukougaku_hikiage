#恐らく使わない
from pykakasi import kakasi
kks = kakasi()
word = input()
result = kks.convert(word)
for converted_word in result:
    print(f"{converted_word['hira']}", end ="")