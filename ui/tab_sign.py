import time
from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QPlainTextEdit, QLabel, QMessageBox, QHBoxLayout
from core.backend import get_backend
from core.formats import pack_message

class SignTab(QWidget):
    def __init__(self, keys_tab, log_cb):
        super().__init__()
        self.keys_tab = keys_tab
        self.log = log_cb
        self.backend = get_backend()
        self.last_message_text = ""
        self.last_signature = ""

        self.in_uid = QLineEdit(keys_tab.get_user_id())
        self.in_msg = QPlainTextEdit()
        self.out_sig = QPlainTextEdit()
        self.out_sig.setReadOnly(True)

        btn_sign = QPushButton("签名")
        btn_copy = QPushButton("复制签名")
        btn_sign.clicked.connect(self.on_sign)
        btn_copy.clicked.connect(self.on_copy)

        form = QFormLayout()
        form.addRow("User ID", self.in_uid)
        form.addRow("消息（UTF-8）", self.in_msg)

        btns = QHBoxLayout()
        btns.addWidget(btn_sign)
        btns.addWidget(btn_copy)

        root = QVBoxLayout(self)
        root.addLayout(form)
        root.addLayout(btns)
        root.addWidget(QLabel("签名输出（hex）"))
        root.addWidget(self.out_sig)

    def on_sign(self):
        uid = self.in_uid.text().strip() or self.keys_tab.get_user_id()
        msg_text = self.in_msg.toPlainText()
        pri = self.keys_tab.get_private_key()
        pub = self.keys_tab.get_public_key()

        if not msg_text:
            QMessageBox.warning(self, "提示", "请输入消息")
            return
        if not pri or not pub:
            QMessageBox.warning(self, "提示", "请先在“密钥管理”生成或导入密钥")
            return

        data = pack_message(uid, msg_text)
        try:
            t0 = time.perf_counter()
            sig = self.backend.sign(data, pri, pub)
            dt = (time.perf_counter() - t0) * 1000
        except Exception as e:
            QMessageBox.critical(self, "签名失败", str(e))
            return

        self.last_message_text = msg_text
        self.last_signature = sig
        self.out_sig.setPlainText(sig)
        self.log(f"[SIGN] OK  耗时 {dt:.2f} ms")

    def on_copy(self):
        from PySide6.QtWidgets import QApplication
        sig = self.out_sig.toPlainText().strip()
        if not sig:
            QMessageBox.warning(self, "提示", "签名为空")
            return
        QApplication.clipboard().setText(sig)
        self.log("[COPY] 签名已复制")
