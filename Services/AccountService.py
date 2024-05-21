from Models.User import User
from Models.Repository import Repository

from PyQt6 import QtCore


class AccountService(QtCore.QObject):
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self._repository = Repository(parent=self)

    def findById(self, userId: str) -> User | None:
        return self._repository.findById(userId)

    def findByUsername(self, username: str) -> User | None:
        return self._repository.findByUsername(username)

    def saveUser(self, user: User) -> None:
        self._repository.saveUser(user)