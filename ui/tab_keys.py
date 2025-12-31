from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
from core.backend import get_backend

DEFAULT_UID = "1234567812345678"

class KeysTab(QWidget):
    def __init__(self, log_cb):
        super().__init__()
        self.log = log_cb
        self.backend = get_backend()

        self.in_uid = QLineEdit(DEFAULT_UID)
        self.in_pub = QLineEdit()
        self.in_pri = QLineEdit()
        self.in_pri.setEchoMode(QLineEdit.Password)

        btn_gen = QPushButton("生成密钥对")
        btn_toggle = QPushButton("显示/隐藏私钥")
        btn_copy_pub = QPushButton("复制公钥")
        btn_copy_pri = QPushButton("复制私钥")

        btn_gen.clicked.connect(self.on_gen)
        btn_toggle.clicked.connect(self.on_toggle)
        btn_copy_pub.clicked.connect(lambda: self.copy_text(self.in_pub.text(), "公钥"))
        btn_copy_pri.clicked.connect(lambda: self.copy_text(self.in_pri.text(), "私钥"))

        form = QFormLayout()
        form.addRow("User ID", self.in_uid)
        form.addRow("公钥（hex）", self.in_pub)
        form.addRow("私钥（hex）", self.in_pri)

        btns = QHBoxLayout()
        for b in (btn_gen, btn_toggle, btn_copy_pub, btn_copy_pri):
            btns.addWidget(b)

        root = QVBoxLayout(self)
        root.addLayout(form)
        root.addLayout(btns)

    def on_gen(self):
        try:
            pri, pub = self.backend.generate_keypair()
        except Exception as e:
            QMessageBox.critical(self, "生成失败", str(e))
            return
        self.in_pri.setText(pri)
        self.in_pub.setText(pub)
        self.log("[KEYGEN] OK")

    def on_toggle(self):
        self.in_pri.setEchoMode(
            QLineEdit.Normal if self.in_pri.echoMode() == QLineEdit.Password else QLineEdit.Password
        )

    def copy_text(self, text: str, label: str):
        from PySide6.QtWidgets import QApplication
        if not text.strip():
            QMessageBox.warning(self, "提示", f"{label}为空")
            return
        QApplication.clipboard().setText(text)
        self.log(f"[COPY] {label} 已复制")

    def get_user_id(self) -> str:
        return self.in_uid.text().strip()

    def get_public_key(self) -> str:
        return self.in_pub.text().strip()

    def get_private_key(self) -> str:
        return self.in_pri.text().strip()
