from Utils.Utils import Utils

from PyQt6 import QtCore

import uuid


class User(QtCore.QObject):
    def __init__(self, userId: str = uuid.uuid4().hex, username: str = "", passwordHash: str = "", displayName: str = "", leftTimeMs: int = 0, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self._userId = userId
        self._username = username
        self._passwordHash = passwordHash
        self._displayName = displayName
        self._leftTimeMs = leftTimeMs

    def __str__(self):
        return f"<User {self._displayName}({self._username})>"

    def setPassword(self, password: str) -> None:
        self._passwordHash = Utils.getHash(password)

    def setDisplayName(self, displayName: str) -> None:
        self._displayName = displayName

    def setLeftTimeMs(self, leftTimeMs: int) -> None:
        self._leftTimeMs = leftTimeMs

    def getUserId(self) -> str:
        return self._userId

    def getUsername(self) -> str:
        return self._username

    def getPasswordHash(self) -> str:
        return self._passwordHash

    def getDisplayName(self) -> str:
        return self._displayName

    def getLeftTimeMs(self) -> int:
        return self._leftTimeMs