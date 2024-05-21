from PyQt6 import QtCore

import uuid


class Product(QtCore.QObject):
    def __init__(self, productId: str = uuid.uuid4().hex, name: str = "", cost: int = 0, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self._productId = productId
        self._name = name
        self._cost = cost

    def getProductId(self) -> str:
        return self._productId

    def getName(self) -> str:
        return self._name

    def getCost(self) -> int:
        return self._cost