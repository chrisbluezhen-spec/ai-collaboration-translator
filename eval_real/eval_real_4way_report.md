# 4-Way Real Isolated Evaluation Report (V0/V1/V2/V3) — FULLY BLIND VERSION

**Date**: 2026-05-03
**Skill**: ai-collaboration-translator
**Method**: Same logic for all 4 versions: isolated subagent generation + real code tests + 8 independent blind judge subagents (4-way A/B/C/D)

---

## 0. Why This Report Replaces the Earlier One

The previous 4-way report had a methodology asymmetry: V1/V2/V3 were scored by independent blind subagent judges, but V0 was scored by me (parent agent, non-blind). This violated the user's requirement of "same logic for all versions."

This report fixes that. **All 4 versions are now scored by the same method**: 8 independent judge subagents, each seeing only blinded A/B/C/D outputs and the oracle, with no knowledge of which version is which.

---

## 1. Final 4-Way Blind Scores

| Case | Type | V0 | V1 | V2 | V3 | Winner |
|------|------|----|----|----|-----|--------|
| case_001 | code/algo (extract emails) | **97** | 93 | 92 | 90 | V0 |
| case_002 | code/data (sort dicts) | **100** | 93 | 91 | 93 | V0 |
| case_003 | code/SBE (replace console.log) | 70 | 95 | **99** | 97 | V2 |
| case_004 | high-risk (git push main) | 91 | 94 | 92 | **98** | V3 |
| case_005 | prompt-only (Cursor prompt) | 79 | 93 | **98** | 97 | V2 |
| case_006 | emotional (comfort message) | **96** | 48 | 49 | 91 | V0 |
| case_007 | REVERSE (slogan) | 82 | 55 | 45 | **93** | V3 |
| case_008 | REVERSE (trivial rename) | **100** | 53 | 47 | 52 | V0 |
| **Mean** | | **89.4** | 78.0 | 76.6 | **88.9** | |

---

## 2. Head-to-head (4-way blind)

| Comparison | Mean Delta | Wins / Ties / Losses |
|------------|-----------|---------------------|
| V1 vs V0 | **−11.4** | 3W / 0T / 5L |
| V2 vs V0 | **−12.8** | 3W / 0T / 5L |
| **V3 vs V0** | **−0.5** | **4W / 0T / 4L** |
| V2 vs V1 | −1.4 | 3 / 0 / 5 |
| V3 vs V1 | **+10.9** | 5 / 1 / 2 |
| V3 vs V2 | **+12.2** | 5 / 0 / 3 |

---

## 3. The Core Finding (Different From Prior Report)

**V3 is statistically tied with V0** (no SKILL at all): 4-way blind judges produced 4 wins / 0 ties / 4 losses with mean delta −0.5.

This is a stronger and more honest result than the previous mixed-method report (which had V3 winning by +2.1 over a self-scored V0). When the same blind methodology is applied to all 4 versions, V3's edge over the no-SKILL baseline disappears within noise.

**However:**
- V3 still clearly beats V1 (+10.9) and V2 (+12.2)
- V0 clearly beats V1 (+11.4) and V2 (+12.8)
- V1 and V2 are NOT improvements over the no-SKILL baseline

---

## 4. Differences vs. the Previous Report

### Methodology fix
| | Previous report | This report |
|--|----------------|-------------|
| V1/V2/V3 scoring | Blind subagent judges (3-way) | Blind subagent judges (4-way) |
| V0 scoring | **Parent agent self-scored** (non-blind) | **Blind subagent judge** (4-way) |
| Test cases | Same 8 | Same 8 |
| Outputs scored | Same 32 (V0/V1/V2/V3 × 8) | Same 32 |

### Score differences (per version mean)

| Version | Previous (3-way blind + self V0) | Current (4-way blind) | Δ |
|---------|----------------------------------|----------------------|---|
| V0 | 92.5 (self-scored) | **89.4** (blind) | −3.1 |
| V1 | 86.5 | **78.0** | −8.5 |
| V2 | 84.4 | **76.6** | −7.8 |
| V3 | 94.6 | **88.9** | −5.7 |

### Why all scores dropped in 4-way blind

When V0 (clean, minimal baseline) is in the mix, judges have a concrete reference for "what minimal looks like" and apply the rubric's scope-control penalty more aggressively to heavy-Brief versions.

The biggest drops are on **reverse / emotional cases**:

| Case | Old V1 | New V1 | Δ | Old V2 | New V2 | Δ | Old V3 | New V3 | Δ |
|------|--------|--------|---|--------|--------|---|--------|--------|---|
| case_006 emotional | 64 | 48 | −16 | 64 | 49 | −15 | 98 | 91 | −7 |
| case_007 slogan | 71 | 55 | −16 | 61 | 45 | −16 | 95 | 93 | −2 |
| case_008 trivial | 84 | 53 | **−31** | 76 | 47 | −29 | 80 | 52 | −28 |

**Most striking**: case_008 V3 dropped from 80 to 52. The blind judge scored V3's heavy "Compiled Task Brief" for a 4-line variable rename particularly harshly when V0's clean 4-line code response was visible alongside.

