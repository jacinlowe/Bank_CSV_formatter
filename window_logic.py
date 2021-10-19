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

from QtWidgetBuilder import Button, Status, InputLine, layout_cls, LayoutEnum, Checkbox


class WindowInsert(QWidget):
    def __init__(self):
        super().__init__()

        self.setup()

    def setup(self):
        # Quit button#
        self.btn_quit = Button("Force Quit", QApplication.instance().quit, (100, 20))

        # call function button #
        btn_input_csv = Button("Open CSV File", self.select_csv_files)

        # Run script function
        btn_run_script = Button("run script", self.run_script, (200, 30))

        # set Satus label
        self.label = Status()

        # set up text edit
        self.csv_select = InputLine("Input CSV File")

        # Destination selector
        self.csv_destination = InputLine("Select CSV File Destination")

        # destination Button
        btn_dest_out = Button("Select Destination", self.select_destination)

        # setup HLAYOUT for top bar

        top_Hbox = layout_cls(LayoutEnum.HORIZONTAL)
        top_Hbox.addWidgets([self.label, self.btn_quit])

        # setup hlayout for fileinput
        csv_hbox_input = layout_cls(LayoutEnum.HORIZONTAL)
        csv_hbox_input.addWidgets([self.csv_select, btn_input_csv])

        # setup Hlayout for Destination
        csv_hbox_dest = layout_cls(LayoutEnum.HORIZONTAL)
        csv_hbox_dest.addWidgets([self.csv_destination, btn_dest_out])

        # Toggle DARK MODE push button0
        self.btn_darkMode = QPushButton("Dark Mode")
        self.btn_darkMode.setCheckable(True)
        self.btn_darkMode.setChecked(False)
        # self.btn_darkMode.clicked.connect(self.toggle_dark_theme)

        # Toggle Save xl files #
        self.btn_save_xl = Checkbox("Save Excel files", self.save_excel_files_checked)

        self.save_xl = False

        # Delete Original File when complete
        self.btn_delete_orig_file = Checkbox(
            "Delete Original File when done!", self.del_orig_files_checked
        )

        # Args layout
        args_hbox_btn_layout = layout_cls(LayoutEnum.HORIZONTAL)
        args_hbox_btn_layout.addWidgets([self.btn_save_xl, self.btn_delete_orig_file])
        # setup VLayout for all items
        vlayout = QVBoxLayout()
        vlayout.addLayout(top_Hbox)
        vlayout.setContentsMargins(15, 0, 15, 0)

        vlayout.addLayout(csv_hbox_input)
        vlayout.addLayout(csv_hbox_dest)
        vlayout.addLayout(args_hbox_btn_layout)

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

    def select_csv_files(self):
        file_v = Bank_functions.CsvFunctions.get_file(self)
        # file_v = type(file_v)
        self.file_v = file_v
        self.label.updateText("Successfully added Files")

        # add file to text window
        self.csv_select.updateText(file_v)

    def select_destination(self):
        dest = Bank_functions.CsvFunctions.get_dest(self)
        self.csv_destination.setText(dest)
        self.label.updateText("Destination set!")

    def run_script(self):
        process = Bank_functions.CsvConverter(self.file_v, self.csv_destination.text())
        self.label.updateText("Running Conversion")
        end_message = process.run_Main(
            save_xl=self.save_xl, del_orig_file=self.del_orig_file
        )
        self.label.updateText(end_message, "green")
        # self.label.setText(self.working_html + end_message)

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
