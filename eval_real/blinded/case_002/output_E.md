```python
def sort_by_age_desc(items):
    return sorted(items, key=lambda d: (0, -d['age']) if 'age' in d else (1, 0))
```

排序键用 `(0, -age)` / `(1, 0)` 两段：有 `age` 的按降序排，缺 `age` 的归到后段，自然落到最后；同时保持稳定排序。
