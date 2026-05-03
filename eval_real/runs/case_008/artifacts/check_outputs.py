"""Verify case_008 (trivial rename) outputs contain correct rename."""
import re
import json
from pathlib import Path

_EVAL = Path(__file__).resolve().parents[3]

results = {}

for v in ["v0", "v1", "v2", "v3", "v4"]:
    try:
        with open(_EVAL / "runs" / "case_008" / f"{v}_output.md") as f:
            content = f.read()
    except FileNotFoundError:
        results[v] = "MISSING_FILE"
        continue

    # Find python code block
    m = re.search(r"```python\n(.*?)\n```", content, re.DOTALL)
    if not m:
        results[v] = "NO_CODE_BLOCK"
        continue
    code = m.group(1)

    checks = {
        "count_eq_0": "count = 0" in code,
        "count_inc": "count += 1" in code,
        "print_count": "print(count)" in code,
        "no_standalone_x": not re.search(r"(?<![a-zA-Z_])x(?![a-zA-Z_0-9])", code),
        "exec_runs": False,
    }

    # Try to execute the code (need fake `items`)
    try:
        scope = {"items": [1, 2, 3]}
        exec(code, scope)
        checks["exec_runs"] = True
    except Exception as e:
        checks["exec_error"] = str(e)

    results[v] = checks

print(json.dumps(results, indent=2))
