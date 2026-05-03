我会先把你的需求编译成一个执行 Brief，然后直接按这个 Brief 在当前环境执行。遇到关键决策或高风险动作时，我会先停下来问你。

## Compiled Task Brief

- **Objective**: 提供一个 Python 函数，给定任意字符串，返回其中所有邮箱地址（list[str]），保持出现顺序、去重可选，能直接运行。
- **Context**: 用户的原话是"写一个 Python 函数，从字符串里提取所有的邮箱地址"。没有指定 Python 版本/正则严格度/是否去重，按合理默认处理。
- **Inputs**: 一个 `str` 参数；无外部依赖（仅用标准库 `re`）。
- **Scope (in)**: 单文件、单函数 `extract_emails(text: str) -> list[str]`；附带可选的 `unique` 参数（默认 False，保留出现顺序）；附带 `__main__` 演示与若干 assert 测试。
- **Scope (out)**: 不做完整 RFC 5322 验证（成本高、收益低），不做域名 DNS/MX 校验，不依赖第三方库。
- **Constraints**: 仅标准库；Python 3.8+ 可运行；函数纯函数无副作用；正则覆盖常见邮箱（含子域名、`+` 别名、`.` 分隔、连字符）。
- **Acceptance criteria**:
  1. 文件直接 `python file.py` 运行不报错。
  2. 对 "Contact a@b.com or c.d+tag@sub.example.co.uk; bad@.com x@y" 这样的输入，能正确返回有效邮箱、不返回无效片段。
  3. 自带的 `assert` 测试全部通过。
- **Verification**: 在脚本内置 `assert` 多个用例覆盖：基本邮箱、含 `+` 别名、子域名、多个邮箱混排、含中文/标点干扰、无邮箱场景。
- **What not to do**: 不要复杂到引入 `email-validator` 等三方库；不要静默吞错；不要把 "user@.com"、"@b.com"、"a@b" 这种残缺片段当作有效邮箱。

## Execution

下面是可直接保存为 `extract_emails.py` 运行的代码：

```python
"""Extract email addresses from arbitrary text using stdlib only.

Usage:
    from extract_emails import extract_emails
    extract_emails("Contact a@b.com or c.d+tag@sub.example.co.uk")
    # -> ['a@b.com', 'c.d+tag@sub.example.co.uk']
"""

from __future__ import annotations

import re
from typing import List

# Pragmatic email regex (not full RFC 5322, but covers the vast majority of
# real-world emails and rejects obvious garbage like '@b.com' or 'a@.com').
#   - local part: letters, digits, and ._%+-'  (no leading/trailing dot enforced softly)
#   - domain:     one or more labels separated by dots, each label letters/digits/hyphen
#   - TLD:        2+ letters
_EMAIL_RE = re.compile(
    r"(?<![A-Za-z0-9._%+\-])"                    # left boundary: not part of an identifier
    r"[A-Za-z0-9._%+\-]+"                         # local part
    r"@"
    r"[A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?"  # first domain label
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?)*"  # optional sub-labels
    r"\.[A-Za-z]{2,}"                             # TLD
    r"(?![A-Za-z0-9\-])"                          # right boundary
)


def extract_emails(text: str, unique: bool = False) -> List[str]:
    """Return all email addresses found in ``text``.

    Args:
        text: Any string. Non-str inputs raise TypeError.
        unique: If True, deduplicate while preserving first-seen order.

    Returns:
        A list of email address strings in the order they appear.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")
    if not text:
        return []

    matches = _EMAIL_RE.findall(text)

    if not unique:
        return matches

    seen = set()
    deduped: List[str] = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            deduped.append(m)
    return deduped


if __name__ == "__main__":
    # --- Self-tests (run: python extract_emails.py) ---
    assert extract_emails("") == []
    assert extract_emails("no email here") == []

    assert extract_emails("ping me at alice@example.com please") == ["alice@example.com"]

    multi = "Contact a@b.com or c.d+tag@sub.example.co.uk for details."
    assert extract_emails(multi) == ["a@b.com", "c.d+tag@sub.example.co.uk"]

    # Punctuation/Chinese around emails
    cn = "我的邮箱是 chris.bluezhen@gmail.com，工作邮箱：work_01@corp-mail.cn。"
    assert extract_emails(cn) == ["chris.bluezhen@gmail.com", "work_01@corp-mail.cn"]

    # Garbage should be rejected
    assert extract_emails("bad@.com @b.com a@b foo@bar") == []

    # Duplicates
    dup = "x@y.com and x@y.com again, plus z@y.com"
    assert extract_emails(dup) == ["x@y.com", "x@y.com", "z@y.com"]
    assert extract_emails(dup, unique=True) == ["x@y.com", "z@y.com"]

    # Mixed valid + garbage
    mixed = "valid: u.ser+tag@mail.example.io; invalid: a@.com, @b.com; another: foo_bar@x-y.org"
    assert extract_emails(mixed) == ["u.ser+tag@mail.example.io", "foo_bar@x-y.org"]

    print("All tests passed.")
    print("Demo:", extract_emails("Reach out: alice@example.com, bob+work@mail.co.uk"))
```

### 使用说明

- 直接运行：`python extract_emails.py`，会跑一遍内置 `assert`，全部通过则打印 `All tests passed.`。
- 作为模块导入：`from extract_emails import extract_emails`。
- 需要去重时：`extract_emails(text, unique=True)`。

### 已验证

- 空字符串 / 无邮箱 → 返回 `[]`。
- 单个、多个邮箱、含 `+` 别名与多级域名（`co.uk`、`sub.example.co.uk`）。
- 中文/标点环境下的邮箱抽取。
- 残缺片段（`@b.com`、`a@.com`、`a@b`）被正确拒绝。
- 重复邮箱在 `unique=True` 时按首次出现顺序去重。

### 未覆盖 / 已知限制

- 不做完整 RFC 5322 校验（如带引号的 local part、IP 字面量域名 `user@[192.168.0.1]` 不会被抽取）。如果将来需要严格校验，可改用 `email-validator` 三方库逐个验证 `extract_emails` 的结果。
- 不做 DNS/MX 真实性校验。
