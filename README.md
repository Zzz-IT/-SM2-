
# 题目11：基于 SM2 的数字签名系统（Python 桌面 GUI）

本项目实现一个基于 SM2 的数字签名与验签系统，包含：
- PySide6 桌面 GUI：密钥管理、签名、验签
- tools 工具脚本：独立验证方案与批量测试（生成 JSON 报告，便于课程报告撰写）

---

## 目录结构（建议）

- app.py
- requirements.txt
- core/
- ui/
- tools/
  - __init__.py
  - validate_scheme.py
  - batch_test.py
- data/
  - logs/（运行验证脚本后自动生成）
  - keys/（可选：仅在实现密钥落盘/导入导出时才会出现）

---

## 环境要求

- Python 3.9+（建议 3.10/3.11）
- Windows / macOS / Linux 均可

---

## 安装（推荐使用虚拟环境）

### Windows（PowerShell）
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 推荐用“python -m pip”避免 pip 指向全局环境
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
````

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

如果安装依赖出现网络/SSL 报错，建议使用国内镜像：

```bash
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

---

## 运行 GUI

在项目根目录执行：

```bash
python app.py
```

GUI 操作建议流程：

1. 密钥管理：生成密钥对
2. 签名：输入消息并签名
3. 验签：填充上一次签名内容并验签（应成功）

---

## 工具脚本（推荐用 -m 方式运行）

说明：项目包含 `tools/__init__.py`，因此建议使用模块方式运行，避免导入路径问题。

### 1）独立验证方案（生成 JSON 报告）

运行：

```bash
python -m tools.validate_scheme
```

输出：

* 控制台：每个用例 PASS/FAIL
* 报告文件：`data/logs/validation_report_*.json`

用例包括（期望行为）：

* 正常验签：应通过
* 篡改消息后验签：应失败
* 伪造签名/公钥不匹配：应失败
* User ID 不一致：应失败
* （可选加分）重放风险说明：同一消息+签名重复验证仍可通过（提示需 nonce/timestamp/序列号防重放）

### 2）批量测试（生成 JSON 报告 + 性能统计）

运行：

```bash
python -m tools.batch_test
```

输出：

* 报告文件：`data/logs/batch_report_*.json`
* 控制台：summary（通过率、平均/最大耗时等）

---

## 输出文件说明

* `data/logs/`：验证方案与批量测试产生的 JSON 报告（可作为报告实验数据来源）
* `data/keys/`：可选目录（仅在实现密钥落盘/导入导出时才会出现）

---

## 常见问题

### Q1：运行 tools 脚本报 `ModuleNotFoundError: No module named 'core'`

A：请使用模块方式运行：

```bash
python -m tools.validate_scheme
python -m tools.batch_test
```

### Q2：依赖安装失败（SSL / EOF / Timeout）

A：换镜像并提高超时重试：

```bash
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn --timeout 120 --retries 10
```

### Q3：依赖装到全局环境导致“卸不干净”

A：建议始终使用虚拟环境，并用以下方式安装，避免 pip 指向全局：

```bash
python -m pip install -r requirements.txt
```

---

## 课程报告建议材料（最小闭环）

* GUI 截图：生成密钥、签名成功、验签成功
* 验证方案输出：`validation_report_*.json` + 控制台 PASS 截图
* 批量测试输出：`batch_report_*.json`（通过率 + 性能统计表）

```

如果你希望 README 里加入“**提交清单**”（比如需要提交哪些源码文件/截图/报告 JSON），我也可以按你老师要求的格式再补一版。
```
=======
# 题目11：基于 SM2 的数字签名系统（Python 桌面 GUI）

本项目实现一个基于 SM2 的数字签名与验签系统，包含：
- PySide6 桌面 GUI：密钥管理、签名、验签
- tools 工具脚本：独立验证方案与批量测试（生成 JSON 报告，便于课程报告撰写）

---

## 目录结构（建议）

- app.py
- requirements.txt
- core/
- ui/
- tools/
  - __init__.py
  - validate_scheme.py
  - batch_test.py
- data/
  - logs/（运行验证脚本后自动生成）
  - keys/（可选：仅在实现密钥落盘/导入导出时才会出现）

---

## 环境要求

- Python 3.9+（建议 3.10/3.11）
- Windows / macOS / Linux 均可

---

## 安装（推荐使用虚拟环境）

### Windows（PowerShell）
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 推荐用“python -m pip”避免 pip 指向全局环境
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
````

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

如果安装依赖出现网络/SSL 报错，建议使用国内镜像：

```bash
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

---

## 运行 GUI

在项目根目录执行：

```bash
python app.py
```

GUI 操作建议流程：

1. 密钥管理：生成密钥对
2. 签名：输入消息并签名
3. 验签：填充上一次签名内容并验签（应成功）

---

## 工具脚本（推荐用 -m 方式运行）

说明：项目包含 `tools/__init__.py`，因此建议使用模块方式运行，避免导入路径问题。

### 1）独立验证方案（生成 JSON 报告）

运行：

```bash
python -m tools.validate_scheme
```

输出：

* 控制台：每个用例 PASS/FAIL
* 报告文件：`data/logs/validation_report_*.json`

用例包括（期望行为）：

* 正常验签：应通过
* 篡改消息后验签：应失败
* 伪造签名/公钥不匹配：应失败
* User ID 不一致：应失败
* （可选加分）重放风险说明：同一消息+签名重复验证仍可通过（提示需 nonce/timestamp/序列号防重放）

### 2）批量测试（生成 JSON 报告 + 性能统计）

运行：

```bash
python -m tools.batch_test
```

输出：

* 报告文件：`data/logs/batch_report_*.json`
* 控制台：summary（通过率、平均/最大耗时等）

---

## 输出文件说明

* `data/logs/`：验证方案与批量测试产生的 JSON 报告（可作为报告实验数据来源）
* `data/keys/`：可选目录（仅在实现密钥落盘/导入导出时才会出现）

---

## 常见问题

### Q1：运行 tools 脚本报 `ModuleNotFoundError: No module named 'core'`

A：请使用模块方式运行：

```bash
python -m tools.validate_scheme
python -m tools.batch_test
```

### Q2：依赖安装失败（SSL / EOF / Timeout）

A：换镜像并提高超时重试：

```bash
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn --timeout 120 --retries 10
```

### Q3：依赖装到全局环境导致“卸不干净”

A：建议始终使用虚拟环境，并用以下方式安装，避免 pip 指向全局：

```bash
python -m pip install -r requirements.txt
```

---

## 课程报告建议材料（最小闭环）

* GUI 截图：生成密钥、签名成功、验签成功
* 验证方案输出：`validation_report_*.json` + 控制台 PASS 截图
* 批量测试输出：`batch_report_*.json`（通过率 + 性能统计表）


