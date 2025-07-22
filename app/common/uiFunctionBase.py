# coding: utf-8
import os
import sys
from typing import Callable, Optional, Union
from pathlib import Path

from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl, QFileInfo, QDir, QProcess
from PySide6.QtWidgets import QWidget

from ..common.simpleLogger import loggerPrint
from ..common.levelDefs import LogLevels, MsgBoxLevels
from ..common.configLoader import getConfig
from ..common.eventManager import EventManager, EventEnum, EventFuncType

from .singleton import singleton


# 这里的全部信息都是每次从配置读取的，完全不使用缓存
@singleton
class UIFunctionBase:
    _singleton = None

    def __init__(self) -> None:
        super().__init__()
        self._fetcher = None
        self._formatter = None
        self._exporter = None

    def uiGetConfig(self, key: str, default: str = "") -> str:
        return getConfig(key, default)

    def uiShowMsgBox(
        self,
        level: MsgBoxLevels,
        msg: str,
        acptCbk: Optional[Callable] = None,
        rjctCbk: Optional[Callable] = None,
    ) -> None:
        EventManager.getSingleton().showMsgBox(
            level=level,
            msg=msg,
            acptCbk=acptCbk,
            rejtCbk=rjctCbk,
        )

    def uiSetMainWindow(self, mainWindow: QWidget) -> None:
        EventManager._mainWindow = mainWindow

    # 触发错误处理
    def uiEmitError(self, filename: str, lineno: str, error: str) -> None:
        EventManager.getSingleton()._errorSignal.emit(filename, lineno, error)

    # 触发事件
    def uiEmit(self, event: EventEnum, data: dict) -> None:
        loggerPrint(f"触发事件: {event.name}", level=LogLevels.INFO)
        EventManager.getSingleton().emitEvent(event, data)

    # 订阅事件
    def uiSubscribe(self, event: EventEnum, handler: Callable, evtFuncType: EventFuncType) -> None:
        loggerPrint(f"订阅事件: {event.name}", level=LogLevels.INFO)
        EventManager.getSingleton().subscribe(event, handler, evtFuncType)

    # 取消订阅事件
    def uiUnsubscribe(self, event: EventEnum, handler: Callable) -> None:
        loggerPrint(f"取消订阅事件: {event.name}", level=LogLevels.INFO)
        EventManager.getSingleton().unsubscribe(event, handler)

    def uiOpenURL(self, url: str):
        if not url.startswith("http"):
            if not os.path.exists(url):
                return False

            QDesktopServices.openUrl(QUrl.fromLocalFile(url))
        else:
            QDesktopServices.openUrl(QUrl(url))

        return True

    def showInFolder(self, path: Union[str, Path]):
        """show file in file explorer"""
        if not os.path.exists(path):
            return False

        if isinstance(path, Path):
            path = str(path.absolute())

        if not path or path.lower().startswith("http"):
            return False

        info = QFileInfo(path)  # type:QFileInfo
        if sys.platform == "win32":
            args = [QDir.toNativeSeparators(path)]
            if not info.isDir():
                args.insert(0, "/select,")

            QProcess.startDetached("explorer", args)
        elif sys.platform == "darwin":
            args = [
                "-e",
                'tell application "Finder"',
                "-e",
                "activate",
                "-e",
                f'select POSIX file "{path}"',
                "-e",
                "end tell",
                "-e",
                "return",
            ]
            QProcess.execute("/usr/bin/osascript", args)
        else:
            url = QUrl.fromLocalFile(path if info.isDir() else info.path())
            QDesktopServices.openUrl(url)

        return True


uiFuncBase = UIFunctionBase()
