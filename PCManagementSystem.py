from Models.PCInfo import PCInfo
from Models.HelpInfo import HelpInfo

from Controllers.AccountController import AccountController
from Controllers.HelpController import HelpController
from Controllers.ProductManager import ProductManager
from Controllers.PCManager import PCManager

from Network.WebSocketServer import WebSocketServer
from Network.WebSocketClient import WebSocketClient

from PyQt6 import QtCore, QtWebSockets

import typing
import json


class PCManagementSystem(QtCore.QObject):
    showTextLog = QtCore.pyqtSignal(str)
    helpRequested = QtCore.pyqtSignal(HelpInfo)

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self._accountController = AccountController(parent=self)
        self._pcManager = PCManager(parent=self)
        self._productManager = ProductManager(self._accountController, parent=self)
        self._helpController = HelpController(self._accountController, self._pcManager, parent=self)
        self._helpController.helpRequested.connect(self.helpRequested)
        self._webSocketServer = WebSocketServer(parent=self)
        self._webSocketServer.onClientConnect.connect(self._onClientConnect)
        self._webSocketServer.onClientDisconnect.connect(self._onClientDisconnect)
        self._webSocketServer.onError.connect(self._onServerError)
        self._webSocketServer.onClose.connect(self._onServerClose)
        self._webSocketServer.start(80)

    def _onClientConnect(self, client: WebSocketClient) -> None:
        client.textMessageReceived.connect(self._onNewMessage)
        self._pcManager.addPcInfo(client.getPcInfo())
        self.showTextLog.emit(f"\nPC Connected: {client.getPcInfo().getPcId()}")

    def _onClientDisconnect(self, client: WebSocketClient) -> None:
        self._pcManager.removePcInfo(client.getPcInfo())
        self.showTextLog.emit(f"\nPC Disconnected: {client.getPcInfo().getPcId()}")
        if client.isLoggedIn():
            self.showTextLog.emit(f"\nUser Logged Out: {client.getUser().getDisplayName()}")
            client.logout()

    def _onServerError(self, closeCode: QtWebSockets.QWebSocketProtocol.CloseCode) -> None:
        self.showTextLog.emit(f"\nServer Error: {closeCode}")

    def _onServerClose(self) -> None:
        self.showTextLog.emit("\nServer Closed")

    def _onNewMessage(self, message: str) -> None:
        client: WebSocketClient = self.sender()
        try:
            self._parsePayload(client, json.loads(message))
        except:
            self.showTextLog.emit(f"\nUnable to parse message from client: {client.getId()}")
            self.showTextLog.emit(f"\nClient User: {client.getUser()}")
            self.showTextLog.emit(f"\n[Message] {message}")

    def _parsePayload(self, client: WebSocketClient, payload: dict[str, typing.Any]) -> None:
        if payload["type"] == "register":
            user = self._accountController.signUpRequest(payload["data"]["username"], payload["data"]["password"], payload["data"]["name"])
            if user == None:
                client.notice("Duplicate username")
            else:
                client.login(user)
                self.showTextLog.emit(f"\nRegister / Login: {client.getUser()}")
        elif payload["type"] == "login":
            user = self._accountController.getLogin(payload["data"]["username"], payload["data"]["password"])
            if user == None:
                client.notice("Invalid username or password")
            else:
                client.login(user)
                self.showTextLog.emit(f"\nLogin: {client.getUser()}")
        elif payload["type"] == "logout":
            self.showTextLog.emit(f"\nLogout: {client.getUser()}")
            client.logout()
        elif payload["type"] == "help":
            self.helpRequested.emit(HelpInfo(client.getUser(), client.getPcInfo(), payload["data"]["message"]))
        elif payload["type"] == "product":
            if payload["data"]["type"] == "time":
                oldLeftTime = int(client.getLeftTimeMs() / 1000)
                client.addLeftTimeMs(payload["data"]["amount"])
                newLeftTime = int(client.getLeftTimeMs() / 1000)
                self.showTextLog.emit(f"\n[Time Add]\nUser: {client.getUser().getDisplayName()}\nOld Left Time: {oldLeftTime}s\nAdd Time: {int(payload["data"]["amount"] / 1000)}s\nNew Left Time: {newLeftTime}s")
        else:
            self.showTextLog.emit(f"\nUnknown payload from client.\nClient: {client.getPcInfo().getPcId()} Payload: {payload["type"]}")

    def getPcInfo(self, pcId: str) -> PCInfo | None:
        return self._pcManager.getPcInfo(pcId)

    def sendRemoteCommand(self, targetPcId: str, command: str) -> PCInfo | None:
        pcInfo = self._pcManager.getPcInfo(targetPcId)
        if pcInfo == None:
            return None
        webSocketClient = self._webSocketServer.getClient(pcInfo.getPcId())
        if webSocketClient == None:
            return None
        webSocketClient.remoteControl(command)
        return pcInfo