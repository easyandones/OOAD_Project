from Models.User import User
from Models.PCInfo import PCInfo

from PyQt6 import QtCore, QtWebSockets

import typing
import json


class WebSocketClient(QtCore.QObject):
    textMessageReceived = QtCore.pyqtSignal(str)
    disconnected = QtCore.pyqtSignal()

    def __init__(self, webSocket: QtWebSockets.QWebSocket, pcId: str, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self._pcInfo = PCInfo(pcId=pcId, parent=self)
        self._webSocket = webSocket
        self._webSocket.textMessageReceived.connect(self._textMessageReceived)
        self._webSocket.disconnected.connect(self._diconnected)
        self._user: User | None = None

    def _textMessageReceived(self, text: str) -> None:
        self.textMessageReceived.emit(text)

    def _diconnected(self) -> None:
        self.disconnected.emit()

    def getId(self) -> str:
        return self._pcInfo.getPcId()

    def getPcInfo(self) -> PCInfo:
        return self._pcInfo

    def isValid(self) -> bool:
        return self._webSocket.isValid()

    def getUser(self) -> User | None:
        return self._user

    def isLoggedIn(self) -> bool:
        return self._user != None

    def _sendEvent(self, payload: dict[str, typing.Any]) -> None:
        self._webSocket.sendTextMessage(json.dumps(payload))

    def login(self, user: User) -> None:
        self._user = user
        self.getPcInfo().getPcState().setLoggedIn(user)
        self._sendEvent({
            "type": "account",
            "data": {
                "loggedIn": True,
                "name": self._user.getDisplayName(),
                "leftTimeMs": self.getLeftTimeMs()
            }
        })

    def logout(self) -> None:
        self._user.setLeftTimeMs(self.getLeftTimeMs())
        self._user = None
        self.getPcInfo().getPcState().setLoggedOut()
        self._sendEvent({
            "type": "account",
            "data": {
                "loggedIn": False
            }
        })

    def notice(self, message: str) -> None:
        self._sendEvent({
            "type": "notice",
            "data": {
                "message": message
            }
        })

    def addLeftTimeMs(self, leftTimeMs: int) -> None:
        self._user.setLeftTimeMs(self.getLeftTimeMs() + leftTimeMs)
        self.getPcInfo().getPcState().resetActiveTime()
        self._sendEvent({
            "type": "time",
            "data": {
                "leftTimeMs": self.getLeftTimeMs()
            }
        })

    def getLeftTimeMs(self) -> int:
        leftTime = max(0, self._user.getLeftTimeMs() - (QtCore.QDateTime.currentDateTimeUtc().toMSecsSinceEpoch() - self.getPcInfo().getPcState().getActiveTime()))
        if leftTime == 0:
            self._user.setLeftTimeMs(0)
            self.getPcInfo().getPcState().resetActiveTime()
        return leftTime

    def remoteControl(self, command: str) -> None:
        self._sendEvent({
            "type": "control",
            "data": {
                "command": command
            }
        })