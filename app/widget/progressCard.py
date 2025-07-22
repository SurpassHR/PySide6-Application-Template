# coding:utf-8
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPainter, QFont, QColor, QPen
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout

from qfluentwidgets import (
    CardWidget,
    IconWidget,
    ToolButton,
    FluentIcon,
    BodyLabel,
    CaptionLabel,
    ProgressBar,
    ImageLabel,
    setFont,
    MessageBoxBase,
    SubtitleLabel,
    CheckBox,
    ToolTipFilter,
    InfoLevel,
    DotInfoBadge,
    MessageBox,
    isDarkTheme,
    themeColor,
)

from ..common.uiFunctionBase import uiFuncBase


class TaskCardBase(CardWidget):
    """Task card base class"""

    checkedChanged = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.checkBox = CheckBox()
        self.checkBox.setFixedSize(23, 23)
        self.setSelectionMode(False)

        self.checkBox.stateChanged.connect(self._onCheckedChanged)

    def setSelectionMode(self, enter: bool):
        self.isSelectionMode = enter
        self.checkBox.setVisible(enter)
        if not enter:
            self.checkBox.setChecked(False)

        self.update()

    def isChecked(self):
        return self.checkBox.isChecked()

    def setChecked(self, checked):
        if checked == self.isChecked():
            return

        self.checkBox.setChecked(checked)
        self.update()

    def removeTask(self, deleteFile=False):
        raise NotImplementedError

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        if self.isSelectionMode:
            self.setChecked(not self.isChecked())
        else:
            self.setSelectionMode(True)
            self.setChecked(True)

    def _onDeleteButtonClicked(self):
        w = DeleteTaskDialog(self.window(), deleteOnClose=False)
        w.deleteFileCheckBox.setChecked(False)

        if w.exec():
            self.removeTask(w.deleteFileCheckBox.isChecked())

        w.deleteLater()

    def _onCheckedChanged(self):
        self.setChecked(self.checkBox.isChecked())
        self.checkedChanged.emit(self.checkBox.isChecked())
        self.update()

    def paintEvent(self, e):
        if not (self.isSelectionMode and self.isChecked()):
            return super().paintEvent(e)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        r = float(self.getBorderRadius())
        painter.setPen(QPen(themeColor(), 2))
        painter.setBrush(QColor(255, 255, 255, 15) if isDarkTheme() else QColor(0, 0, 0, 8))
        painter.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), r, r)


