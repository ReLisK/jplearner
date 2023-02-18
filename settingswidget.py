from PyQt6.QtCore import (
    Qt,
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import (
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QColorDialog,
    QMainWindow,
    QRadioButton,
    QGridLayout,
    QDialog,
    QDialogButtonBox,
    QCheckBox,
    QSpinBox,
    QWidget,
    QComboBox,
    QFileDialog,
    QLineEdit,
)
import sys
import configparser
import constants
import translators as tss

config = configparser.ConfigParser()
config.read(constants.CONFIG_FILE)

class SettingsWindow(QDialog):
    """
    General Settings
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon("./assets/setting.png"))
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setMinimumWidth(500)
        self.setMinimumHeight(200)
        QBtn = QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Close
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.Save)
        self.buttonBox.rejected.connect(self.Close)

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # COLORS
        self.color_layout = QVBoxLayout()
        colors = QLabel("Colors")
        F = QFont()
        F.setBold(True)
        F.setUnderline(True)
        colors.setFont(F)

        kanjidict_kanji_color_Hlayout = QHBoxLayout()
        kanjidict_kanji_color = QPushButton("kanjidict kanji color", self)
        self.kanjidict_kanji_color_check = QCheckBox("", self)
        self.kanjidict_kanji_color_check.setStyleSheet("QCheckBox::indicator"
                                                       "{"
                                                       f"background-color : {config['DEFAULT']['kanjidictkanjicolor']};"
                                                       "}")
        kanjidict_kanji_color_Hlayout.addWidget(kanjidict_kanji_color)
        kanjidict_kanji_color_Hlayout.addWidget(self.kanjidict_kanji_color_check)

        tooltip_color_Hlayout = QHBoxLayout()
        tooltip_color = QPushButton("ToolTip Font Color", self)
        self.tooltip_color_check = QCheckBox("", self)
        self.tooltip_color_check.setStyleSheet("QCheckBox::indicator"
                                          "{"
                                          f"background-color : {config['DEFAULT']['tooltipfontcolor']};"
                                          "}")
        tooltip_color_Hlayout.addWidget(tooltip_color)
        tooltip_color_Hlayout.addWidget(self.tooltip_color_check)

        tooltip_bcolor_Hlayout = QHBoxLayout()
        tooltip_bcolor = QPushButton("ToolTip Background Color", self)
        self.tooltip_bcolor_check = QCheckBox("", self)
        self.tooltip_bcolor_check.setStyleSheet("QCheckBox::indicator"
                                          "{"
                                          f"background-color : {config['DEFAULT']['tooltipbackgroundcolor']};"
                                          "}")
        tooltip_bcolor_Hlayout.addWidget(tooltip_bcolor)
        tooltip_bcolor_Hlayout.addWidget(self.tooltip_bcolor_check)

        tlw_bcolor1_Hlayout = QHBoxLayout()
        tlw_bcolor1 = QPushButton("TL Window Bg Color 1", self)
        self.tlw_bcolor1_check = QCheckBox("", self)
        self.tlw_bcolor1_check.setStyleSheet("QCheckBox::indicator"
                                           "{"
                                           f"background-color : {config['DEFAULT']['colorblockeven']};"
                                           "}")
        tlw_bcolor1_Hlayout.addWidget(tlw_bcolor1)
        tlw_bcolor1_Hlayout.addWidget(self.tlw_bcolor1_check)

        tlw_bcolor2_Hlayout = QHBoxLayout()
        tlw_bcolor2 = QPushButton("TL Window Bg Color 2", self)
        self.tlw_bcolor2_check = QCheckBox("", self)
        self.tlw_bcolor2_check.setStyleSheet("QCheckBox::indicator"
                                        "{"
                                        f"background-color : {config['DEFAULT']['colorblockodd']};"
                                        "}")
        tlw_bcolor2_Hlayout.addWidget(tlw_bcolor2)
        tlw_bcolor2_Hlayout.addWidget(self.tlw_bcolor2_check)

        kanjidict_kanji_color.clicked.connect(self._kanjidict_kanji_color_clicked)
        tooltip_color.clicked.connect(self._tooltip_color_clicked)
        tooltip_bcolor.clicked.connect(self._tooltip_bcolor_clicked)
        tlw_bcolor1.clicked.connect(self._tlw_bcolor1_clicked)
        tlw_bcolor2.clicked.connect(self._tlw_bcolor2r_clicked)
        self.color_layout.addWidget(colors)
        self.color_layout.addLayout(kanjidict_kanji_color_Hlayout)
        self.color_layout.addLayout(tooltip_color_Hlayout)
        self.color_layout.addLayout(tooltip_bcolor_Hlayout)
        self.color_layout.addLayout(tlw_bcolor1_Hlayout)
        self.color_layout.addLayout(tlw_bcolor2_Hlayout)

        # GENERAL
        self.general = QVBoxLayout()
        label = QLabel("General")
        label.setFont(F)
        label.setMaximumHeight(20)
        label.setAlignment(Qt.AlignmentFlag.AlignTop)

        G0_Hlayout = QHBoxLayout()
        G0_label = QLabel("Font size:")
        G0_label.setMaximumWidth(120)
        self.fsize = QSpinBox()
        self.fsize.setValue(int(config['DEFAULT']['fontsize']))
        self.fsize.setMaximum(32)
        self.fsize.setWrapping(True)
        self.fsize.setMaximumWidth(60)
        self.fsize.valueChanged.connect(self._set_font_size)
        G0_Hlayout.addWidget(G0_label)
        G0_Hlayout.addWidget(self.fsize)
        G0_Hlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        G_Hlayout = QHBoxLayout()
        G_label = QLabel("kanjidict font size:")
        G_label.setMaximumWidth(120)
        self.kanjidict_fsize = QSpinBox()
        self.kanjidict_fsize.setValue(int(config['DEFAULT']['kanjidictfontsize']))
        self.kanjidict_fsize.setMaximum(32)
        self.kanjidict_fsize.setWrapping(True)
        self.kanjidict_fsize.setMaximumWidth(60)
        self.kanjidict_fsize.valueChanged.connect(self._set_kanjidict_font_size)
        G_Hlayout.addWidget(G_label)
        G_Hlayout.addWidget(self.kanjidict_fsize)
        G_Hlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        G1_Hlayout = QHBoxLayout()
        G1_label = QLabel("translation fontsize:")
        G1_label.setMaximumWidth(120)
        self.ToolTip_fsize = QSpinBox()
        self.ToolTip_fsize.setValue(int(config['DEFAULT']['translationtooltipfontsize']))
        self.ToolTip_fsize.setMaximum(32)
        self.ToolTip_fsize.setWrapping(True)
        self.ToolTip_fsize.setMaximumWidth(60)
        self.ToolTip_fsize.valueChanged.connect(self._set_ToolTip_font_size)
        G1_Hlayout.addWidget(G1_label)
        G1_Hlayout.addWidget(self.ToolTip_fsize)
        G1_Hlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        G2_Hlayout = QHBoxLayout()
        G2_label = QLabel("Preprocess threshold:")
        G2_label.setMaximumWidth(120)
        self.Threshold_size = QSpinBox()
        self.Threshold_size.setMaximum(255)
        self.Threshold_size.setValue(int(config['DEFAULT']['preprocessthreshold']))
        self.Threshold_size.setWrapping(True)
        self.Threshold_size.setMaximumWidth(60)
        self.Threshold_size.valueChanged.connect(self._set_Threshold_size)
        G2_Hlayout.addWidget(G2_label)
        G2_Hlayout.addWidget(self.Threshold_size)
        G2_Hlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        G3_Hlayout = QHBoxLayout()
        G3_label = QLabel("Translator:")
        G3_label.setMaximumWidth(120)
        # Translators Dropdown
        self.tls_list = tss.translators_pool
        self.tl_combobox = QComboBox()
        self.tl_combobox.setMaximumHeight(30)
        self.tl_combobox.setMaximumWidth(100)
        [self.tl_combobox.addItem(tl) for tl in self.tls_list]
        if config['DEFAULT']['Translator'] == '':
            self.tl_combobox.setPlaceholderText("--Translators--")
        else:
            self.tl_combobox.setCurrentIndex(self.tls_list.index(config['DEFAULT']['Translator']))
        self.tl_combobox.activated.connect(self._set_Translator)
        G3_Hlayout.addWidget(G3_label)
        G3_Hlayout.addWidget(self.tl_combobox)
        G3_Hlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # GOOGLE VISION OCR
        G_ocr_Hlayout = QHBoxLayout()
        G_ocr_creds_btn = QPushButton("Google Vision Credentials:", self)
        self.G_ocr_creds_path = QLineEdit()
        self.G_ocr_creds_path.setText(config['DEFAULT']['G_ocr'])
        self.G_ocr_creds_path.setReadOnly(True)
        G_ocr_creds_btn.clicked.connect(self._select_googleVision_creds)
        G_ocr_Hlayout.addWidget(G_ocr_creds_btn)
        G_ocr_Hlayout.addWidget(self.G_ocr_creds_path)
        G_ocr_Hlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        G_ocr_Hlayout.stretch(2)

        self.general.addWidget(label)
        self.general.addLayout(G0_Hlayout)
        self.general.addLayout(G_Hlayout)
        self.general.addLayout(G1_Hlayout)
        self.general.addLayout(G2_Hlayout)
        self.general.addLayout(G3_Hlayout)

        self.layout.addLayout(self.general, 0, 0)
        self.layout.addLayout(self.color_layout, 0, 1)
        self.layout.addLayout(G_ocr_Hlayout, 1, 0)
        self.layout.addWidget(self.buttonBox, 2, 1)
        self.setLayout(self.layout)

    def _select_googleVision_creds(self):
        fname = QFileDialog.getOpenFileName(self, 'Select credential file',
                                            'c:\\', "JSON file (*.json)")
        file_path = fname[0]
        self.G_ocr_creds_path.setText(file_path)
        config.set('DEFAULT', 'G_ocr', str(file_path))
        self.G_ocr_creds_path.setText(config['DEFAULT']['G_ocr'])
        print(file_path)

    def _set_Translator(self):
        self.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(True)
        val = self.tl_combobox.currentText()
        config.set('DEFAULT', 'translator', str(val))

    def _set_Threshold_size(self):
        self.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(True)
        val = self.Threshold_size.value()
        config.set('DEFAULT', 'preprocessthreshold', str(val))

    def _set_ToolTip_font_size(self):
        self.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(True)
        val = self.ToolTip_fsize.value()
        config.set('DEFAULT', 'translationtooltipfontsize', str(val))

    def _set_kanjidict_font_size(self):
        self.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(True)
        val = self.kanjidict_fsize.value()
        config.set('DEFAULT', 'kanjidictfontsize', str(val))

    def _set_font_size(self):
        self.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(True)
        val = self.fsize.value()
        config.set('DEFAULT', 'fontsize', str(val))

    def _set_color(self, ckey):
        self.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(True)
        color = QColorDialog()
        getcolor = color.getColor()
        selected_color = getcolor.name()
        config.set('DEFAULT', ckey, selected_color)

    def _kanjidict_kanji_color_clicked(self):
        self._set_color('kanjidictkanjicolor')

    def _tooltip_color_clicked(self):
        self._set_color('ToolTipFontColor')

    def _tooltip_bcolor_clicked(self):
        self._set_color('tooltipbackgroundcolor')

    def _tlw_bcolor1_clicked(self):
        self._set_color('colorblockeven')

    def _tlw_bcolor2r_clicked(self):
        self._set_color('colorblockodd')

    def Save(self):
        # This flag seems hacky rethink..
        config.set('DEFAULT', 'changeflag', 'True')

        with open(constants.CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        self.tooltip_color_check.setStyleSheet("QCheckBox::indicator"
                                               "{"
                                               f"background-color : {config['DEFAULT']['kanjidictkanjicolor']};"
                                               "}")
        self.tooltip_color_check.setStyleSheet("QCheckBox::indicator"
                                               "{"
                                               f"background-color : {config['DEFAULT']['tooltipfontcolor']};"
                                               "}")
        self.tooltip_bcolor_check.setStyleSheet("QCheckBox::indicator"
                                                "{"
                                                f"background-color : {config['DEFAULT']['tooltipbackgroundcolor']};"
                                                "}")
        self.tlw_bcolor1_check.setStyleSheet("QCheckBox::indicator"
                                             "{"
                                             f"background-color : {config['DEFAULT']['colorblockeven']};"
                                             "}")
        self.tlw_bcolor2_check.setStyleSheet("QCheckBox::indicator"
                                             "{"
                                             f"background-color : {config['DEFAULT']['colorblockodd']};"
                                             "}")
        self.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(False)
        self.update()

    def Close(self):
        self.close()
