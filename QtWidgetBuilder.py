from typing import Any, List, Optional, Tuple
from PySide6 import QtWidgets
from PySide6 import QtCore
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
from collections.abc import Callable
from enum import Enum, auto


class Button(QPushButton):
    def __init__(
        self,
        name: str,
        function: Callable[
            [],
        ],
        max_size: Tuple[int, int] = (100, 20),
    ) -> None:
        super().__init__(name)

        self.maxW = max_size[0]
        self.maxH = max_size[1]
        self.clicked.connect(function)
        self.resize(self.sizeHint())

        self.setMaximumSize(self.maxW, self.maxH)


class Status(QLabel):
    def __init__(
        self,
        text: str = " ",
    ) -> None:
        super().__init__(text)
        self.status = "Status: "
        self.s_html = f"<font color=red size=5> {self.status} </font>"
        self.setText(self.s_html + "No CSV File added!")
        self.setContentsMargins(0, 5, 0, 5)

    def updateText(self, text: str, color="red"):
        if color != "red":
            self._changeStatusColor(color)
        self.setText(f"{self.s_html} {text}")
        self.adjustSize()
        print(text)

    def _changeStatusColor(self, color):
        self.s_html = f"<font color={color} size=5>{self.status} </font>"


class InputLine(QLineEdit):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.setPlaceholderText(text)
        self.setContentsMargins(0, 5, 0, 5)
        self.resize(self.sizeHint())

    def updateText(self, text: str):
        self.setText(text)


# class Layout:
#     def addWidgets(self, widgets: List[Any]):
#         for widget in widgets:
#             self.addWidget(widget)


class LayoutEnum(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()


def layout_cls(type: LayoutEnum):
    if type == LayoutEnum.HORIZONTAL:
        properties = QHBoxLayout
    elif type == LayoutEnum.VERTICAL:
        properties = QVBoxLayout

    class Layout(properties):
        def addWidgets(self, widgets: List[Any]):
            for widget in widgets:
                self.addWidget(widget)

    return Layout()


class Checkbox(QCheckBox):
    def __init__(
        self,
        text: str,
        function: Callable[
            [],
        ],
        isCheckable: bool = True,
        isChecked: bool = False,
    ) -> None:
        super().__init__(text)
        self.setCheckable(isCheckable)
        self.setChecked(isChecked)
        self.clicked.connect(function)
