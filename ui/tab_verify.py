import time
from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QPlainTextEdit, QLabel, QMessageBox, QHBoxLayout
from core.backend import get_backend
from core.formats import pack_message

class VerifyTab(QWidget):
    def __init__(self, keys_tab, sign_tab, log_cb):
        super().__init__()
        self.keys_tab = keys_tab
        self.sign_tab = sign_tab
        self.log = log_cb
        self.backend = get_backend()

        self.in_uid = QLineEdit(keys_tab.get_user_id())
        self.in_msg = QPlainTextEdit()
        self.in_sig = QPlainTextEdit()
        self.result = QLabel("等待验签")

        btn_fill = QPushButton("填充上一次签名内容")
        btn_verify = QPushButton("验签")
        btn_fill.clicked.connect(self.on_fill)
        btn_verify.clicked.connect(self.on_verify)

        form = QFormLayout()
        form.addRow("User ID", self.in_uid)
        form.addRow("消息（UTF-8）", self.in_msg)
        form.addRow("签名（hex）", self.in_sig)

        btns = QHBoxLayout()
        btns.addWidget(btn_fill)
        btns.addWidget(btn_verify)

        root = QVBoxLayout(self)
        root.addLayout(form)
        root.addLayout(btns)
        root.addWidget(QLabel("验签结果"))
        root.addWidget(self.result)

    def on_fill(self):
        uid = self.sign_tab.in_uid.text().strip() or self.keys_tab.get_user_id()
        self.in_uid.setText(uid)
        self.in_msg.setPlainText(self.sign_tab.last_message_text)
        self.in_sig.setPlainText(self.sign_tab.last_signature)
        self.log("[VERIFY] 已填充上一次签名数据")

    def on_verify(self):
        uid = self.in_uid.text().strip() or self.keys_tab.get_user_id()
        msg_text = self.in_msg.toPlainText()
        sig = self.in_sig.toPlainText().strip()
        pub = self.keys_tab.get_public_key()

        if not msg_text or not sig or not pub:
            QMessageBox.warning(self, "提示", "请填写 User ID / 消息 / 签名，并确保已加载公钥")
            return

        data = pack_message(uid, msg_text)
        try:
            t0 = time.perf_counter()
            ok = self.backend.verify(data, sig, pub)
            dt = (time.perf_counter() - t0) * 1000
        except Exception as e:
            QMessageBox.critical(self, "验签失败", str(e))
            return

        if ok:
            self.result.setText(f"✅ 验签成功（{dt:.2f} ms）")
            self.log(f"[VERIFY] OK  耗时 {dt:.2f} ms")
        else:
            self.result.setText(f"❌ 验签失败（{dt:.2f} ms）")
            self.log(f"[VERIFY] FAIL  耗时 {dt:.2f} ms")
