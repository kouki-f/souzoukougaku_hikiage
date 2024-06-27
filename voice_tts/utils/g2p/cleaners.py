import re
from utils.g2p.japanese import japanese_to_romaji_with_accent, japanese_to_ipa, japanese_to_ipa2, japanese_to_ipa3
patterns = [r'\[EN\](.*?)\[EN\]', r'\[ZH\](.*?)\[ZH\]', r'\[JA\](.*?)\[JA\]']
def japanese_cleaners(text):
    text = japanese_to_romaji_with_accent(text)
    text = re.sub(r'([A-Za-z])$', r'\1.', text)
    return text

def japanese_cleaners2(text):
    return japanese_cleaners(text).replace('ts', 'ʦ').replace('...', '…')

def cje_cleaners(text):
    matches = []
    for pattern in patterns:
        matches.extend(re.finditer(pattern, text))

    matches.sort(key=lambda x: x.start())  # Sort matches by their start positions

    outputs = ""
    output_langs = []

    for match in matches:
        text_segment = text[match.start():match.end()]
        phon = clean_one(text_segment)
        if "[EN]" in text_segment:
            lang = 'en'
        elif "[ZH]" in text_segment:
            lang = 'zh'
        elif "[JA]" in text_segment:
            lang = 'ja'
        else:
            raise ValueError("If you see this error, please report this bug to issues.")
        outputs += phon
        output_langs += [lang] * len(phon)
    assert len(outputs) == len(output_langs)
    return outputs, output_langs


def clean_one(text):
    if text.find('[JA]') != -1:
        text = re.sub(r'\[JA\](.*?)\[JA\]',
                      lambda x: japanese_to_ipa2(x.group(1))+' ', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    return text
