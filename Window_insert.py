"""
            This Script contains all the widgets and buttons for app

"""

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QMessageBox,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QCheckBox,
)
from PySide6.QtGui import QCloseEvent, QPalette, QColor
from PySide6.QtCore import Qt, Slot
import Bank_functions
from time import sleep


class WindowInsert(QWidget):
    def __init__(self):
        super().__init__()

        self.setup()

    def setup(self):
        # Quit button#
        self.btn_quit = QPushButton("Force Quit", self)
        self.btn_quit.clicked.connect(QApplication.instance().quit)
        self.btn_quit.resize(self.btn_quit.sizeHint())
        self.btn_quit.setMaximumSize(100, 20)
        # self.btn_quit.move(90, 100)

        # call function button #
        btn_test_function = QPushButton("Open CSV File", self)
        btn_test_function.clicked.connect(self.csv_gotten)
        btn_test_function.resize(btn_test_function.sizeHint())

        # Run script function
        btn_run_script = QPushButton("run script", self)
        btn_run_script.clicked.connect(self.run_script)
        btn_run_script.resize(btn_run_script.sizeHint())

        # set Satus label
        self.status = "Status: "
        self.label = QLabel(self)
        self.s_html = f"<font color=red size=5> {self.status} </font>"
        self.label.setText(self.s_html + "No CSV File added!")
        # self.label.move(10, 100)

        # set up text edit
        self.csv_select = QLineEdit()
        self.csv_select.setPlaceholderText("Input CSV File")
        self.csv_select.setContentsMargins(0, 0, 0, 0)
        self.csv_select.resize(self.csv_select.sizeHint())

        # setup HLAYOUT for top bar

        top_Hbox = QHBoxLayout()
        top_Hbox.addWidget(self.label)
        top_Hbox.addWidget(self.btn_quit)

        # setup hlayout for fileinput
        csv_hbox = QHBoxLayout()
        csv_hbox.addWidget(self.csv_select)
        csv_hbox.addWidget(btn_test_function)

        # Toggle DARK MODE push button0
        self.btn_darkMode = QPushButton("Dark Mode")
        self.btn_darkMode.setCheckable(True)
        self.btn_darkMode.setChecked(True)
        # self.btn_darkMode.clicked.connect(self.toggle_dark_theme)

        # Toggle Save xl files #
        self.btn_save_xl = QCheckBox("Save Excel files")
        self.btn_save_xl.setCheckable(True)
        self.btn_save_xl.setChecked(False)
        self.save_xl = False
        self.btn_save_xl.clicked.connect(self.save_excel_files_checked)

        # Delete Original File when complete
        self.btn_delete_orig_file = QCheckBox("Delete Original File when done!")
        self.btn_delete_orig_file.setCheckable(True)
        self.del_orig_file = False
        self.btn_delete_orig_file.clicked.connect(self.del_orig_files_checked)

        # setup VLayout for all items
        vlayout = QVBoxLayout()
        vlayout.addLayout(top_Hbox)
        vlayout.setContentsMargins(15, 0, 15, 100)
        vlayout.addLayout(csv_hbox)
        vlayout.addWidget(self.btn_save_xl)
        vlayout.addWidget(self.btn_delete_orig_file)

        vlayout.addWidget(btn_run_script)
        vlayout.addWidget(self.btn_darkMode)

        # ---- Theme Set up ----- #
        # # Dark Palette (found on github, couldn't track the original author)

        self.default_palette = QPalette()
        self.dark_palette = QPalette()

        self.dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        self.dark_palette.setColor(QPalette.WindowText, Qt.white)
        self.dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        self.dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        self.dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        self.dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        self.dark_palette.setColor(QPalette.Text, Qt.white)
        self.dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        self.dark_palette.setColor(QPalette.ButtonText, Qt.white)
        self.dark_palette.setColor(QPalette.BrightText, Qt.red)
        self.dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        self.dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        self.dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.dark_palette.setColor(QPalette.PlaceholderText, Qt.lightGray)

        # Base geo
        self.setGeometry(100, 100, 500, 300)
        self.setWindowTitle("Butterfield Bank Statement Converter")
        self.setLayout(vlayout)
        self.setMinimumSize(300, 200)

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

    def csv_gotten(self):
        file_v = Bank_functions.CsvFunctions.get_file(self)
        # file_v = type(file_v)
        self.file_v = file_v
        self.added_html = f"<font color=green size=5> {self.status} </font>"
        self.label.setText(self.added_html + "Successfully added Files")
        self.label.adjustSize()
        # add file to text window
        self.csv_select.setText(file_v)

    def finishedHtml(self):

        self.finished_html = f"<font color=green size=5> {self.status} </font>"
        self.label.setText(self.finished_html + "Successfully Completed")
        self.label.adjustSize()

    def run_script(self):
        process = Bank_functions.CsvConverter(self.file_v)
        self.working_html = f"<font color=red size=5> {self.status} </font>"
        self.label.setText(self.working_html + "Running Conversion")
        self.label.adjustSize()
        end_message = process.run_Main(
            save_xl=self.save_xl, del_orig_file=self.del_orig_file
        )
        self.finishedHtml()
        self.label.setText(self.working_html + end_message)

    def save_excel_files_checked(self):
        if self.btn_save_xl.isChecked():
            self.save_xl = True
        else:
            pass

    def del_orig_files_checked(self):
        if self.btn_delete_orig_file.isChecked():
            self.del_orig_file = True
        else:
            pass

    # Toggle theme function
    @Slot()
    def toggle_dark_theme(self):
        if not self.btn_darkMode.isChecked():
            self.setPalette(self.dark_palette)
            self.btn_save_xl.colorCount()
        else:
            self.setPalette(self.default_palette)


def run():
    app = QApplication([])
    app.setStyle("Fusion")

    ex = WindowInsert()

    app.exec_()


if __name__ == "__main__":
    run()
