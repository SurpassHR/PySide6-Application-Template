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
        self.widgetCard1 = TextAreaCard(
            title="带输入区域的卡片组件。",
            desc="可以在输入区域输入文字。",
            parent=self,
        )
        self.widgetCard1.setMaximumHeight(100)
        self.widgetCard2 = TextAreaCard(
            title="带输入区域的卡片组件。",
            desc="可以在输入区域输入文字。",
            parent=self,
        )
        self.widgetCard2.setMaximumHeight(100)
        self.widgetCard3 = TextAreaCard(
            title="带输入区域的卡片组件。",
            desc="可以在输入区域输入文字。",
            parent=self,
        )
        self.widgetCard3.setMaximumHeight(100)

        self.container.addWidget(self.widgetCard1, 1)
        self.container.addWidget(self.widgetCard2, 1)
        self.container.addWidget(self.widgetCard3, 1)
        self.container.addStretch(1)

        self.setLayout(self.container)