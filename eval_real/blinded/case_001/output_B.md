我会先把你的需求编译成一个执行 Brief，然后直接按这个 Brief 在当前环境执行。遇到关键决策或高风险动作时，我会先停下来问你。

## Compiled Task Brief

- **Objective**: 写一个 Python 函数，从任意字符串中提取所有邮箱地址，返回去重并保持出现顺序的列表。
- **Context**: 通用工具函数，独立可运行，无外部依赖（仅用标准库 `re`）。
- **Inputs**: 任意 `str`，可能包含 0 个或多个邮箱、混合中英文、标点、换行。
- **Scope**:
  - In: 提取符合 RFC 5322 常见子集的邮箱（local-part 允许字母数字与 `._%+-`，domain 允许字母数字与 `.-`，TLD 至少 2 位字母）。
  - Out: 不做 DNS/MX 校验，不解析国际化域名（IDN/Punycode），不做大小写归一化以外的修复。
- **Constraints**:
  - 只用标准库。
  - 函数签名清晰，含 docstring 与类型注解。
  - 大小写不敏感匹配，但返回小写形式以便去重。
- **Acceptance criteria**:
  - `extract_emails("联系 a@x.com 或 B@X.COM, c.d+tag@sub.example.co.uk; 不是邮箱: foo@bar")` 返回 `['a@x.com', 'b@x.com', 'c.d+tag@sub.example.co.uk']`。
  - `extract_emails("")` 返回 `[]`。
  - 同一邮箱多次出现只保留第一次出现的位置。
- **What not to do**:
  - 不要把不带 TLD 的 `foo@bar` 也算作邮箱。
  - 不要破坏出现顺序。
  - 不要引入第三方库。

## Execution

```python
import re
from typing import List

# local-part: 字母数字加常见符号；domain: 至少一个点，TLD >= 2 位字母
_EMAIL_RE = re.compile(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    re.IGNORECASE,
)


def extract_emails(text: str) -> List[str]:
    """从字符串中提取所有邮箱地址。

    规则：
    - 大小写不敏感匹配，统一返回小写。
    - 去重，但保留首次出现顺序。
    - 不做 DNS/MX 校验，仅做语法层面的常见子集匹配。

    Args:
        text: 任意字符串。

    Returns:
        去重后的邮箱列表，按首次出现顺序排列。
    """
    if not text:
        return []

    seen = set()
    result: List[str] = []
    for match in _EMAIL_RE.findall(text):
        email = match.lower()
        if email not in seen:
            seen.add(email)
            result.append(email)
    return result


if __name__ == "__main__":
    sample = (
        "请联系 a@x.com 或 B@X.COM，"
        "也可以发到 c.d+tag@sub.example.co.uk；"
        "这不是邮箱: foo@bar，重复的 a@x.com 会被忽略。"
    )
    print(extract_emails(sample))
    # 预期输出: ['a@x.com', 'b@x.com', 'c.d+tag@sub.example.co.uk']
```

### 自检

- 空字符串 -> `[]`：命中 `if not text` 早退。
- 大小写不同的同一邮箱：`.lower()` + `seen` 去重。
- `foo@bar`：正则要求 `\.[A-Za-z]{2,}`，被正确排除。
- 顺序：用 `list` 而非 `set` 保留首次出现顺序。