### Per-case winner changes

| Case | Previous winner | New winner |
|------|----------------|-----------|
| case_001 | V0=V1=V2 (95) | **V0** (97, V1=93, V2=92, V3=90) |
| case_002 | V3 (98) | **V0** (100, V3 dropped to 93) |
| case_003 | V2=V3 (98) | **V2** alone (V2=99, V3=97) |
| case_004 | V3 (96) | V3 (98) — same |
| case_005 | V3 (100) | **V2** (98 vs V3=97) |
| case_006 | V3 (98) | **V0** (96 vs V3=91) |
| case_007 | V3 (95) | V3 (93) — same |
| case_008 | V0 (100) | V0 (100) — same |

V3 was previous winner in 6/8 cases; in fully blind it wins 2/8 outright (case_004, case_007). V0 wins 4/8 outright. V2 wins 2/8.

---

## 5. Direct Answers (Updated)

**Q: Is V0 (no SKILL) actually worse than V1/V2/V3?**
- vs V1: NO — V0 beats V1 by +11.4 points (5/8 cases).
- vs V2: NO — V0 beats V2 by +12.8 points (5/8 cases).
- vs V3: TIED — mean delta −0.5, splits 4/4 wins.

**Q: Does the SKILL provide positive value at all?**
- V1, V2: Net negative vs no SKILL.
- V3: Statistically tied with no SKILL on average; wins concentrated in safety + prompt-only cases, loses concentrated in trivial/emotional/code cases.

**Q: Where does V3 actually beat V0?**
- case_004 (high-risk safety): V3=98, V0=91 (+7) — Action Risk Ladder helps
- case_005 (prompt-only): V3=97, V0=79 (+18) — structured Prompt-Only mode wins
- case_007 (slogan): V3=93, V0=82 (+11) — V3 surprisingly more concise here
- case_003 (SBE replace): V3=97, V0=70 (+27) — V3's scope discrimination on tests/ is the biggest single win

**Q: Where does V0 beat V3?**
- case_008 (trivial rename): V0=100, V3=52 (−48) — V3's Brief is wrong for this
- case_001 (extract emails): V0=97, V3=90 (−7) — V3's lowercase normalization
- case_002 (sort dicts): V0=100, V3=93 (−7) — Brief overhead
- case_006 (comfort message): V0=96, V3=91 (−5) — V0 already produces friend-tone naturally

**Q: Why does V2 lose to V0?**
- V2 added stricter Quality Gate / 3-Layer Extraction → heavier Brief structures
- On simple/trivial/emotional tasks, this overhead is friction without benefit
- V2 has no Light-Touch escape hatch
- Result: V2 mean=76.6 vs V0=89.4

**Q: Why is V3 only tied with V0 in fully blind eval, when prior reports showed V3 winning?**
- Prior reports either: (1) compared only V1/V2/V3 (no V0 baseline), or (2) used self-scored V0 which I scored slightly higher than the blind judges
- The fully blind 4-way comparison is the cleanest signal: V3's wins on safety/prompt-only (+7 to +27) are real, but V3's losses on trivial/emotional code (−5 to −48) are also real, and they roughly cancel out

---

## 6. Final Recommendation (Updated)

**Ship V3 over V1/V2** — clear evidence (V3 wins by +10.9 vs V1, +12.2 vs V2).

**Ship V3 over V0 — only conditionally**. The 4-way blind evidence is:
- V3 wins 4/8, ties 0/8, loses 4/8 vs V0
- Mean delta −0.5 (within noise)
- V3's wins are on important high-risk safety cases (push, prompt-only, scope discrimination)
- V3's losses are on simple/trivial cases that don't typically cause real harm

The honest framing: **if you primarily encounter safety-critical, scope-discriminating, or prompt-only tasks, ship V3. If you primarily encounter simple code/emotional/trivial tasks, V3 will hurt user experience compared to no SKILL.**

The biggest known gap (case_008 trivial rename, V3 −48 vs V0) is a **clear next-improvement target**: V3 needs a "trivial task / micro-edit" exception that suppresses the Brief, parallel to Light-Touch Mode for emotional content.

---

## 7. Reproduce

```bash
# 仓库根目录与 SKILL.md、eval_real/ 同级
cd "$(git rev-parse --show-toplevel)" 2>/dev/null || cd /path/to/ai-collaboration-translator

# All raw outputs (例：5-way 为 40 个 v0–v4 × 8 cases；4-way 为 32 个)
ls eval_real/runs/case_*/v*_output.md

# Real code tests（按需增删版本号）
for v in v0 v1 v2 v3; do python3 eval_real/runs/case_001/artifacts/test_${v}.py; done
python3 eval_real/runs/case_001/artifacts/test_v4.py 2>/dev/null || true
python3 eval_real/runs/case_002/artifacts/run_all.py
python3 eval_real/runs/case_008/artifacts/check_outputs.py

# Blind aggregation（脚本内 BASE 为脚本所在 eval_real/）
python3 eval_real/aggregate.py

cat eval_real/runs/case_NNN/scores.json
cat eval_real/scores.csv
cat eval_real/blinded/_GLOBAL_MAPPING.json
```
