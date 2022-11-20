import os
import time
import MeCab
import json
import logging

from jamdict import Jamdict

import imagehash
import pytesseract
import translators as ts
from furigana_fork.furigana.furigana import print_html, return_html
from PIL import Image, ImageGrab
from PyQt6 import QtCore, QtWebEngineWidgets
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QSizePolicy,
    QWidget,
)

import utils
from constants import *

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

class Translator:
    def __init__(self, mainwindow):
        self.jam = Jamdict()
        self.main_window = mainwindow
        self.layout = self.main_window.layout
        self.coordinates = self.main_window.coordinates
        self.coordinates_label = QLabel(f"Box coordinates: {self.coordinates}")
        # Add scroll area for translations
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.view.setMinimumHeight(100)
        self.view.setMinimumWidth(500)
        self.h_box = (
            QHBoxLayout()
        )  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        self.h_box.addWidget(self.view)
        layout1 = QVBoxLayout()
        layout1.addLayout(self.h_box)
        lower_Hbox = QHBoxLayout()
        lower_Hbox.addWidget(self.coordinates_label)
        self.tl_snap_button = QPushButton("Snap")
        self.tl_snap_button.clicked.connect(self.main_window._tl_snap_button)
        lower_Hbox.addWidget(self.tl_snap_button)
        layout1.addLayout(lower_Hbox)
        self.layout.addLayout(layout1)
        self.init_html()

    def translate(self):
        self.text = []
        save_path = utils.get_snippet(
            TRANSLATION_PICS_SAVE_LOCATION,
            TRANSLATION_PICS_FILE_NAME,
            coordinates=self.coordinates,
        )
        print(pytesseract.get_languages(config=""))
        if self.main_window.jph.isChecked():
            lang = 'jpn'
        elif self.main_window.jpv.isChecked():
            lang = 'jpn_vert'
        try:
            ocr_output = pytesseract.image_to_string(
                Image.open(save_path), lang=lang, timeout=1
            )
            print(ocr_output)
            furigana_conversion = return_html(ocr_output)
            print_html(ocr_output)
            self.text.append(f"{furigana_conversion}")
            html_list = self.list2html(elements=self.text, raw_text=ocr_output) + '\n<!--tl_list-->'
            with open('index.html', 'r', encoding="utf-8") as f:
                data = f.read()
                data = data.replace("<!--tl_list-->", html_list)
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(data)
            self.create_js(ocr_output)
            self.view.reload()
            # self.view.setHtml(html)
        except Exception as e:
            print(e)
            raise

    def list2html(self, elements, raw_text):
        try:
            translation = self.deepl_translate(raw_text)
        except:
            try:
                translation = self.google_translate(raw_text)
            except Exception as e:
                translation = str(e)
        return (
            f"<div class ='tooltip-container'>\n"
            f"<p class = 'tooltip-text'> {translation}</p>\n"
            "<ul class='tooltip-list'>\n"
            + "\n".join(["<li>".rjust(8) + name + "</li>" for name in elements])
            + "\n</ul>\n"
              "</div>\n"
        )

    def deepl_translate(self, raw_text):
        translated_text = ts.deepl(raw_text, to_language='en')
        return translated_text

    def google_translate(self, raw_text):
        translated_text = ts.google(raw_text, to_language='en')
        return translated_text

    def create_js(self, jp_text):
        # split_text_definitions = []
        # print(f"text: {jp_text}")
        # chasen = MeCab.Tagger("-Owakati")
        # split_text = chasen.parse(jp_text).split()
