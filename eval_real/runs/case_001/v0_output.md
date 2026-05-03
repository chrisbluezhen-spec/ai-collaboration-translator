下面是一个用正则表达式从字符串中提取所有邮箱地址的 Python 函数：

```python
import re
from typing import List


def extract_emails(text: str) -> List[str]:
    """
    从字符串中提取所有邮箱地址。

    参数:
        text: 任意字符串，可能包含零个或多个邮箱地址。

    返回:
        提取到的邮箱地址列表（按出现顺序，保留重复项）。
        如果想去重，可以对返回值再做 list(dict.fromkeys(...)) 处理。
    """
    if not isinstance(text, str) or not text:
        return []

    # 邮箱正则：
    # - 本地部分：字母、数字以及常见允许字符 ._%+-
    # - @ 后是域名：字母数字加 .-
    # - 顶级域名：至少 2 个字母
    pattern = r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"
    return re.findall(pattern, text)


if __name__ == "__main__":
    sample = """
    联系我们：
    - 工作邮箱: alice.work+filter@example.com
    - 个人邮箱: bob_123@mail.co.uk
    - 无效: not-an-email@、@nodomain.com、plainaddress
    重复出现: alice.work+filter@example.com
    """
    emails = extract_emails(sample)
    print(emails)
    # 去重（保留顺序）：
    print(list(dict.fromkeys(emails)))
```

说明：

- 使用 `re.findall` 一次性提取所有匹配项，时间复杂度与文本长度成线性。
- 这个正则覆盖了绝大多数常见邮箱格式，但并不完全等同于 RFC 5322 标准（RFC 完整规范非常复杂，正则会很长）。如果你需要更严格的校验，建议在提取后再用 `email.utils.parseaddr` 或第三方库（如 `email-validator`）做二次校验。
- 如果想忽略大小写或限制顶级域名长度，只要调整正则即可。比如把 `{2,}` 改成 `{2,24}` 可以避免匹配过长的伪 TLD。
