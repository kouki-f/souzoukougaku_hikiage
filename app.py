from voice_stt.run import SpeechRecognizer
from faq_ai.faq_ai_main import search_ans
from faq_ai.video import PlayVideoWithSound


def import_speech(sp):
    #マイクで受け取った音声を認識してテキストに出力
    while True:
        audio = sp.grab_audio()
        speech = sp.recognize_audio(audio)
        sp.speech.append(speech)

        if speech == 1:
            speech = f"認識できませんでした"
        elif speech == 2:
            speech = f"音声認識のリクエストが失敗しました:"
        else:
            break

        print(speech)
    return speech

speech = SpeechRecognizer()
while(True):
    inputted_text = import_speech(speech)
    [ans, video_time] = search_ans(inputted_text)
    print(inputted_text, video_time)
    #PlayVideoWithSound("test.mp4", video_time[0], video_time[1], ans)