#         kana = ['あ','い','う','え','お','や','ゆ','よ','か','き','く','け','こ','きゃ','きゅ','きょ','さ','し','す','せ','そ','しゃ','しゅ',
# 'しょ','た','ち','つ','て','と','ちゃ','ちゅ','ちょ','な','に','ぬ','ね','の','にゃ','にゅ','にょ','は','ひ','ふ','へ','ほ','ひゃ',
# 'ひゅ','ひょ','ま','み','む','め','も','みゃ','みゅ','みょ','や','ゆ','よ','ら','り','る','れ','ろ','りゃ','りゅ','りょ','わ','ゐ',
# 'ゑ','を','ん','が','ぎ','ぐ','げ','ご','ぎゃ','ぎゅ','ぎょ','ざ','じ','ず','ぜ','ぞ','じゃ','じゅ','じょ','だ','ぢ','づ','で',
# 'ど','ぢゃ','ぢゅ','ぢょ','ば','び','ぶ','べ','ぼ','びゃ','びゅ','びょ','ぱ','ぴ','ぷ','ぺ','ぽ','ぴゃ','ぴゅ','ぴょ','ア','イ',
# 'ウ','エ','オ','ャ','ュ','ョ','カ','キ','ク','ケ','コ','キャ','キュ','キョ','サ','シ','ス','セ','ソ','シャ','シュ','ショ','タ',
# 'チ','ツ','テ','ト','チャ','チュ','チョ','ナ','ニ','ヌ','ネ','ノ','ニャ','ニュ','ニョ','ハ','ヒ','フ','ヘ','ホ','ヒャ','ヒュ',
# 'ヒョ','マ','ミ','ム','メ','モ','ミャ','ミュ','ミョ','ヤ','ユ','ヨ','ラ','リ','ル','レ','ロ','リャ','リュ','リョ','ワ','ヰ','ヱ',
# 'ヲ','ン','ガ','ギ','グ','ゲ','ゴ','ギャ','ギュ','ギョ','ザ','ジ','ズ','ゼ','ゾ','ジャ','ジュ','ジョ','ダ','ヂ','ヅ','デ','ド',
# 'ヂャ','ヂュ','ヂョ','バ','ビ','ブ','ベ','ボ','ビャ','ビュ','ビョ','パ','ピ','プ','ペ','ポ','ピャ','ピュ','ピョ']
#         for word in split_text:
#             if word in kana:
#                 split_text.remove(word)
#         print(f"split text: {split_text}")
#
#         for text in split_text:
#             definition = self.jam.lookup(text, strict_lookup=True)
#             if len(definition.entries) > 0:
#                 split_text_definitions.append(str(definition.entries))
#             else:
#                 split_text_definitions.append('')
#         dict_conversion = dict(zip(split_text, split_text_definitions))
#         print(str(dict_conversion))
        dict_conversion = {'test':'test'}
        js = f"""var dict = {dict_conversion};
function get_definitions() {{

let text = document.getElementById("list").textContent;
console.log(text);
console.log(dict);
var boundary = document.getElementById('list');
var mouseOverFunction = function () {{
    this.style.color = "blue"; // your colour change
}};
var boundary = document.getElementById('list');
const li = document.getElementById('wordlist');
}}
function appendDefinition(text){{
    if (text in dict) {{
        console.log('?SDFS');
        let p = document.createElement('p');
        p.innerHTML = dict[text];
        console.log(dict);
        document.getElementById('test').appendChild(p);
    }} else {{
        console.log('NOT found in dict');
    }}
}}
get_definitions();
// selecting the elements for which we want to add a tooltip
// const target = document.getElementById("tooltip-list");
const target = document.getElementsByClassName("tooltip-list");
// const tooltip = document.getElementById("tooltip-text");
const tooltip = document.getElementsByClassName("tooltip-text");

for (let i=0; i < target.length; i++)
{{
    // change display to 'block' on mouseover
    target[i].addEventListener('mouseover', () => {{
        tooltip[i].style.display = 'block';
    }}, false);
    // change display to 'none' on mouseleave
    target[i].addEventListener('mouseleave', () => {{
      tooltip[i].style.display = 'none';
    }}, false);
}}
document.getElementById('scroll').scrollIntoView();

"""
        try:
            with open('javascript.js', 'w+', encoding="utf-8") as jsfile:
                jsfile.write(js)
        except Exception as e:
            print(e)

    def run_js(self):
        self.view.page().runJavaScript("document.getElementById('scroll').scrollIntoView();")
        pass

    def init_html(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        index_html = '''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
        <style>
            /* this is a _demo_ container. remember the importance of relative and absolute positioning */
            .tooltip-container {
                position: relative;
                display: flex;
                place-content: center;
            }

            /* styling of the tooltip display */
            .tooltip-text {
                display: none;
                position: absolute;
                top: -60px;
                z-index: 1;
                background: #00732c;
                padding: 8px;
                font-size: 1rem;
                color: #fff;
                border-radius: 2px;
                animation: fadeIn 0.6s;
            }

            /* optional styling to add a "wedge" to the tooltip */
            .tooltip-text:before {
              content: "";
              position: absolute;
              top: 100%;
              left: 50%;
              margin-left: -8px;
              border: 8px solid transparent;
              border-top: 8px solid #00732c;
            }

            @keyframes fadeIn {
             from {
               opacity: 0;
             }
             to {
               opacity: 1;
             }
            }
        </style>
    </head>
    <body>
        <p id="list">
            Press Snap!
            <!--tl_list-->
        <div id="scroll"></div>
        </p>
    </body>
    <script type = "text/javascript" src = "./javascript.js"></script>
</html>
        '''
        with open("index.html", 'w+', encoding="utf-8") as f:
            f.write(index_html)
        url = QtCore.QUrl.fromLocalFile(os.path.join(current_dir, "index.html"))
        self.view.load(url)
        self.view.loadFinished.connect(self.run_js)
