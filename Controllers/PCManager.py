from Models.PCInfo import PCInfo

from PyQt6 import QtCore


class PCManager(QtCore.QObject):
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self._pcList: dict[str, PCInfo] = {}

    def addPcInfo(self, pcInfo: PCInfo) -> None:
        self._pcList[pcInfo.getPcId()] = pcInfo

    def removePcInfo(self, pcInfo: PCInfo) -> None:
        self._pcList.pop(pcInfo.getPcId())

    def getPcInfo(self, pcId: str) -> PCInfo | None:
        return self._pcList.get(pcId, None)