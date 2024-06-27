from vclone import tts

input_prompt = "00619_1.mp3"
input_prompt_text = "三分の一ぐらいの量しか貰えん。とても、そんなもん、腹いっぱいになるようなもんでない。"
output_prompt_text = "そういうひどい収容所に放り込まれてそれからは次から次とであっちこっち引っ張り回されて農場へ行ったりそれから工場、農場関係の仕事に連れていかれたりね"

tts(input_prompt, input_prompt_text, output_prompt_text)