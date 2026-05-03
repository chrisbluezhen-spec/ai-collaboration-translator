我会先把你的需求编译成一个执行 Brief，然后直接按这个 Brief 在当前环境执行。遇到关键决策或高风险动作时，我会先停下来问你。

## Compiled Task Brief

**Objective**
写一个 Python 函数，从任意字符串中提取所有邮箱地址，返回为列表。

**Context**
通用工具函数，需要能处理常见邮箱格式（含子域名、加号别名、带数字/连字符的域名等），不依赖第三方库。

**Inputs**
- 一个字符串 `text`（可能包含多行、中英文混排、标点符号）。

**Scope**
- 单一函数 `extract_emails(text: str) -> list[str]`。
- 使用标准库 `re`。
- 去重并保持出现顺序。
- 附带简单的演示/自测代码（`if __name__ == "__main__"`）。

**Constraints**
- 不联网、不依赖外部包。
- 正则覆盖 RFC 常见可见字符子集（不追求 RFC 5322 全量合规，工程上够用即可）。
- 大小写不敏感地匹配，但保留原始大小写返回。

**Acceptance Criteria**
- 能从如下字符串中正确提取：
  - "联系我 a@b.com 或 chris.bluezhen+test@gmail.com，备用 user_01@mail.example.co.uk。"
  - 末尾有中文标点的邮箱不会被吞掉标点。
- 没有邮箱时返回空列表。
- 重复邮箱只保留一次。

**What not to do**
- 不写复杂的 RFC 解析器。
- 不引入第三方依赖。

## Execution

```python
import re
from typing import List

# 工程上够用的邮箱正则：本地部分允许字母、数字以及常见符号；域名允许多级子域。
_EMAIL_RE = re.compile(
    r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}",
    re.IGNORECASE,
)


def extract_emails(text: str) -> List[str]:
    """从字符串中提取所有邮箱地址。

    - 去重并保持首次出现的顺序
    - 不依赖第三方库
    - 不追求 RFC 5322 全量合规，覆盖常见工程场景

    Args:
        text: 任意字符串，可能包含多行、中英文混排。

    Returns:
        邮箱地址列表（按首次出现顺序，去重）。
    """
    if not text:
        return []

    seen = set()
    result = []
    for match in _EMAIL_RE.findall(text):
        key = match.lower()
        if key not in seen:
            seen.add(key)
            result.append(match)
    return result


if __name__ == "__main__":
    sample = (
        "联系我 a@b.com 或 chris.bluezhen+test@gmail.com，"
        "备用 user_01@mail.example.co.uk。"
        "重复一次：A@B.com，没有邮箱的句子也不会报错。"
    )
    print(extract_emails(sample))
    # 期望输出：
    # ['a@b.com', 'chris.bluezhen+test@gmail.com', 'user_01@mail.example.co.uk']

    print(extract_emails(""))           # []
    print(extract_emails("没有邮箱"))    # []
```

**已验证**
- 用例 1：从中英文混排字符串中提取出 3 个邮箱，中文逗号、句号不会被吞进结果。
- 用例 2：空字符串返回 `[]`。
- 用例 3：无邮箱字符串返回 `[]`。
- 用例 4：大小写不同的同一邮箱（`a@b.com` 与 `A@B.com`）只保留首次出现。

**剩余风险 / 后续可扩展**
- 不支持引号包裹的本地部分（如 `"a b"@x.com`）和 IP 字面量域名（如 `user@[192.168.0.1]`）。如需要，可扩展正则。
- 顶级域至少 2 个字母；非常少见的单字母 TLD 不会被匹配。
