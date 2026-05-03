```python
import re

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

def extract_emails(text: str) -> list[str]:
    """从字符串里提取所有的邮箱地址，按出现顺序返回。"""
    return EMAIL_RE.findall(text)
```

用法示例：

```python
text = "联系我：alice@example.com 或 bob.lee+work@sub.domain.co；备用 carol_99@test.io。"
print(extract_emails(text))
# ['alice@example.com', 'bob.lee+work@sub.domain.co', 'carol_99@test.io']
```

正则覆盖了常见邮箱格式（含 `.`、`_`、`%`、`+`、`-` 等本地部分字符，以及多级域名）。如果你需要更严格地遵守 RFC 5322，或者要在去重、转小写、过滤特定域名等方向上加规则，告诉我一下我再调整。
