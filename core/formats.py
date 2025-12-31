def pack_message(user_id: str, message_text: str) -> bytes:
    """
    最简可复现策略：把 User ID 作为前缀纳入签名输入。
    这样验证方案里可以清晰演示：ID 一变 => 验签失败。
    """
    uid = (user_id or "").strip()
    msg = message_text or ""
    return (f"UID={uid}|{msg}").encode("utf-8")
