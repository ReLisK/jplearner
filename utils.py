import os
from jisho_api.tokenize import Tokens
from jisho_api.word import Word

from PIL import Image, ImageGrab
from PyQt6.QtWidgets import QMessageBox


def get_snippet(location, filename, coordinates=None):
    if coordinates is not None:
        if coordinates[0] > coordinates[2] and coordinates[1] > coordinates[3]:
            temp = (coordinates[2], coordinates[3], coordinates[0], coordinates[1])
            coordinates = temp
    snapshot = ImageGrab.grab(bbox=coordinates)
    save_path = os.path.join(
        location,
        filename
    )
    snapshot.save(save_path)
    return save_path


def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def qt_alert(msg):
    msg_box = QMessageBox()
    msg_box.setText(msg)
    msg_box.exec()

def j_tokenize(text):
    kana = ['あ', 'い', 'う', 'え', 'お', 'や', 'ゆ', 'よ', 'か', 'き', 'く', 'け', 'こ', 'きゃ', 'きゅ', 'きょ', 'さ', 'し', 'す', 'せ', 'そ',
            'しゃ', 'しゅ',
            'しょ', 'た', 'ち', 'つ', 'て', 'と', 'ちゃ', 'ちゅ', 'ちょ', 'な', 'に', 'ぬ', 'ね', 'の', 'にゃ', 'にゅ', 'にょ', 'は', 'ひ', 'ふ',
            'へ', 'ほ', 'ひゃ',
            'ひゅ', 'ひょ', 'ま', 'み', 'む', 'め', 'も', 'みゃ', 'みゅ', 'みょ', 'や', 'ゆ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ', 'りゃ', 'りゅ',
            'りょ', 'わ', 'ゐ',
            'ゑ', 'を', 'ん', 'が', 'ぎ', 'ぐ', 'げ', 'ご', 'ぎゃ', 'ぎゅ', 'ぎょ', 'ざ', 'じ', 'ず', 'ぜ', 'ぞ', 'じゃ', 'じゅ', 'じょ', 'だ',
            'ぢ', 'づ', 'で',
            'ど', 'ぢゃ', 'ぢゅ', 'ぢょ', 'ば', 'び', 'ぶ', 'べ', 'ぼ', 'びゃ', 'びゅ', 'びょ', 'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ', 'ぴゃ', 'ぴゅ', 'ぴょ',
            'ア', 'イ',
            'ウ', 'エ', 'オ', 'ャ', 'ュ', 'ョ', 'カ', 'キ', 'ク', 'ケ', 'コ', 'キャ', 'キュ', 'キョ', 'サ', 'シ', 'ス', 'セ', 'ソ', 'シャ',
            'シュ', 'ショ', 'タ',
            'チ', 'ツ', 'テ', 'ト', 'チャ', 'チュ', 'チョ', 'ナ', 'ニ', 'ヌ', 'ネ', 'ノ', 'ニャ', 'ニュ', 'ニョ', 'ハ', 'ヒ', 'フ', 'ヘ', 'ホ',
            'ヒャ', 'ヒュ',
            'ヒョ', 'マ', 'ミ', 'ム', 'メ', 'モ', 'ミャ', 'ミュ', 'ミョ', 'ヤ', 'ユ', 'ヨ', 'ラ', 'リ', 'ル', 'レ', 'ロ', 'リャ', 'リュ', 'リョ',
            'ワ', 'ヰ', 'ヱ',
            'ヲ', 'ン', 'ガ', 'ギ', 'グ', 'ゲ', 'ゴ', 'ギャ', 'ギュ', 'ギョ', 'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ', 'ジャ', 'ジュ', 'ジョ', 'ダ', 'ヂ',
            'ヅ', 'デ', 'ド',
            'ヂャ', 'ヂュ', 'ヂョ', 'バ', 'ビ', 'ブ', 'ベ', 'ボ', 'ビャ', 'ビュ', 'ビョ', 'パ', 'ピ', 'プ', 'ペ', 'ポ', 'ピャ', 'ピュ', 'ピョ', '。', '、', '|'
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    r = Tokens.request(text)
    if r:
        r_filtered = [obj.token for obj in r if obj.token not in kana]
    else:
        return None
    return r_filtered


def definition_dict(text, pbar=None):
    token_list = j_tokenize(text)
    oxford = {}
    if token_list:
        for token in token_list:
            pval = pbar.value()
            if pval < 99:
                pbar.setValue(pval + 1)
            word = Word.request(token)
            if word:
                r = word.data[0].senses
                r = [r.english_definitions for r in r]
                from itertools import chain
                r = list(chain(*r))
                oxford[token] = r
    return oxford


# text = '日本と中国の関係が発展するように話し合いを続けることを決めました。'
# import MeCab
# def smthn(jp_text):
#     chasen = MeCab.Tagger("-Owakati")
#     split_text = chasen.parse(jp_text).split()
#     return split_text
#
# parsed = smthn(text)
# print(parsed)
#
# import requests
# import json
#
# data = {
#   "query": f"{{word}}",
#   "language": "English",
#   "no_english": 'false'
# }
#
# url = "https://jotoba.de/api/search/words"
# r = requests.post(url, json.dumps(data))
# print(r)

