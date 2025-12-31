from __future__ import annotations

class CryptoBackend:
    name: str = "base"

    def generate_keypair(self) -> tuple[str, str]:
        """return (private_key_hex, public_key_hex)"""
        raise NotImplementedError

    def sign(self, msg: bytes, private_key_hex: str, public_key_hex: str) -> str:
        """return signature hex string"""
        raise NotImplementedError

    def verify(self, msg: bytes, signature_hex: str, public_key_hex: str) -> bool:
        raise NotImplementedError


def get_backend() -> CryptoBackend:
    # 当前最简单后端：gmssl
    from core.backend_gmssl import GmsslBackend
    return GmsslBackend()
