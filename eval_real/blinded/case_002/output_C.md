我会先把你的需求编译成一个执行 Brief，然后直接按这个 Brief 在当前环境执行。

## Compiled Task Brief

- **Objective**: 写一个 Python 函数，按字典中的 `'age'` 字段对列表降序排序；缺失 `'age'` 字段（key 不存在或值为 `None`）的元素一律放到列表末尾。
- **Context**: 通用工具函数，输入是 `list[dict]`，元素结构不固定，`'age'` 字段可能缺失或为 `None`。
- **Inputs**: 任意 `list[dict]`。
- **Scope**:
  - In: 排序逻辑、缺失值处理、不修改原列表（返回新列表）、保持稳定排序。
  - Out: 不做类型校验、不处理非 dict 元素、不递归处理嵌套结构。
- **Constraints**:
  - 使用标准库 `sorted`，O(n log n)。
  - 缺失定义为：`'age'` 不在 dict 中，或值为 `None`。
  - 非缺失但 age 值需可比较（int/float）。
- **Acceptance criteria**:
  - 输入 `[{'name':'A','age':30},{'name':'B'},{'name':'C','age':25},{'name':'D','age':None}]`
  - 输出顺序：A(30) → C(25) → B(missing) → D(None)
  - 原列表未被修改。
- **What not to do**:
  - 不要把缺失的 age 当成 0 排进中间。
  - 不要让 `None` 与 int 直接比较抛 `TypeError`。
  - 不要原地排序破坏调用方数据。

## Execution

```python
from typing import Any


def sort_by_age_desc(items: list[dict]) -> list[dict]:
    """按 'age' 字段降序排序，缺失或为 None 的放最后。

    - 不修改原列表，返回新列表。
    - 排序稳定：'age' 相同或同为缺失时，保持原相对顺序。
    """
    def key(item: dict) -> tuple[int, Any]:
        age = item.get("age")
        if age is None:
            # 缺失 / None 一律放最后：第一维 1 排在 0 之后
            return (1, 0)
        # 存在 age：第一维 0 在前；第二维取负值实现降序
        return (0, -age)

    return sorted(items, key=key)


if __name__ == "__main__":
    data = [
        {"name": "A", "age": 30},
        {"name": "B"},
        {"name": "C", "age": 25},
        {"name": "D", "age": None},
        {"name": "E", "age": 30},
    ]
    for row in sort_by_age_desc(data):
        print(row)
    # 期望输出顺序：A(30), E(30), C(25), B(missing), D(None)
```

### 说明

- `sorted` 是稳定排序，age 相同的元素（如 A、E）保持原顺序。
- 用元组 `(0/1, -age)` 作 key：第一维把"缺失组"压到末尾，第二维取负数把"非缺失组"变成降序，避免使用 `reverse=True` 同时影响两组的相对顺序。
- 若 age 可能是 `float`，逻辑同样适用；若可能是字符串数字，需要调用方先转成数值。
