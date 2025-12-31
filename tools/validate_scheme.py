import os
import json
import time
from datetime import datetime

from core.backend import get_backend
from core.formats import pack_message

def tamper_message(msg: str) -> str:
    if not msg:
        return "X"
    # 最简单篡改：改最后一个字符
    last = msg[-1]
    repl = "X" if last != "X" else "Y"
    return msg[:-1] + repl

def run_scheme():
    backend = get_backend()

    uid = "1234567812345678"
    msg = "temperature=23.5;device=sensor-001;ts=1700000000"

    pri, pub = backend.generate_keypair()

    base = {
        "backend": backend.name,
        "uid": uid,
        "message": msg,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "cases": []
    }

    # Case 1: 正常签名验签
    data = pack_message(uid, msg)
    t0 = time.perf_counter()
    sig = backend.sign(data, pri, pub)
    sign_ms = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    ok = backend.verify(data, sig, pub)
    ver_ms = (time.perf_counter() - t0) * 1000

    base["cases"].append({
        "name": "正常验签",
        "expected": True,
        "actual": ok,
        "sign_ms": round(sign_ms, 3),
        "verify_ms": round(ver_ms, 3)
    })

    # Case X: 重放风险验证（同一消息+签名重复提交仍可通过）
    # 说明：签名算法保证完整性与身份，但不天然防重放；重复提交同一 (msg, sig) 仍会验签成功。
    t0 = time.perf_counter()
    ok_replay_1 = backend.verify(data, sig, pub)
    ok_replay_2 = backend.verify(data, sig, pub)
    replay_ms = (time.perf_counter() - t0) * 1000

    base["cases"].append({
        "name": "重放风险验证（同一消息+签名重复验证）",
        "expected": True,
        "actual": bool(ok_replay_1 and ok_replay_2),
        "detail": {
            "note": "该用例用于说明：签名算法本身不防重放；若不引入 nonce/timestamp/序列号等机制，同一消息与签名可被重复提交并通过验签。"
        },
        "verify_twice_ms": round(replay_ms, 3)
    })

    # Case 2: 篡改消息 => 应失败
    msg2 = tamper_message(msg)
    data2 = pack_message(uid, msg2)
    ok2 = backend.verify(data2, sig, pub)
    base["cases"].append({
        "name": "篡改消息后验签",
        "expected": False,
        "actual": ok2,
        "detail": {"tampered_message": msg2}
    })

    # Case 3: 伪造签名（换一对私钥签）=> 用原公钥验应失败
    pri_f, pub_f = backend.generate_keypair()
    sig_f = backend.sign(data, pri_f, pub_f)
    ok3 = backend.verify(data, sig_f, pub)
    base["cases"].append({
        "name": "伪造签名（他人私钥签）",
        "expected": False,
        "actual": ok3
    })

    # Case 4: User ID 不一致 => 应失败
    uid_bad = "0000000000000000"
    data_bad = pack_message(uid_bad, msg)
    ok4 = backend.verify(data_bad, sig, pub)
    base["cases"].append({
        "name": "User ID 不一致",
        "expected": False,
        "actual": ok4,
        "detail": {"uid_bad": uid_bad}
    })

    # 输出报告
    os.makedirs("data/logs", exist_ok=True)
    fname = datetime.now().strftime("validation_report_%Y%m%d_%H%M%S.json")
    path = os.path.join("data", "logs", fname)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(base, f, ensure_ascii=False, indent=2)

    # 控制台摘要
    print("=== 验证方案结果 ===")
    print("backend:", backend.name)
    print("report :", path)
    for c in base["cases"]:
        passed = (c["expected"] == c["actual"])
        print(f"- {c['name']}: expected={c['expected']} actual={c['actual']}  -> {'PASS' if passed else 'FAIL'}")

if __name__ == "__main__":
    run_scheme()
