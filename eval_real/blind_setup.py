"""Generate random A/B/C blinding for each case, copy outputs."""
import random
import json
import shutil
import os
from pathlib import Path

random.seed(20260503)  # reproducible (new seed for 5-way to avoid leaking prior mappings)

CASES = ["case_001", "case_002", "case_003", "case_004", "case_005", "case_006", "case_007", "case_008"]
VERSIONS = ["v0", "v1", "v2", "v3", "v4"]
BASE = str(Path(__file__).resolve().parent)

global_mapping = {}

for case in CASES:
    # Find which versions exist for this case
    available = []
    for v in VERSIONS:
        src = f"{BASE}/runs/{case}/{v}_output.md"
        if os.path.exists(src):
            available.append(v)

    # Shuffle the available versions and assign letters
    letters = ["A", "B", "C", "D", "E"][:len(available)]
    shuffled = available.copy()
    random.shuffle(shuffled)

    # mapping: letter -> version
    mapping = dict(zip(letters, shuffled))

    # Copy files using mapping
    for letter, version in mapping.items():
        src = f"{BASE}/runs/{case}/{version}_output.md"
        dst = f"{BASE}/blinded/{case}/output_{letter}.md"
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(src, dst)

    # Save mapping (will be hidden during scoring)
    mapping_file = f"{BASE}/blinded/{case}/mapping.json"
    with open(mapping_file, "w") as f:
        json.dump(mapping, f, indent=2)

    global_mapping[case] = mapping
    print(f"{case}: {len(available)} outputs -> {sorted(letters)} (mapping hidden)")

# Save the global mapping in a separate file for later reveal
with open(f"{BASE}/blinded/_GLOBAL_MAPPING.json", "w") as f:
    json.dump(global_mapping, f, indent=2)

print("\nMapping saved (do not read until scoring complete).")
