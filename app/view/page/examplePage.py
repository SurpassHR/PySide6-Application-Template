#coding: utf-8
from PySide6.QtWidgets import QFrame, QVBoxLayout

from ...widget.textAreaCard import TextAreaCard

class ExamplePage(QFrame):
    def __init__(self, text: str, window):
        super().__init__(window)
        self.setObjectName(text.replace(" ", "-"))

        # global variable
        self.window = window

        # create container
        self.container = QVBoxLayout()

        # create a widget card
        self.widgetCard = TextAreaCard(
            title="带输入区域的卡片组件。",
            desc="可以在输入区域输入文字。",
        )

        self.container.addWidget(self.widgetCard, 1)
        self.container.addStretch(1)

        self.setLayout(self.container)