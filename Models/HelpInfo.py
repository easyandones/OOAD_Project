from Models.User import User
from Models.PCInfo import PCInfo

from PyQt6 import QtCore


class HelpInfo(QtCore.QObject):
    def __init__(self, user: User, pcInfo: PCInfo, message: str, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self._user = user
        self._pcInfo = pcInfo
        self._message = message
        self._timestamp = QtCore.QDateTime.currentDateTimeUtc().toSecsSinceEpoch()

    def getUser(self) -> User:
        return self._user

    def getPCInfo(self) -> PCInfo:
        return self._pcInfo

    def getMessage(self) -> str:
        return self._message

    def getTimestamp(self) -> int:
        return self._timestamp