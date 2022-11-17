import os
import time
import MeCab

import imagehash
import pytesseract
from furigana.furigana import print_html
from furigana_mod import return_plaintext, return_html
from PIL import Image, ImageGrab
from PyQt6 import QtCore, QtWebEngineWidgets
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

import utils
from constants import *


class Translator:
    def __init__(self, mainwindow):
        self.main_window = mainwindow
        self.text = []
        self.layout = self.main_window.layout
        self.coordinates = self.main_window.coordinates
        self.coordinates_label = QLabel(f"Box coordinates: {self.coordinates}")
        # Add scroll area for translations
        self.scroll = (
            QScrollArea()
        )  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.scroll_text_box = (
            QVBoxLayout()
        )  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        self.widget.setLayout(self.scroll_text_box)

        # Scroll Area Properties
        self.scroll_bar = self.scroll.verticalScrollBar()
        # self.scroll_bar.sliderChange(self.scroll_bar.SliderChange.SliderRangeChange)
        self.scroll.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.scroll.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        layout1 = QVBoxLayout()
        layout1.addWidget(self.scroll)
        lower_Hbox = QHBoxLayout()
        lower_Hbox.addWidget(self.coordinates_label)
        self.tl_snap_button = QPushButton("Snap")
        self.tl_snap_button.clicked.connect(self.main_window._tl_snap_button)
        lower_Hbox.addWidget(self.tl_snap_button)
        layout1.addLayout(lower_Hbox)
        self.layout.addLayout(layout1)

        self.view = QtWebEngineWidgets.QWebEngineView()
        self.scroll_text_box.addWidget(self.view)


    def translate(self):
        save_path = utils.get_snippet(TRANSLATION_PICS_SAVE_LOCATION, TRANSLATION_PICS_FILE_NAME, coordinates=self.coordinates)
        print(pytesseract.get_languages(config=""))
        if self.main_window.jp2f.isChecked():
            # do below aka translate to furigana
            pass
        elif self.main_window.jp2eng.isChecked():
            # give eng translation
            pass
        try:
            translation_output = pytesseract.image_to_string(
                Image.open(save_path), lang='jpn', timeout=1
            )
            self.create_json(translation_output)
            translation_output = return_html(translation_output)
            self.text.append(f"{translation_output}")
            html_list = self.list2html(self.text)
            print(html_list)
            html = f'''<!DOCTYPE html>
                        <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <title>Title</title>
                            </head>
                            <body>
                                <p>
                                    {html_list}
                                </p>
                            </body>
                        </html>'''
            self.view.setHtml(html)
        except RuntimeError as e:
            print(e)
            pass

        self.scroll_bar.rangeChanged.connect(self._onRangeChanged)

    def _onRangeChanged(self):
        # Set scrollbar to bottom whenever updated.
        self.scroll_bar.setSliderPosition(self.scroll_bar.maximum())

    def list2html(self, elements):
        return '<ul>\n' + '\n'.join(['<li>'.rjust(8) + name + '</li>' for name in elements]) + '\n</ul>'

    def create_json(self, jp_text):
        chasen = MeCab.Tagger("-Ochasen")
        sd =chasen.parse(jp_text).split()
        print(sd)
        yomi = MeCab.Tagger("-Oyomi")
        sd = chasen.parse(jp_text).split()
        print(sd)