class SuccessTaskCard(TaskCardBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.infoLayout = QHBoxLayout()

        self.imageLabel = ImageLabel(":/app/images/DefaultCover.jpg")
        self.fileNameLabel = BodyLabel("Default Task Name")

        self.createTimeIcon = IconWidget(FluentIcon.DATE_TIME)
        self.createTimeLabel = CaptionLabel("2000-05-30 00:00:00")
        self.sizeIcon = IconWidget(FluentIcon.BOOK_SHELF)
        self.sizeLabel = CaptionLabel("16GB")

        self.redownloadButton = ToolButton(FluentIcon.UPDATE)
        self.openFolderButton = ToolButton(FluentIcon.FOLDER)
        self.deleteButton = ToolButton(FluentIcon.DELETE)

        self._initWidget()

    def _initWidget(self):
        self.imageLabel.setScaledSize(QSize(112, 63))
        self.imageLabel.setBorderRadius(4, 4, 4, 4)
        self.createTimeIcon.setFixedSize(16, 16)
        self.sizeIcon.setFixedSize(16, 16)

        self.redownloadButton.setToolTip(self.tr("Restart"))
        self.redownloadButton.setToolTipDuration(3000)
        self.redownloadButton.installEventFilter(ToolTipFilter(self.redownloadButton))
        self.openFolderButton.setToolTip(self.tr("Show in folder"))
        self.openFolderButton.setToolTipDuration(3000)
        self.openFolderButton.installEventFilter(ToolTipFilter(self.openFolderButton))
        self.deleteButton.setToolTip(self.tr("Remove task"))
        self.deleteButton.setToolTipDuration(3000)
        self.deleteButton.installEventFilter(ToolTipFilter(self.deleteButton))

        setFont(self.fileNameLabel, 18, QFont.Weight.Bold)
        self.fileNameLabel.setWordWrap(True)

        self._initLayout()
        self._connectSignalToSlot()

    def _initLayout(self):
        self.hBoxLayout.setContentsMargins(20, 11, 20, 11)
        self.hBoxLayout.addWidget(self.checkBox)
        self.hBoxLayout.addSpacing(5)
        self.hBoxLayout.addWidget(self.imageLabel)
        self.hBoxLayout.addSpacing(5)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.hBoxLayout.addSpacing(20)
        self.hBoxLayout.addWidget(self.redownloadButton)
        self.hBoxLayout.addWidget(self.openFolderButton)
        self.hBoxLayout.addWidget(self.deleteButton)

        self.vBoxLayout.setSpacing(5)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.fileNameLabel)
        self.vBoxLayout.addLayout(self.infoLayout)

        self.infoLayout.setContentsMargins(0, 0, 0, 0)
        self.infoLayout.setSpacing(3)
        self.infoLayout.addWidget(self.createTimeIcon)
        self.infoLayout.addWidget(self.createTimeLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.infoLayout.addSpacing(8)
        self.infoLayout.addWidget(self.sizeIcon)
        self.infoLayout.addWidget(self.sizeLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.infoLayout.addStretch(1)

    def updateCover(self):
        # self.imageLabel.setImage(str(self.task.coverPath))
        self.imageLabel.setScaledSize(QSize(112, 63))

    def _onOpenButtonClicked(self):
        return

    def removeTask(self, deleteFile=False):
        return

    def redownload(self):
        return

    def _connectSignalToSlot(self):
        self.openFolderButton.clicked.connect(self._onOpenButtonClicked)
        self.deleteButton.clicked.connect(self._onDeleteButtonClicked)
        self.redownloadButton.clicked.connect(self.redownload)


class FailedTaskCard(TaskCardBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.infoLayout = QHBoxLayout()

        self.imageLabel = ImageLabel()
        self.fileNameLabel = BodyLabel("Default Task Name")

        self.createTimeIcon = IconWidget(FluentIcon.DATE_TIME)
        self.createTimeLabel = CaptionLabel("2000-05-30 00:00:00")
        self.sizeIcon = IconWidget(FluentIcon.BOOK_SHELF)
        self.sizeLabel = CaptionLabel("16GB")

        self.redownloadButton = ToolButton(FluentIcon.UPDATE)
        self.logButton = ToolButton(FluentIcon.COMMAND_PROMPT)
        self.deleteButton = ToolButton(FluentIcon.DELETE)

        self._initWidget()

    def _initWidget(self):
        # self.imageLabel.setImage(QFileIconProvider().icon(QFileInfo(self.task.videoPath)).pixmap(32, 32))
        self.createTimeIcon.setFixedSize(16, 16)
        self.sizeIcon.setFixedSize(16, 16)

        self.redownloadButton.setToolTip(self.tr("Restart"))
        self.redownloadButton.setToolTipDuration(3000)
        self.redownloadButton.installEventFilter(ToolTipFilter(self.redownloadButton))

        self.logButton.setToolTip(self.tr("View log"))
        self.logButton.setToolTipDuration(3000)
        self.logButton.installEventFilter(ToolTipFilter(self.logButton))

        setFont(self.fileNameLabel, 18, QFont.Weight.Bold)
        self.fileNameLabel.setWordWrap(True)

        self._initLayout()
        self._connectSignalToSlot()

    def _initLayout(self):
        self.hBoxLayout.setContentsMargins(20, 11, 20, 11)
        self.hBoxLayout.addWidget(self.checkBox)
        self.hBoxLayout.addSpacing(5)
        self.hBoxLayout.addWidget(self.imageLabel)
        self.hBoxLayout.addSpacing(5)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.hBoxLayout.addSpacing(20)
        self.hBoxLayout.addWidget(self.redownloadButton)
        self.hBoxLayout.addWidget(self.logButton)
        self.hBoxLayout.addWidget(self.deleteButton)

        self.vBoxLayout.setSpacing(5)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.fileNameLabel)
        self.vBoxLayout.addLayout(self.infoLayout)

        self.infoLayout.setContentsMargins(0, 0, 0, 0)
        self.infoLayout.setSpacing(3)
        self.infoLayout.addWidget(self.createTimeIcon)
        self.infoLayout.addWidget(self.createTimeLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.infoLayout.addSpacing(8)
        self.infoLayout.addWidget(self.sizeIcon)
        self.infoLayout.addWidget(self.sizeLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.infoLayout.addStretch(1)

    def _onLogButtonClicked(self):
        uiFuncBase.uiOpenURL("https://www.baidu.com")

    def removeTask(self, deleteFile=False):
        return

    def redownload(self):
        return

    def _connectSignalToSlot(self):
        self.logButton.clicked.connect(self._onLogButtonClicked)
        self.deleteButton.clicked.connect(self._onDeleteButtonClicked)
        self.redownloadButton.clicked.connect(self.redownload)


class DeleteTaskDialog(MessageBoxBase):
    def __init__(self, parent=None, showCheckBox=True, deleteOnClose=True):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(self.tr("Delete task"), self)
        self.contentLabel = BodyLabel(self.tr("Are you sure to delete this task?"), self)
        self.deleteFileCheckBox = CheckBox(self.tr("Remove file"), self)

        self.deleteFileCheckBox.setVisible(showCheckBox)

        if deleteOnClose:
            self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

        self._initWidgets()

    def _initWidgets(self):
        self.deleteFileCheckBox.setChecked(True)
        self.widget.setMinimumWidth(330)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.titleLabel)
        layout.addSpacing(12)
        layout.addWidget(self.contentLabel)
        layout.addSpacing(10)
        layout.addWidget(self.deleteFileCheckBox)
        self.viewLayout.addLayout(layout)


class LiveDownloadingTaskCard(TaskCardBase):
    """Live Downloading Task card"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.infoLayout = QHBoxLayout()

        self.imageLabel = ImageLabel()
        self.fileNameLabel = BodyLabel("Defalt Task Name")
        self.progressBar = ProgressBar()

        self.speedIcon = IconWidget(FluentIcon.SPEED_HIGH)
        self.speedLabel = CaptionLabel("0MB/s")
        self.timeIcon = IconWidget(FluentIcon.STOP_WATCH)
        self.timeLabel = CaptionLabel("00m00s/00m00s")
        self.statusIcon = DotInfoBadge(self, InfoLevel.SUCCESS)
        self.statusLabel = CaptionLabel(self.tr("Recording"))

        self.openFolderButton = ToolButton(FluentIcon.FOLDER)
        self.deleteButton = ToolButton(FluentIcon.DELETE)
        self.stopButton = ToolButton(FluentIcon.ACCEPT)

        self._initWidget()

    def _initWidget(self):
        # self.imageLabel.setImage(QFileIconProvider().icon(QFileInfo(self.task.videoPath)).pixmap(32, 32))
        self.speedIcon.setFixedSize(16, 16)
        self.timeIcon.setFixedSize(16, 16)
        self.statusIcon.setFixedSize(10, 10)

        self.openFolderButton.setToolTip(self.tr("Show in folder"))
        self.openFolderButton.setToolTipDuration(3000)
        self.openFolderButton.installEventFilter(ToolTipFilter(self.openFolderButton))
        self.stopButton.setToolTip(self.tr("Stop recording"))
        self.stopButton.setToolTipDuration(3000)
        self.stopButton.installEventFilter(ToolTipFilter(self.stopButton))
        self.deleteButton.setToolTip(self.tr("Remove task"))
        self.deleteButton.setToolTipDuration(3000)
        self.deleteButton.installEventFilter(ToolTipFilter(self.deleteButton))

        setFont(self.fileNameLabel, 18, QFont.Weight.Bold)
        self.fileNameLabel.setWordWrap(True)

        self._initLayout()
        self._connectSignalToSlot()

    def _initLayout(self):
        self.hBoxLayout.setContentsMargins(20, 11, 20, 11)
        self.hBoxLayout.addWidget(self.checkBox)
        self.hBoxLayout.addSpacing(5)
        self.hBoxLayout.addWidget(self.imageLabel)
        self.hBoxLayout.addSpacing(5)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.hBoxLayout.addSpacing(20)
        self.hBoxLayout.addWidget(self.openFolderButton)
        self.hBoxLayout.addWidget(self.stopButton)
        self.hBoxLayout.addWidget(self.deleteButton)

        self.vBoxLayout.setSpacing(5)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.fileNameLabel)
        self.vBoxLayout.addLayout(self.infoLayout)
        self.vBoxLayout.addWidget(self.progressBar)

        self.infoLayout.setContentsMargins(0, 0, 0, 0)
        self.infoLayout.setSpacing(3)
        self.infoLayout.addWidget(self.statusIcon, 0, Qt.AlignmentFlag.AlignVCenter)
        self.infoLayout.addWidget(self.statusLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.infoLayout.addSpacing(5)
        self.infoLayout.addWidget(self.speedIcon, 0, Qt.AlignmentFlag.AlignVCenter)
        self.infoLayout.addWidget(self.speedLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.infoLayout.addSpacing(5)
        self.infoLayout.addWidget(self.timeIcon, 0, Qt.AlignmentFlag.AlignVCenter)
        self.infoLayout.addWidget(self.timeLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.infoLayout.addStretch(1)

    def _connectSignalToSlot(self):
        self.openFolderButton.clicked.connect(self._onOpenButtonClicked)
        self.deleteButton.clicked.connect(self._onDeleteButtonClicked)
        self.stopButton.clicked.connect(self._onStopButtonClicked)

    def _onOpenButtonClicked(self):
        return

    def _onStopButtonClicked(self):
        w = MessageBox(
            self.tr("Stop recording"), self.tr("Are you sure to stop recording the live stream?"), self.window()
        )
        w.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

    def removeTask(self, deleteFile=False):
        return

    def setInfo(self, info):
        return
