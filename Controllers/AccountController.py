from Models.User import User

from Services.AccountService import AccountService

from Utils.Utils import Utils

from PyQt6 import QtCore


class AccountController(QtCore.QObject):
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self._accountService = AccountService(parent=self)

    def getLogin(self, username: str, password: str) -> User | None:
        user = self._accountService.findByUsername(username)
        if user == None:
            return None
        passwordHash = Utils.getHash(password)
        if passwordHash == user.getPasswordHash():
            return user
        return None

    def signUpRequest(self, username: str, password: str, displayName: str) -> User | None:
        user = self._accountService.findByUsername(username)
        if user != None:
            return None
        user = User(
            username=username,
            passwordHash=Utils.getHash(password),
            displayName=displayName
        )
        self._accountService.saveUser(user)
        return user

    def getUser(self, userId: str) -> User | None:
        return self._accountService.findById(userId)

    def setUserLeftTime(self, userId: str, leftTimeMs: int) -> None:
        user = self._accountService.findById(userId)
        if user != None:
            user.setLeftTimeMs(leftTimeMs)