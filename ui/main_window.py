from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPlainTextEdit, QLabel
from ui.tab_keys import KeysTab
from ui.tab_sign import SignTab
from ui.tab_verify import VerifyTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SM2 数字签名系统")

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)

        tabs = QTabWidget()
        self.tab_keys = KeysTab(self.append_log)
        self.tab_sign = SignTab(self.tab_keys, self.append_log)
        self.tab_verify = VerifyTab(self.tab_keys, self.tab_sign, self.append_log)

        tabs.addTab(self.tab_keys, "密钥管理")
        tabs.addTab(self.tab_sign, "签名")
        tabs.addTab(self.tab_verify, "验签")

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.addWidget(tabs, 8)
        layout.addWidget(QLabel("运行日志"))
        layout.addWidget(self.log, 3)
        self.setCentralWidget(root)

    def append_log(self, msg: str):
        self.log.appendPlainText(msg)
