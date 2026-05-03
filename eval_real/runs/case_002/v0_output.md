```python
from typing import Any


def sort_by_age_desc(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    按 'age' 字段降序排序字典列表，缺失 'age' 的字典放在最后。

    参数:
        items: 包含字典的列表，每个字典可能含有 'age' 字段。

    返回:
        排序后的新列表（不修改原列表）。
    """
    def sort_key(d: dict[str, Any]) -> tuple[int, float]:
        age = d.get("age")
        if age is None:
            # 缺失的放最后：第一关键字 1 排在 0 之后
            return (1, 0)
        # 取负数实现降序
        return (0, -float(age))

    return sorted(items, key=sort_key)


if __name__ == "__main__":
    data = [
        {"name": "Alice", "age": 30},
        {"name": "Bob"},
        {"name": "Carol", "age": 25},
        {"name": "Dave", "age": 40},
        {"name": "Eve"},
    ]

    result = sort_by_age_desc(data)
    for item in result:
        print(item)
    # 输出：
    # {'name': 'Dave', 'age': 40}
    # {'name': 'Alice', 'age': 30}
    # {'name': 'Carol', 'age': 25}
    # {'name': 'Bob'}
    # {'name': 'Eve'}
```
