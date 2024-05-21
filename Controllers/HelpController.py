from Models.HelpInfo import HelpInfo

from Controllers.AccountController import AccountController
from Controllers.PCManager import PCManager

from PyQt6 import QtCore


class HelpController(QtCore.QObject):
    helpRequested = QtCore.pyqtSignal(HelpInfo)

    def __init__(self, accountController: AccountController, pcManager: PCManager, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self._accountController = accountController
        self._pcManager = pcManager

    def callStaff(self, userId: str, pcId: str, message: str) -> None:
        user = self._accountController.getUser(userId)
        if user == None:
            return
        pcInfo = self._pcManager.getPcInfo(pcId)
        if pcInfo == None:
            return
        self.helpRequested.emit(
            HelpInfo(
                user=user,
                pcInfo=pcInfo,
                message=message,
                parent=self
            )
        )