我会先把你的需求编译成一个执行 Brief，然后直接按这个 Brief 在当前环境执行。遇到关键决策或高风险动作时，我会先停下来问你。

## Compiled Task Brief

**Objective**
写一个 Python 函数，输入是 list[dict]，按每个 dict 的 `'age'` 字段降序排序；`'age'` 缺失（key 不存在或值为 None）的元素放到列表最后。

**Inputs**
- `items: list[dict]`：每个元素是 dict，可能包含 `'age'` 字段，类型通常为 int/float，也可能缺失或为 None。

**Scope**
- 只写一个纯函数，不做 I/O，不依赖外部库。
- 返回新列表，不修改原列表（避免副作用）。
- 排序稳定（Python `sorted` 默认稳定），相同 age 的元素保持原相对顺序；缺失 age 的元素之间也保持原相对顺序。

**Assumptions**
- `'age'` 存在时为可比较的数值（int/float）。
- "缺失" 包含两种情况：key 不存在 或 值为 None。
- 对非数值类型不做强制转换（保持简单、可预期）。

**Acceptance Criteria**
- 有 age 的元素按 age 从大到小排在前面。
- 无 age（缺失或 None）的元素全部排在后面，相对顺序保持稳定。
- 原输入列表不被修改。

**Verification**
- 提供示例数据并打印输出，肉眼校验顺序。

**What Not to Do**
- 不引入第三方依赖。
- 不就地修改入参。

## Execution

```python
from typing import Any


def sort_by_age_desc(items: list[dict]) -> list[dict]:
    """按 'age' 字段降序排序；'age' 缺失或为 None 的元素放在最后。

    - 不修改原列表，返回新列表。
    - 排序稳定：age 相同或同为缺失的元素，保持原相对顺序。

    Args:
        items: 字典列表，每个 dict 可能包含 'age' 字段。

    Returns:
        新的已排序列表。
    """

    def sort_key(d: dict) -> tuple[int, Any]:
        age = d.get("age")
        if age is None:
            # missing_flag=1 -> 排到后面；第二项给个占位值，不参与有效比较
            return (1, 0)
        # missing_flag=0 -> 排到前面；用 -age 实现降序（配合默认升序）
        return (0, -age)

    return sorted(items, key=sort_key)


if __name__ == "__main__":
    data = [
        {"name": "Alice", "age": 30},
        {"name": "Bob"},                 # 缺失 age
        {"name": "Cathy", "age": 25},
        {"name": "Dan", "age": None},    # age 为 None
        {"name": "Eve", "age": 42},
        {"name": "Frank", "age": 30},    # 与 Alice 同 age，验证稳定性
    ]

    result = sort_by_age_desc(data)
    for item in result:
        print(item)

    # 预期输出（顺序）：
    # {'name': 'Eve', 'age': 42}
    # {'name': 'Alice', 'age': 30}
    # {'name': 'Frank', 'age': 30}
    # {'name': 'Cathy', 'age': 25}
    # {'name': 'Bob'}
    # {'name': 'Dan', 'age': None}
```

**Notes**
- 关键技巧：`sorted` 的 key 返回 `(missing_flag, -age)` 元组。先按是否缺失分两组（0 在前、1 在后），再在有 age 的组内用 `-age` 实现降序。
- 如果你的 age 可能是字符串数字（如 `"30"`），需要先统一类型；目前实现假定为数值。
- 如果想要原地排序，可以把 `return sorted(...)` 改成 `items.sort(key=sort_key)`，但默认实现不修改入参更安全。
