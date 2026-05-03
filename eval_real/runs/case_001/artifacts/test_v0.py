"""Real test for case_001 V0 output."""
import re
from typing import List


def extract_emails(text: str) -> List[str]:
    if not isinstance(text, str) or not text:
        return []
    pattern = r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"
    return re.findall(pattern, text)


import json
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

print(json.dumps(results, indent=2))
