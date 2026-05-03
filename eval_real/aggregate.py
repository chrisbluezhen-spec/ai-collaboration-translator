"""Reveal mapping, aggregate per-version scores, output scores.csv and stats."""
import json
import csv
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent
CASES = ["case_001", "case_002", "case_003", "case_004", "case_005",
         "case_006", "case_007", "case_008"]

# Load global mapping
with open(BASE / "blinded" / "_GLOBAL_MAPPING.json") as f:
    global_mapping = json.load(f)

# Per-version score collection
version_scores = {"v0": [], "v1": [], "v2": [], "v3": [], "v4": []}
case_table = []

for case in CASES:
    scores_file = BASE / "runs" / case / "scores.json"
    if not scores_file.exists():
        print(f"WARNING: {case} scores missing")
        continue
    with open(scores_file) as f:
        raw = json.load(f)

    # Handle nested vs flat format
    if "scores" in raw and isinstance(raw["scores"], dict):
        scores = raw["scores"]
    else:
        scores = raw

    mapping = global_mapping[case]  # letter -> version
    row = {"case": case}
    for letter, version in mapping.items():
        if letter in scores:
            sc = scores[letter]
            total = sc.get("total")
            # field name normalization
            oracle = sc.get("oracle_hit", sc.get("oracle_goal_hit", 0))
            correct = sc.get("correctness", sc.get("correctness_safety", 0))
            usable = sc.get("usability", 0)
            scope = sc.get("scope", sc.get("scope_control", 0))
            if total is None:
                total = oracle + correct + usable + scope
            row[f"{version}_total"] = total
            row[f"{version}_oracle"] = oracle
            row[f"{version}_correct"] = correct
            row[f"{version}_usable"] = usable
            row[f"{version}_scope"] = scope
            row[f"{version}_notes"] = sc.get("notes", "")
            version_scores[version].append(total)
    case_table.append(row)

# Save scores.csv
with open(BASE / "scores.csv", "w", newline="") as f:
    fieldnames = ["case",
                  "v0_total", "v0_oracle", "v0_correct", "v0_usable", "v0_scope",
                  "v1_total", "v1_oracle", "v1_correct", "v1_usable", "v1_scope",
                  "v2_total", "v2_oracle", "v2_correct", "v2_usable", "v2_scope",
                  "v3_total", "v3_oracle", "v3_correct", "v3_usable", "v3_scope",
                  "v4_total", "v4_oracle", "v4_correct", "v4_usable", "v4_scope",
                  "v0_notes", "v1_notes", "v2_notes", "v3_notes", "v4_notes"]
    writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in case_table:
        writer.writerow({k: row.get(k, "") for k in fieldnames})

# Aggregate stats
stats = {}
for v in ["v0", "v1", "v2", "v3", "v4"]:
    scores = version_scores[v]
    if scores:
        stats[v] = {
            "n": len(scores),
            "mean": sum(scores) / len(scores),
            "min": min(scores),
            "max": max(scores),
            "scores": scores,
        }

# Per-case head-to-head (V0 included)
h2h = {}
pairs = [("v1","v0"), ("v2","v0"), ("v3","v0"), ("v4","v0"),
         ("v2","v1"), ("v3","v1"), ("v4","v1"),
         ("v3","v2"), ("v4","v2"),
         ("v4","v3")]
for a, b in pairs:
    wins = sum(1 for r in case_table if a+"_total" in r and b+"_total" in r and r[a+"_total"] > r[b+"_total"])
    losses = sum(1 for r in case_table if a+"_total" in r and b+"_total" in r and r[a+"_total"] < r[b+"_total"])
    ties = sum(1 for r in case_table if a+"_total" in r and b+"_total" in r and r[a+"_total"] == r[b+"_total"])
    deltas = [r[a+"_total"] - r[b+"_total"] for r in case_table if a+"_total" in r and b+"_total" in r]
    h2h[f"{a}_vs_{b}"] = {"W": wins, "T": ties, "L": losses,
                          "mean_delta": round(sum(deltas)/len(deltas), 2) if deltas else 0}

print("=" * 60)
print("PER-VERSION AGGREGATE")
print("=" * 60)
for v, s in stats.items():
    print(f"{v.upper()}: n={s['n']}, mean={s['mean']:.1f}, min={s['min']}, max={s['max']}, scores={s['scores']}")

print()
print("=" * 60)
print("HEAD-TO-HEAD")
print("=" * 60)
for k, v in h2h.items():
    print(f"  {k}: W={v['W']}/T={v['T']}/L={v['L']}, mean delta={v['mean_delta']:+.1f}")

print()
print("=" * 60)
print("PER-CASE TABLE")
print("=" * 60)
print(f"{'case':<10} {'v0':>5} {'v1':>5} {'v2':>5} {'v3':>5} {'v4':>5}  winner")
for row in case_table:
    v0 = row.get("v0_total", "-")
    v1 = row.get("v1_total", "-")
    v2 = row.get("v2_total", "-")
    v3 = row.get("v3_total", "-")
    v4 = row.get("v4_total", "-")
    nums = [(x, n) for x, n in [(v0,"v0"), (v1,"v1"), (v2,"v2"), (v3,"v3"), (v4,"v4")] if isinstance(x, (int, float))]
    if nums:
        winner_n, winner_v = max(nums)
        winner = winner_v
    else:
        winner = "?"
    print(f"{row['case']:<10} {str(v0):>5} {str(v1):>5} {str(v2):>5} {str(v3):>5} {str(v4):>5}  {winner}")

# Save stats
with open(BASE / "aggregate_stats.json", "w") as f:
    json.dump({"stats": stats, "h2h": h2h, "case_table": case_table,
               "global_mapping": global_mapping}, f, indent=2)

print(f"\nSaved scores.csv and aggregate_stats.json to {BASE}")
