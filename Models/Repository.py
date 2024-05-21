from Models.User import User

from PyQt6 import QtCore


class Repository(QtCore.QObject):
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self._userList: dict[str, User] = {}

    def findById(self, userId: str) -> User | None:
        return self._userList.get(userId, None)

    def findByUsername(self, username: str) -> User | None:
        for user in self._userList.values():
            if username == user.getUsername():
                return user
        return None

    def saveUser(self, user: User) -> None:
        self._userList[user.getUserId()] = user