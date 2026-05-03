"""Real tests for case_002 V1/V2/V3 — same algorithm extracted from each output."""
from typing import Any
import json


def make_v1():
    def sort_by_age_desc(items):
        def sort_key(d):
            age = d.get("age")
            if age is None:
                return (1, 0)
            return (0, -age)
        return sorted(items, key=sort_key)
    return sort_by_age_desc


def make_v2():
    def sort_by_age_desc(data):
        def key(item):
            age = item.get("age")
            if age is None:
                return (1, 0)
            return (0, -age)
        return sorted(data, key=key)
    return sort_by_age_desc


def make_v3():
    def sort_by_age_desc(items):
        def key(item):
            age = item.get("age")
            if age is None:
                return (1, 0)
            return (0, -age)
        return sorted(items, key=key)
    return sort_by_age_desc


def make_v0():
    def sort_by_age_desc(items):
        def sort_key(d):
            age = d.get("age")
            if age is None:
                return (1, 0)
            return (0, -float(age))
        return sorted(items, key=sort_key)
    return sort_by_age_desc


def make_v4():
    def sort_by_age_desc(items):
        return sorted(items, key=lambda d: (0, -d['age']) if 'age' in d else (1, 0))
    return sort_by_age_desc


def run_oracle(fn):
    results = {}
    try:
        assert fn([]) == []
        results["empty"] = "PASS"
    except Exception as e:
        results["empty"] = f"FAIL: {e}"
    try:
        out = fn([{'age':10},{'age':30},{'age':20}])
        assert out == [{'age':30},{'age':20},{'age':10}], f"got {out}"
        results["desc_order"] = "PASS"
    except Exception as e:
        results["desc_order"] = f"FAIL: {e}"
    try:
        out = fn([{'age':30},{'name':'X'},{'age':10}])
        assert out[-1] == {'name':'X'}, f"got {out}"
        results["missing_last"] = "PASS"
    except Exception as e:
        results["missing_last"] = f"FAIL: {e}"
    try:
        out = fn([{'age':30},{'age':None},{'age':10}])
        assert out[-1] == {'age':None}, f"got {out}"
        results["none_last"] = "PASS"
    except Exception as e:
        results["none_last"] = f"FAIL: {e}"
    try:
        original = [{'age':30},{'name':'X'},{'age':10}]
        snapshot = list(original)
        fn(original)
        assert original == snapshot, "input mutated"
        results["no_mutate"] = "PASS"
    except Exception as e:
        results["no_mutate"] = f"FAIL: {e}"
    return results


for name, factory in [("V0", make_v0), ("V1", make_v1), ("V2", make_v2), ("V3", make_v3), ("V4", make_v4)]:
    print(f"=== {name} ===")
    print(json.dumps(run_oracle(factory()), indent=2))
