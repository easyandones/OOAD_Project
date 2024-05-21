from Models.Product import Product

from PyQt6 import QtCore

import uuid


class TimeProduct(Product):
    def __init__(self, productId: str = uuid.uuid4().hex, name: str = "", cost: int = 0, timeMs: int = 0, parent: QtCore.QObject | None = None):
        super().__init__(productId=productId, name=name, cost=cost, parent=parent)
        self._timeMs = timeMs

    def getTimeMs(self) -> int:
        return self._timeMs