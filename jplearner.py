import sys
import time

from BlurWindow.blurWindow import blur
from PIL import ImageGrab
from PyQt6 import QtCore, QtGui
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
    QSizePolicy,
)

import constants
import translator
import utils


class DrawTranslationBox(QWidget):
    def __init__(self, screen_size):
        super().__init__(parent=None)
        screenshot = utils.get_snippet(
            constants.SCREENSHOTS, constants.SCREENSHOTS_NAME
        )
        self.screen_size = screen_size
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        blur(self.winId())
        # stylesheet = f"background-image: url({screenshot})"
        # self.setStyleSheet(stylesheet)
        # self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.setWindowTitle("Draw Translation Box")

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        br = QtGui.QBrush(QtCore.Qt.BrushStyle.Dense7Pattern)
        qp.setBrush(br)
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()


class MainWindow(QMainWindow):
    def __init__(self, screen_size):
        super().__init__(parent=None)
        self.screen_size = screen_size
        self.setWindowTitle(constants.MAIN_WINDOW_TITLE)
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        window = QWidget()
        self.layout = QVBoxLayout()
        self.instructions = QLabel(
            "<h1>Let's start with drawing the Translation Box!</h1>"
        )
        self.layout.addWidget(self.instructions)

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
        window.setLayout(self.layout)
        self.setCentralWidget(window)

        self.tl = None
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

    def _init(self):
        self.DrawTranslationBoxWindow = DrawTranslationBox(self.screen_size)

    def _createMenu(self):
        pass

    def _createToolBar(self):
        pass

    def _createStatusBar(self):
        pass

    def _draw_box_clicked(self):
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
        self.tl.translate()


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
