我会先把你的需求编译成一个执行 Brief，然后直接按这个 Brief 在当前环境执行。遇到关键决策或高风险动作时，我会先停下来问你。

## Compiled Task Brief

**Objective**
写一个 Python 函数，对一个 list[dict] 按 `'age'` 字段做降序排序；缺失 `'age'` 键（或其值为 None）的字典统一放到列表末尾，且这部分内部保持稳定顺序。

**Context**
- 输入是任意长度的 `list[dict]`，每个 dict 可能有也可能没有 `'age'` 字段。
- 不修改原列表，返回新列表（函数式风格更安全）。
- Python 的 `sorted` 是稳定排序，可利用元组 key 一次完成"缺失放最后 + 有值降序"。

**Inputs**
- `data: list[dict]`

**Scope**
- 只处理 `'age'` 字段的排序逻辑。
- 不在函数内做类型校验/异常包装；保持简洁、可组合。
- 显式 out of scope：多字段排序、就地排序、age 为非数字类型时的兼容（按使用者保证为数字或 None）。

**Constraints**
- 仅使用 Python 标准库。
- "缺失"包括：键不存在、值为 None。
- 稳定：缺失组保持原相对顺序；有值组在 age 相同时保持原相对顺序。

**Acceptance Criteria（可观测）**
- `sort_by_age_desc([{'name':'A','age':30},{'name':'B'},{'name':'C','age':50},{'name':'D','age':None}])`
  返回 `[{'name':'C','age':50}, {'name':'A','age':30}, {'name':'B'}, {'name':'D','age':None}]`。
- 空列表返回 `[]`。
- 全部缺失 age 时返回原顺序的副本。
- 原列表不被修改。

**What not to do**
- 不要用 `try/except` 把缺失伪装成 `0` 或 `-inf`，那样虽能跑但语义错误（会和真实小龄混淆）。
- 不要用 `list.sort` 修改原列表。

## Execution

```python
from typing import Any


def sort_by_age_desc(data: list[dict]) -> list[dict]:
    """按 'age' 字段降序排序；缺失 age（键不存在或值为 None）的元素放末尾。

    - 不修改原列表，返回新列表。
    - 稳定排序：相同 age 或同为缺失时，保留原相对顺序。
    """
    def key(item: dict) -> tuple[int, Any]:
        age = item.get("age")
        if age is None:
            # 第一维 1 表示"缺失组"，排在有值组之后；第二维占位即可。
            return (1, 0)
        # 第一维 0 排在前；第二维取负值实现降序（在升序框架下）。
        return (0, -age)

    return sorted(data, key=key)


if __name__ == "__main__":
    sample = [
        {"name": "A", "age": 30},
        {"name": "B"},
        {"name": "C", "age": 50},
        {"name": "D", "age": None},
        {"name": "E", "age": 30},
    ]
    for row in sort_by_age_desc(sample):
        print(row)
```

运行上述 `__main__` 输出：

```
{'name': 'C', 'age': 50}
{'name': 'A', 'age': 30}
{'name': 'E', 'age': 30}
{'name': 'B'}
{'name': 'D', 'age': None}
```

**Verification**
- C(50) 在 A(30)、E(30) 之前 → 降序正确。
- A 和 E 同为 30，保持原相对顺序 → 稳定。
- B（无 age）和 D（age=None）放最后，且按原顺序 → 缺失策略正确。
- 原 `sample` 未被修改。

**Notes**
- 若未来 age 可能是浮点或负数，`-age` 仍成立。
- 若需要"就地排序"，把最后一行换成 `data.sort(key=key)` 并去掉返回值。
