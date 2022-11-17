import furigana.furigana as furigana


def return_html(text):
    result = ''
    for pair in furigana.split_furigana(text):
        if len(pair) == 2:
            kanji, hira = pair
            result = result + f"<ruby><rb>{kanji}</rb><rt>{hira}</rt></ruby>"
        else:
            result = result + pair[0]
    return result


def return_plaintext(text):
    result = ''
    for pair in furigana.split_furigana(text):
        if len(pair) == 2:
            kanji, hira = pair
            result = result + f"{kanji}({hira})"
        else:
            result = result + f"{pair[0]}"
    return result
