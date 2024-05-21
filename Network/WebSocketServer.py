from Network.WebSocketClient import WebSocketClient

from PyQt6 import QtCore, QtNetwork, QtWebSockets


class WebSocketServer(QtCore.QObject):
    onClientConnect = QtCore.pyqtSignal(WebSocketClient)
    onClientDisconnect = QtCore.pyqtSignal(WebSocketClient)
    onError = QtCore.pyqtSignal(QtWebSockets.QWebSocketProtocol.CloseCode)
    onClose = QtCore.pyqtSignal()

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self._server = QtWebSockets.QWebSocketServer("", QtWebSockets.QWebSocketServer.SslMode.NonSecureMode, parent=self)
        self._server.newConnection.connect(self._onNewConnection)
        self._server.closed.connect(self._onClosed)
        self._server.serverError.connect(self._onServerError)
        self._clients: dict[str, WebSocketClient] = {}

    def start(self, port: int) -> bool:
        if self._server.listen(QtNetwork.QHostAddress.SpecialAddress.LocalHost, port):
            return True
        else:
            return False

    def stop(self) -> None:
        self._server.close()

    def isRunning(self) -> bool:
        return self._server.isListening()

    def getClient(self, clientId: str) -> WebSocketClient | None:
        return self._clients.get(clientId)

    def _onNewConnection(self) -> None:
        webSocket = self._server.nextPendingConnection()
        if webSocket.isValid():
            client = WebSocketClient(webSocket, QtCore.QUrlQuery(webSocket.requestUrl().query()).queryItemValue("id"), parent=self)
            client.disconnected.connect(self._clientDisconnected)
            self._clients[client.getId()] = client
            self.onClientConnect.emit(client)

    def _onClosed(self) -> None:
        self.onClose.emit()

    def _onServerError(self, closeCode: QtWebSockets.QWebSocketProtocol.CloseCode) -> None:
        self.onError.emit(closeCode)

    def _clientDisconnected(self) -> None:
        client: WebSocketClient = self.sender()
        self._clients.pop(client.getId())
        self.onClientDisconnect.emit(client)