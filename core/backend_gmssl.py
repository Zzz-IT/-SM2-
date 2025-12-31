from __future__ import annotations
from gmssl import func
from gmssl.sm2 import CryptSM2, default_ecc_table
from core.backend import CryptoBackend

class GmsslBackend(CryptoBackend):
    name = "gmssl"

    def generate_keypair(self) -> tuple[str, str]:
        pri = func.random_hex(64)  # 256-bit private key
        tmp = CryptSM2(public_key="", private_key=pri)

        # gmssl 常见实现：用 _kg 计算公钥点
        # 如果你的 gmssl 版本接口不同，报错贴我，我给你适配。
        pub = tmp._kg(int(pri, 16), default_ecc_table["g"])
        return pri, pub

    def sign(self, msg: bytes, private_key_hex: str, public_key_hex: str) -> str:
        c = CryptSM2(public_key=public_key_hex, private_key=private_key_hex)
        k = func.random_hex(64)
        return c.sign(msg, k)

    def verify(self, msg: bytes, signature_hex: str, public_key_hex: str) -> bool:
        c = CryptSM2(public_key=public_key_hex, private_key="")
        return bool(c.verify(signature_hex, msg))
