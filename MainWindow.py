from Models.HelpInfo import HelpInfo

from PCManagementSystem import PCManagementSystem

from PyQt6 import QtWidgets

import sys


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent=parent)
        self.setWindowTitle("PC Management System")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.chatDisplay = QtWidgets.QTextEdit(self)
        self.chatDisplay.setReadOnly(True)
        self.verticalLayout.addWidget(self.chatDisplay)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.messageInput = QtWidgets.QLineEdit(self)
        self.messageInput.setMinimumHeight(30)
        self.messageInput.returnPressed.connect(self._evalCommand)
        self.horizontalLayout.addWidget(self.messageInput)
        self.sendButton = QtWidgets.QPushButton("실행", self)
        self.sendButton.clicked.connect(self._evalCommand)
        self.horizontalLayout.addWidget(self.sendButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self._core = PCManagementSystem(parent=self)
        self._core.showTextLog.connect(self.logText)
        self._core.helpRequested.connect(self._helpRequested)

    def logText(self, text: str) -> None:
        self.chatDisplay.append(text)

    def _helpRequested(self, helpInfo: HelpInfo) -> None:
        self.showInfo("관리자 호출", f"{helpInfo.getPCInfo().getPcId()}번 좌석 - {helpInfo.getUser().getDisplayName()}님의 메시지\n\n{helpInfo.getMessage()}")

    def showInfo(self, title: str, content: str) -> None:
        messageBox = QtWidgets.QMessageBox(parent=self)
        messageBox.setWindowTitle(title)
        messageBox.setText(content)
        messageBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        messageBox.exec()

    def _evalCommand(self):
        message = self.messageInput.text()
        if message != "":
            self.logText(f"ADMIN >>> {message}")
            self.messageInput.clear()
            try:
                command, params = message.split(" ", 1)
                if command == "status":
                    pcInfo = self._core.getPcInfo(params)
                    if pcInfo == None:
                        self.logText(f"PC Not Found: {params}")
                    else:
                        self.logText(f"PC ID: {pcInfo.getPcId()}\nLogged In: {pcInfo.getPcState().getUser() != None}")
                        if pcInfo.getPcState().getUser() != None:
                            self.logText(f"User: {pcInfo.getPcState().getUser().getDisplayName()}")
                elif command == "control":
                    targetPcId, remoteControlCommand = params.split(" ", 1)
                    pcInfo = self._core.sendRemoteCommand(targetPcId, remoteControlCommand)
                    if pcInfo == None:
                        self.logText(f"PC Not Found: {targetPcId}")
                    else:
                        self.logText(f"Sent command to PC {pcInfo.getPcId()}\nCommand: {remoteControlCommand}")
                else:
                    self.logText(f"Unknown command: {command}")
            except:
                self.logText("Invalid Command")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())