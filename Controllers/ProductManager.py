from Models.User import User
from Models.Product import Product
from Models.TimeProduct import TimeProduct

from Controllers.AccountController import AccountController

from PyQt6 import QtCore


class ProductManager(QtCore.QObject):
    def __init__(self, accountController: AccountController, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self._productList: dict[str, Product] = {}
        self._accountController = accountController

    def addProduct(self, product: Product) -> None:
        self._productList[product.getProductId()] = product

    def getProduct(self, productId: str) -> Product | None:
        return self._productList.get(productId, None)

    def buyProduct(self, userId: str, productId: str, payment: int) -> Product | None:
        user = self._accountController.getUser(userId)
        if user == None:
            return None
        product = self.getProduct(productId)
        if product == None:
            return None
        if payment != product.getCost():
            return None
        return product

    def buyTimeProduct(self, userId: str, productId: str, payment: int) -> User | None:
        user = self._accountController.getUser(userId)
        if user == None:
            return None
        product = self.getProduct(productId)
        if product == None:
            return None
        if not isinstance(product, TimeProduct):
            return None
        if payment != product.getCost():
            return None
        user.setLeftTimeMs(user.getLeftTimeMs() + product.getTimeMs())
        return user