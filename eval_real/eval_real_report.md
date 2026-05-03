# Real Isolated V1/V2/V3 Evaluation Report

**Date**: 2026-05-02
**Skill**: ai-collaboration-translator
**Method**: Isolated subagent execution + real code tests + blinded scoring + reveal

---

## 1. Real vs. Simulated

| Step | Real / Simulated | Evidence |
|------|------------------|----------|
| Output generation (V1/V2/V3 × 8 cases = 24 outputs) | **Real** | 24 fresh `general-purpose` subagents, each given only one SKILL file + raw prompt, isolated context. Outputs in `eval_real/runs/case_*/v*_output.md`. |
| Code execution (cases 001, 002, 008) | **Real** | Python tests in `eval_real/runs/case_*/artifacts/` actually ran. All 9 (3 versions × 3 code cases) passed all oracle assertions. |
| Blinding | **Real** | Deterministic Python script (seed=20260501) shuffled outputs to A/B/C labels. Mapping in `eval_real/blinded/_GLOBAL_MAPPING.json`, separate from outputs. |
| Scoring | **Real** | 8 fresh judge subagents (one per case), each saw only blinded outputs + oracle, did NOT see mapping. Scores in `eval_real/runs/case_*/scores.json`. |
| Aggregation | **Real** | Script revealed mapping and computed per-version totals. Output in `eval_real/scores.csv`, `aggregate_stats.json`. |

**No simulated scores in this report.** All numbers come from blinded judge agents reading actual generated outputs.

**Caveats**:
- Judge agents are also Claude (same model family). Independent third-party (different model) confirmation would strengthen the result.
- Judge agents were given the oracle text — they were not asked to discover what "good" means; only to score against pre-defined criteria.

---

## 2. What Was Saved Where

| Artifact | Path |
|----------|------|
| V1 outputs | `eval_real/runs/case_NNN/v1_output.md` (8 files) |
| V2 outputs | `eval_real/runs/case_NNN/v2_output.md` (8 files) |
| V3 outputs | `eval_real/runs/case_NNN/v3_output.md` (8 files) |
| Test runners | `eval_real/runs/case_001/artifacts/test_v{1,2,3}.py`, `case_002/artifacts/run_all.py`, `case_008/artifacts/check_outputs.py` |
| Blinded copies | `eval_real/blinded/case_NNN/output_{A,B,C}.md` |
| Mapping | `eval_real/blinded/_GLOBAL_MAPPING.json` |
| Per-case scores | `eval_real/runs/case_NNN/scores.json` |
| Aggregated CSV | `eval_real/scores.csv` |
| Stats JSON | `eval_real/aggregate_stats.json` |

---

## 3. Per-case Final Scores (after un-blinding)

| Case | Type | V1 | V2 | V3 | Winner |
|------|------|----|----|-----|--------|
| case_001 | code/algo (extract emails) | 95 | 95 | **92** | V1=V2 |
| case_002 | code/data (sort dicts) | 95 | 95 | **98** | V3 |
| case_003 | code/SBE (replace console.log) | 95 | 98 | **98** | V2=V3 |
| case_004 | high-risk safety (git push main) | 94 | 88 | **96** | V3 |
| case_005 | prompt-only (Cursor prompt) | 94 | 98 | **100** | V3 |
| case_006 | emotional (comfort message) | 64 | 64 | **98** | V3 |
| case_007 | REVERSE simple writing (slogan) | 71 | 61 | **95** | V3 |
| case_008 | REVERSE trivial code (rename) | **84** | 76 | 80 | V1 |
| **Mean** | | **86.5** | **84.4** | **94.6** | |

---

## 4. Head-to-head

| Comparison | Wins | Ties | Losses |
|------------|------|------|--------|
| V3 vs V1 | 6 | 0 | 2 |
| V3 vs V2 | 6 | 1 | 1 |
| V2 vs V1 | 2 | 3 | 3 |

---

## 5. Real Code Test Results

For 3 code cases, code was extracted from outputs and run with Python:

| Case | V1 | V2 | V3 |
|------|----|----|-----|
| case_001 (6 assertions) | 6/6 PASS | 6/6 PASS | 6/6 PASS |
| case_002 (5 assertions) | 5/5 PASS | 5/5 PASS | 5/5 PASS |
| case_008 (4 checks) | 4/4 PASS | 4/4 PASS | 4/4 PASS |

**Code correctness is equivalent across all 3 versions.** The score differences come from Brief overhead, scope discipline, and output framing.

---

## 6. Blinded A/B/C Mapping (revealed)

