from Models.PCState import PCState

from PyQt6 import QtCore

import uuid


class PCInfo(QtCore.QObject):
    def __init__(self, pcId: str = uuid.uuid4().hex, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self._pcId = pcId
        self._pcState = PCState(parent=self)

    def getPcId(self) -> str:
        return self._pcId

    def getPcState(self) -> PCState:
        return self._pcState