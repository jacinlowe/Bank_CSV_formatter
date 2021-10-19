"""
            This is the Main window. The features and buttons are then called from the Qwidget. I did this because i
            needed to access some functions and methods of a QMainwindow.

"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLayout,
    QApplication,
    QMessageBox,
    QMenu,
    QLabel,
    QPushButton,
)
from PySide6.QtGui import QCloseEvent, QColor
from PySide6.QtCore import QPropertyAnimation, Property
from window_logic import WindowInsert


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)

        self.main_widget = QWidget(self)

        self.form_widget = WindowInsert()
        # This is my UI widget

        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.sizeConstraint = QLayout.SetDefaultConstraint
        self.main_layout.addWidget(self.form_widget)
        # form_widget has its own main_widget where I put all other widgets onto

        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)
        self.setWindowTitle(self.form_widget.windowTitle())
        self.setGeometry(self.form_widget.geometry())

        # self.form_widget.btn_quit.clicked.connect(QApplication.instance().quit)

        # ---- set Palette ---- #
        self.form_widget.btn_darkMode.clicked.connect(self.set_Palette)
        self.init_ui()

    def init_ui(self):

        # ---- Set up Top menuBar ---- #
        menubar = self.menuBar()

        # --- Set File item Top Menu --- #
        file_menu = menubar.addMenu("File")

        # --- Quit item -- #
        f_quit_action = file_menu.addAction("Quit")
        f_quit_action.setStatusTip("Close Program")
        f_quit_action.triggered.connect(QApplication.instance().quit)

        # --- Help menu --- #
        help_menu = menubar.addMenu("Help")
        ab_action = help_menu.addAction("About")

        self.statusBar().showMessage("Testing")

        self.show()

    def closeEvent(self, event: QCloseEvent):
        reply = QMessageBox.question(
            self,
            "Message",
            "Are you sure you want to Quit",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def set_Palette(self):
        if self.form_widget.btn_darkMode.isChecked():
            self.setPalette(self.form_widget.dark_palette)
        else:
            self.setPalette(self.form_widget.default_palette)


def run():
    app = QApplication([])
    app.setStyle("Fusion")

    ex = MyMainWindow()
    ex.show()
    app.exec_()


if __name__ == "__main__":
    run()
