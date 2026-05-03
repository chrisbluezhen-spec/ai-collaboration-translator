"""Real test for case_001 V2 output."""
from __future__ import annotations
import re
from typing import List

# Code extracted verbatim from v2_output.md
_EMAIL_RE = re.compile(
    r"(?<![A-Za-z0-9._%+\-])"
    r"[A-Za-z0-9._%+\-]+"
    r"@"
    r"[A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?)*"
    r"\.[A-Za-z]{2,}"
    r"(?![A-Za-z0-9\-])"
)


def extract_emails(text: str, unique: bool = False) -> List[str]:
    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")
    if not text:
        return []
    matches = _EMAIL_RE.findall(text)
    if not unique:
        return matches
    seen = set()
    deduped: List[str] = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            deduped.append(m)
    return deduped


results = {}
try:
    assert extract_emails('') == [], "fail empty"
    results["empty"] = "PASS"
except Exception as e:
    results["empty"] = f"FAIL: {e}"

try:
    assert extract_emails('no email here') == [], "fail no-match"
    results["no_match"] = "PASS"
except Exception as e:
    results["no_match"] = f"FAIL: {e}"

try:
    res = extract_emails('a@b.com and c@d.org')
    assert len(res) == 2, f"got {res}"
    results["multi"] = "PASS"
except Exception as e:
    results["multi"] = f"FAIL: {e}"

try:
    res = extract_emails('a@b.com')
    assert res[0] == 'a@b.com', f"got {res}"
    results["single"] = "PASS"
except Exception as e:
    results["single"] = f"FAIL: {e}"

try:
    res = extract_emails('foo@bar')
    assert res == [], f"should reject 'foo@bar' but got {res}"
    results["no_tld_reject"] = "PASS"
except Exception as e:
    results["no_tld_reject"] = f"FAIL: {e}"

try:
    res = extract_emails('valid: a@b.com; invalid: a@.com, @b.com')
    assert 'a@b.com' in res, f"missing valid: {res}"
    assert '@b.com' not in res, f"included garbage: {res}"
    results["mixed"] = "PASS" if len(res) == 1 else f"PARTIAL: {res}"
except Exception as e:
    results["mixed"] = f"FAIL: {e}"

import json
print(json.dumps(results, indent=2))
