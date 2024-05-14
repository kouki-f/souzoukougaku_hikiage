#恐らく使わない
#標準的な音声合成ライブラリ
import pyttsx3

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
text = "おしょうのかいてくれたかみをくまさんはよみあげる。「ええー、じゅげむじゅげむ、ごこうのすりきれ、うみじゃりすいぎょのすいぎょうまつ、うんらいまつ、ふうらいまつ、くうねるところにすむところ、やぶらこうじのぶらこうじ、ぱいぽぱいぽ、ぱいぽのしゅーりんがん、しゅーりんがんのぐーりんだい、ぐーりんだいのぽんぽこぴーのぽんぽこなのちょうきゅういのちのち ょうすけ、うーん、こうなべてみるとみんなつけてえなまえばかりですねえ"
engine.say(text)
engine.runAndWait()