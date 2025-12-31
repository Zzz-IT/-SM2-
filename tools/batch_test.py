import os
import sys
import json
import time
import random
from pathlib import Path
from datetime import datetime
from statistics import mean

# 解决直接运行 tools/batch_test.py 时找不到 core 包的问题
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.backend import get_backend
from core.formats import pack_message

def tamper_message(msg: str) -> str:
    if not msg:
        return "X"
    last = msg[-1]
    repl = "X" if last != "X" else "Y"
    return msg[:-1] + repl

def mk_message(length: int) -> str:
    # 生成指定长度的可读消息（用于批量性能测试）
    base = "device=sensor-001;temp=23.5;ts=1700000000;"
    if length <= len(base):
        return base[:length]
    # 用重复填充到目标长度
    pad = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789;"
    s = base + (pad * ((length - len(base)) // len(pad) + 1))
    return s[:length]

def now_name(prefix: str) -> str:
    return datetime.now().strftime(f"{prefix}_%Y%m%d_%H%M%S.json")

def run_one_suite(backend, uid: str, msg: str):
    """对一条消息跑一轮 4 用例，并记录耗时。"""
    pri, pub = backend.generate_keypair()
    data = pack_message(uid, msg)

    # 签名
    t0 = time.perf_counter()
    sig = backend.sign(data, pri, pub)
    sign_ms = (time.perf_counter() - t0) * 1000

    # 验签（正常）
    t0 = time.perf_counter()
    ok_normal = backend.verify(data, sig, pub)
    verify_ms = (time.perf_counter() - t0) * 1000

    cases = []
    cases.append({
        "name": "正常验签",
        "expected": True,
        "actual": bool(ok_normal),
        "sign_ms": round(sign_ms, 3),
        "verify_ms": round(verify_ms, 3),
    })

    # 篡改消息后验签
    msg_t = tamper_message(msg)
    data_t = pack_message(uid, msg_t)
    ok_tamper = backend.verify(data_t, sig, pub)
    cases.append({
        "name": "篡改消息后验签",
        "expected": False,
        "actual": bool(ok_tamper),
        "detail": {"tampered_message": msg_t[-80:]}  # 截断保存，避免太长
    })

    # 伪造签名：用别的私钥签同一消息，然后用原公钥验签
    pri2, pub2 = backend.generate_keypair()
    sig2 = backend.sign(data, pri2, pub2)
    ok_forge = backend.verify(data, sig2, pub)
    cases.append({
        "name": "伪造签名（他人私钥签）",
        "expected": False,
        "actual": bool(ok_forge),
    })

    # UID 不一致
    uid_bad = "0000000000000000"
    data_uid_bad = pack_message(uid_bad, msg)
    ok_uid = backend.verify(data_uid_bad, sig, pub)
    cases.append({
        "name": "User ID 不一致",
        "expected": False,
        "actual": bool(ok_uid),
        "detail": {"uid_bad": uid_bad}
    })

    # 随机性：同一消息同一私钥再签一次（签名应该不同，但都能验签）
    sig_again = backend.sign(data, pri, pub)
    ok_again = backend.verify(data, sig_again, pub)
    cases.append({
        "name": "签名随机性（同消息二次签名）",
        "expected": True,
        "actual": bool(ok_again),
        "detail": {
            "sig_equals": (sig_again == sig),
        }
    })

    return {
        "uid": uid,
        "message_len": len(msg),
        "message_preview": msg[:120],
        "cases": cases,
    }

def summarize(report):
    """生成汇总：每个用例通过率、耗时均值等。"""
    all_cases = {}
    sign_ms = []
    verify_ms = []
    for run in report["runs"]:
        for c in run["cases"]:
            all_cases.setdefault(c["name"], []).append((c["expected"], c["actual"]))
            if "sign_ms" in c:
                sign_ms.append(c["sign_ms"])
            if "verify_ms" in c:
                verify_ms.append(c["verify_ms"])

    summary = {"case_pass_rate": {}, "perf": {}}
    for name, pairs in all_cases.items():
        passed = sum(1 for e, a in pairs if e == a)
        summary["case_pass_rate"][name] = {
            "total": len(pairs),
            "passed": passed,
            "pass_rate": round(passed / len(pairs), 4)
        }

    if sign_ms:
        summary["perf"]["sign_ms_avg"] = round(mean(sign_ms), 3)
        summary["perf"]["sign_ms_max"] = round(max(sign_ms), 3)
    if verify_ms:
        summary["perf"]["verify_ms_avg"] = round(mean(verify_ms), 3)
        summary["perf"]["verify_ms_max"] = round(max(verify_ms), 3)

    return summary

def main():
    backend = get_backend()

    # 你可以改这些参数
    uid = "1234567812345678"
    rounds = 20                 # 批量轮数
    message_lengths = [64, 256, 1024]  # 不同消息长度做对比

    random.seed(20251231)

    report = {
        "backend": getattr(backend, "name", "unknown"),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "config": {
            "rounds": rounds,
            "message_lengths": message_lengths,
            "uid": uid,
        },
        "runs": []
    }

    for i in range(rounds):
        L = message_lengths[i % len(message_lengths)]
        msg = mk_message(L)
        run = run_one_suite(backend, uid, msg)
        run["round_index"] = i + 1
        report["runs"].append(run)

    report["summary"] = summarize(report)

    os.makedirs(ROOT / "data" / "logs", exist_ok=True)
    out_path = ROOT / "data" / "logs" / now_name("batch_report")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("=== Batch Test Done ===")
    print("backend:", report["backend"])
    print("output :", str(out_path))
    print("summary:", json.dumps(report["summary"], ensure_ascii=False))

if __name__ == "__main__":
    main()
