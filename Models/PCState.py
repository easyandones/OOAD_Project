from Models.User import User

from PyQt6 import QtCore


class PCState(QtCore.QObject):
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self._user: User | None = None
        self._activeTime: int | None = None

    def setLoggedIn(self, user: User) -> None:
        self._user = user
        self._activeTime = QtCore.QDateTime.currentDateTimeUtc().toMSecsSinceEpoch()

    def setLoggedOut(self) -> None:
        self._user = None
        self._activeTime = None

    def resetActiveTime(self) -> None:
        self._activeTime = QtCore.QDateTime.currentDateTimeUtc().toMSecsSinceEpoch()

    def getUser(self) -> User | None:
        return self._user

    def getActiveTime(self) -> int | None:
        return self._activeTime