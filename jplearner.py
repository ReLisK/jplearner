import sys
import time
import logging
import configparser

from BlurWindow.blurWindow import blur
from PIL import ImageGrab
from PyQt6.QtCore import (
    Qt,
    QPoint,
    QRect,
    QSize,
)
from PyQt6.QtGui import (
    QPainter,
    QBrush,
    QCloseEvent,
    QAction,
    QIcon,
)
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QProgressBar,
)

import constants
import translator
import translators as tss
import utils
from settingswidget import SettingsWindow

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read(constants.CONFIG_FILE)


class DrawTranslationBox(QWidget):
    def __init__(self, screen_size):
        super().__init__(parent=None)
        # screenshot = utils.get_snippet(
        #     constants.SCREENSHOTS, constants.SCREENSHOTS_NAME
        # )
        self.screen_size = screen_size
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        blur(self.winId())
        # stylesheet = f"background-image: url({screenshot})"
        # self.setStyleSheet(stylesheet)
        # self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.setWindowTitle("Draw Translation Box")

        self.begin = QPoint()
        self.end = QPoint()

    def paintEvent(self, event):
        qp = QPainter(self)
        br = QBrush(Qt.BrushStyle.Dense7Pattern)
        qp.setBrush(br)
        qp.drawRect(QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()

    def closeEvent(self, a0: QCloseEvent):
        # Might need to use this to handle if user closes window before saving or anything.
        pass


class MainWindow(QMainWindow):
    def __init__(self, screen_size):
        super().__init__(parent=None)
        self.screen_size = screen_size
        self.setWindowTitle(constants.MAIN_WINDOW_TITLE)
        self.setWindowIcon(QIcon("assets/mainIcon32.png"))
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        window = QWidget()

        # Holds the full main layout including kanjidict
        self.main_Pfull_layout = QVBoxLayout()
        self.main_full_layout = QHBoxLayout()

        # Kanjidict in a scroll area hide/unhide from menu bar
        self.scroll_kanjidict = QScrollArea()
        self.dict_widget = QWidget()
        self.scroll_text_box = QVBoxLayout()
        # for i in range(1, 50):
        #     object = QLabel("TextLabel")
        #     self.scroll_text_box.addWidget(object)
        self.dict_widget.setLayout(self.scroll_text_box)
        # Scroll Area Properties
        self.scroll_bar = self.scroll_kanjidict.verticalScrollBar()
        # connect to _onrangechanged to keep window scrolled down.
        self.scroll_bar.rangeChanged.connect(self._onRangeChanged)
        self.scroll_kanjidict.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.scroll_kanjidict.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_kanjidict.setWidgetResizable(True)
        self.scroll_kanjidict.setMaximumWidth(800)
        self.scroll_kanjidict.setMinimumWidth(500)
        self.scroll_kanjidict.setWidget(self.dict_widget)

        self.layout = QVBoxLayout()
        self.instructions = QLabel(
            "<h1>Let's start with drawing the Translation Box!</h1>"
        )
        self.layout.addWidget(self.instructions)

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
        self.layout.addWidget(self.tl_combobox)

        # Radio buttons
        self.radio_layout = QHBoxLayout()
        self.radio_btn_grp = QButtonGroup()
        self.jph = QRadioButton("JP Horizontal", self)
        self.jph.setChecked(True)
        self.radio_btn_grp.addButton(self.jph)
        self.radio_layout.addWidget(self.jph)
        self.jpv = QRadioButton("JP Vertical", self)
        self.radio_btn_grp.addButton(self.jpv)
        self.radio_layout.addWidget(self.jpv)
        self.layout.addLayout(self.radio_layout)

        self.draw_box_button = QPushButton("Draw Box")
        self.draw_box_button.clicked.connect(self._draw_box_clicked)
        self.layout.addWidget(self.draw_box_button)
        self.instructions.setMaximumHeight(30)
        self.jph.setMaximumHeight(30)
        self.jpv.setMaximumHeight(30)

        # PROGRESS BAR
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.pbar.hide()

        self.main_full_layout.addWidget(self.scroll_kanjidict)
        self.main_full_layout.addLayout(self.layout)
        self.scroll_kanjidict.hide()

        self.main_Pfull_layout.addLayout(self.main_full_layout)
        self.main_Pfull_layout.addWidget(self.pbar)
        window.setLayout(self.main_Pfull_layout)
        self.setCentralWidget(window)



        self.tl = None
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

    def _init(self):
        self.DrawTranslationBoxWindow = DrawTranslationBox(self.screen_size)

    def _createMenu(self):
        # File - Settings
        # View - hide/unhide dict
        # tools - Anki, thresh
        fileMenu = self.menuBar().addMenu("&File")
        ViewMenu = self.menuBar().addMenu("&View")
        ToolMenu = self.menuBar().addMenu("&Tools")
        settings_action = QAction(QIcon("./assets/setting.png"), "&Settings", self)
        settings_action.triggered.connect(self.settings)
        kanji_dict_action = QAction("&Kanji Dict", self)
        kanji_dict_action.setCheckable(True)
        kanji_dict_action.toggled.connect(self._display_kanjidict)
        self.preprocess_action = QAction("Preprocess", self)
        self.preprocess_action.setCheckable(True)
        anki_action = QAction("Anki", self)
        fileMenu.addAction(settings_action)
        ViewMenu.addAction(kanji_dict_action)
        ToolMenu.addAction(self.preprocess_action)
        ToolMenu.addAction(anki_action)

    def _createToolBar(self):
        pass

    def _createStatusBar(self):
        pass

    def settings(self):
        dlg = SettingsWindow()
        dlg.exec()
        print(config['DEFAULT']['Translator'])
        self.tl_combobox.setCurrentIndex(self.tls_list.index(config['DEFAULT']['Translator']))
        self.tl_combobox.setCurrentText(config['DEFAULT']['Translator'])

    def _draw_box_clicked(self):
        if self.tl_combobox.currentText() == "":
            utils.qt_alert("You must select a translator...")
            return
        self._init()
        self.instructions.setText(
            "Use your mouse on the screen to click and drag a box around the translation area"
        )
        initial_window_width = self.frameGeometry().width()
        initial_window_height = self.frameGeometry().height()
        desktop_width = self.screen_size.width()

        # Move window to top right corner - not perfect
        x = desktop_width - initial_window_width - 205
        y = 100
        self.setGeometry(x, y, initial_window_width, initial_window_height)
        self.DrawTranslationBoxWindow.showMaximized()
        # self.draw_box_button.deleteLater()
        if not hasattr(self, "save_tl_box_button"):
            self.save_tl_box_button = QPushButton("Save Box")
            self.layout.addWidget(self.save_tl_box_button)
        self.save_tl_box_button.show()
        self.save_tl_box_button.clicked.connect(self._save_tl_box_button)

    def _save_tl_box_button(self):
        # Get box coordinates for Translator
        x = self.DrawTranslationBoxWindow.begin.x()
        y = self.DrawTranslationBoxWindow.begin.y()
        x1 = self.DrawTranslationBoxWindow.end.x()
        y1 = self.DrawTranslationBoxWindow.end.y()
        self.coordinates = (x, y, x1, y1)
        self.DrawTranslationBoxWindow.close()
        self.DrawTranslationBoxWindow.deleteLater()

        self.save_tl_box_button.close()
        self.instructions.setText("See translations below:")

        # Sleep because it needs a second to get paint off window before taking pic
        time.sleep(0.3)
        # Instantiate translator
        if self.tl is None:
            self.tl = translator.Translator(mainwindow=self)
        self.tl.coordinates = self.coordinates

    def _tl_snap_button(self):
        self.tl.coordinates = self.coordinates
        self.pbar.show()
        self.tl.run()
        self.pbar.setValue(100)
        self.pbar.close()

    def _onRangeChanged(self):
        # Set scrollbar to bottom whenever updated.
        self.scroll_bar.setSliderPosition(self.scroll_bar.maximum())

    def _display_kanjidict(self):
        if self.scroll_kanjidict.isVisible():
            self.scroll_kanjidict.hide()
        else:
            self.scroll_kanjidict.show()


def main():
    app = QApplication([])
    screen = app.primaryScreen()
    print("Screen: %s" % screen.name())
    screen_size = screen.size()
    print("Size: %d x %d" % (screen_size.width(), screen_size.height()))
    window = MainWindow(screen_size)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
