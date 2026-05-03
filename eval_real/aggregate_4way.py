"""Combine V0 self-scores with V1/V2/V3 prior blind scores into 4-way comparison."""
import json
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent

# Prior blind 3-way scores per case (V1/V2/V3) — from earlier blind eval
prior_scores = {
    "case_001": {"v1": 95, "v2": 95, "v3": 92},
    "case_002": {"v1": 95, "v2": 95, "v3": 98},
    "case_003": {"v1": 95, "v2": 98, "v3": 98},
    "case_004": {"v1": 94, "v2": 88, "v3": 96},
    "case_005": {"v1": 94, "v2": 98, "v3": 100},
    "case_006": {"v1": 64, "v2": 64, "v3": 98},
    "case_007": {"v1": 71, "v2": 61, "v3": 95},
    "case_008": {"v1": 84, "v2": 76, "v3": 80},
}

# V0 self-scored
with open(BASE / "v0_self_scored.json") as f:
    v0_data = json.load(f)

CASES = ["case_001", "case_002", "case_003", "case_004", "case_005", "case_006", "case_007", "case_008"]

# Combine
all_scores = {v: [] for v in ["v0", "v1", "v2", "v3"]}
case_table = []

for case in CASES:
    row = {"case": case,
           "v0": v0_data[case]["v0"]["total"],
           "v1": prior_scores[case]["v1"],
           "v2": prior_scores[case]["v2"],
           "v3": prior_scores[case]["v3"]}
    case_table.append(row)
    for v in ["v0", "v1", "v2", "v3"]:
        all_scores[v].append(row[v])

# Stats
print("=" * 70)
print("4-WAY COMPARISON: V0 (no SKILL) vs V1 vs V2 vs V3")
print("=" * 70)
print()
print(f"{'case':<10} {'V0':>5} {'V1':>5} {'V2':>5} {'V3':>5}  winner")
print("-" * 50)
for row in case_table:
    nums = [(row[v], v.upper()) for v in ["v0", "v1", "v2", "v3"]]
    winner = max(nums)[1]
    print(f"{row['case']:<10} {row['v0']:>5} {row['v1']:>5} {row['v2']:>5} {row['v3']:>5}  {winner}")

print()
print("PER-VERSION MEAN")
print("-" * 50)
for v in ["v0", "v1", "v2", "v3"]:
    s = all_scores[v]
    print(f"  {v.upper()}: mean={sum(s)/len(s):.1f}, min={min(s)}, max={max(s)}")

print()
print("HEAD-TO-HEAD (per case wins)")
print("-" * 50)
pairs = [("v1", "v0"), ("v2", "v0"), ("v3", "v0"),
         ("v2", "v1"), ("v3", "v1"), ("v3", "v2")]
for a, b in pairs:
    wins = sum(1 for r in case_table if r[a] > r[b])
    losses = sum(1 for r in case_table if r[a] < r[b])
    ties = sum(1 for r in case_table if r[a] == r[b])
    delta = sum(r[a] - r[b] for r in case_table) / len(case_table)
    print(f"  {a.upper()} vs {b.upper()}: {wins}W / {ties}T / {losses}L,  mean delta = {delta:+.1f}")

# Save CSV
with open(BASE / "scores_4way.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["case", "v0", "v1", "v2", "v3"], lineterminator="\n")
    writer.writeheader()
    for row in case_table:
        writer.writerow(row)

print(f"\nSaved scores_4way.csv to {BASE}")