| Case | A | B | C |
|------|---|---|---|
| case_001 | V2 | V3 | V1 |
| case_002 | V1 | V2 | V3 |
| case_003 | V3 | V2 | V1 |
| case_004 | V3 | V2 | V1 |
| case_005 | V2 | V3 | V1 |
| case_006 | V3 | V2 | V1 |
| case_007 | V3 | V1 | V2 |
| case_008 | V3 | V1 | V2 |

The mapping was random and not consistent across cases — judges could not infer the version from position.

---

## 7. Answers to Required Questions

**Q1: Which cases were really executed, which only simulated?**
- All 24 V1/V2/V3 outputs: **really executed** (isolated subagents).
- Code tests for case_001, case_002, case_008: **really executed** (Python subprocess).
- case_003, case_004, case_005, case_006, case_007: not executable code — judged on text quality only.

**Q2: Where are each version's raw outputs?**
- `eval_real/runs/case_NNN/v1_output.md`, `v2_output.md`, `v3_output.md` for all 8 cases.

**Q3: Were any test commands actually run?**
- Yes. `python3 eval_real/runs/case_001/artifacts/test_v{1,2,3}.py`, `python3 eval_real/runs/case_002/artifacts/run_all.py`, `python3 eval_real/runs/case_008/artifacts/check_outputs.py`. All passed.

**Q4: What were the per-case A/B/C blind scores?**
- See `eval_real/scores.csv` and `eval_real/runs/case_NNN/scores.json`.

**Q5: After un-blinding, V1/V2/V3 final scores?**
- V1: mean 86.5, range 64-95
- V2: mean 84.4, range 61-98
- V3: mean 94.6, range 80-100

**Q6: Is V3 really better than V2?**
- **Yes**, by the available evidence. V3 wins 6/8, ties 1/8, loses 1/8 against V2. Mean +10.2 points. Largest gains: case_006 emotional (+34) and case_007 slogan (+34).

**Q7: Is V2 really better than V1?**
- **Not by this evaluation.** V2 wins 2/8, ties 3/8, loses 3/8 against V1. Mean −2.1 points. V2's stricter Quality Gate and 3-Layer extraction added Brief overhead that hurt scores on tasks like case_007 slogan, case_004 git push, and case_008 trivial rename.

**Q8: Any regressions?**
- **V3 regresses on case_001** (92 vs 95): minor, caused by V3 normalizing email output to lowercase (an opinionated default that surprised the judge).
- **V3 regresses on case_008 vs V1** (80 vs 84): V3 produced heavier Brief for a trivial 4-line rename — the reverse-case concern materialized.
- **V2 regresses vs V1 on cases 004, 007, 008**: Quality Gate / 3-Layer extraction overhead hurt on tasks needing less ceremony.

**Q9: Is the evidence sufficient to declare a winner?**
- **For V3 over V2: Yes.** 6/8 wins, mean +10.2, Light-Touch Mode demonstrably resolves emotional/creative cases.
- **For V3 over V1: Yes, with caveat.** 6/8 wins, mean +8.1, but V1 wins case_008 (REVERSE trivial). V3's edge is concentrated in emotional/safety/prompt-only cases.
- **For V2 over V1: NOT proven.** Evidence is mixed/negative.

---

## 8. Final Conclusion

**Recommended version: V3.**

Rationale:
1. Highest mean score (94.6 vs V1=86.5, V2=84.4)
2. Most consistent floor (min 80 vs V1=64, V2=61)
3. Wins on high-stakes cases: emotional (Light-Touch), high-risk safety (Action Risk Ladder), prompt-only (clean mode selection), code/data
4. Single regression (case_008 trivial rename, V3 lost by 4 points to V1) is acknowledged but does not outweigh the 6 wins

**V2 should NOT be considered an improvement over V1** based on this evaluation. The 3-Layer Intent Extraction and Quality Gate added Brief overhead that hurt on simple tasks. V3's additions (Light-Touch Mode, Action Risk Ladder, SBE Rule, TRC) are what actually deliver the value over V1.

**Known limitation in V3**: Reverse case_008 showed V3 over-structuring a trivial code rename. Recommended next improvement: add a "trivial task" exception to the Quality Gate (skip heavy Brief when the request is a self-contained micro-edit with all inputs in the prompt).

---

## 9. How to Reproduce

```bash
cd "$(git rev-parse --show-toplevel)" 2>/dev/null || cd /path/to/ai-collaboration-translator

ls eval_real/runs/case_*/

python3 eval_real/runs/case_001/artifacts/test_v1.py
python3 eval_real/runs/case_002/artifacts/run_all.py
python3 eval_real/runs/case_008/artifacts/check_outputs.py

python3 eval_real/aggregate.py

cat eval_real/blinded/case_006/output_A.md
```
