# Failure Modes

## Documented Regressions

### B02 — Apology Email (Pre-Light-Touch Fix)

**Status**: Regression in prior evaluation; resolved in v3 with Light-Touch Mode.

**Root cause**: The Skill's Compile-then-Execute Mode produced a visible, structured Compiled Task Brief that caused the downstream Agent to generate a corporate-sounding, bullet-heavy apology letter. The user wanted something sincere and personal; the structure signaled formality to the Agent.

**Oracle score**: Baseline 65 → Skill 60 → Uplift −5 (regression)
**Downstream score**: Baseline 67 → Skill 58 → Uplift −9 (regression)

**Fix applied**: Light-Touch Mode (Operating Mode F) added in v3. For emotional writing, apology messages, and personal communication, the Skill now suppresses the visible compiled brief and instructs the Agent to preserve the user's emotional register directly.

**Verification**: B02v2 re-evaluated with Light-Touch Mode active: Oracle uplift +19, Downstream uplift +15. Regression resolved.

---

## Recurring Failure Patterns (non-regression, but weak)

### Pattern 1 — Vague Scope Without Inspect-First

Cases like "clean up the project" or "check consistency" where v1 attempted broad edits without first inspecting the current state. Fixed by Context Scan (v2) and Inspect-First Protocol emphasis (v3).

**Risk**: Medium-high. Without inspect-first, the Agent may delete or modify things the user wanted preserved.

### Pattern 2 — Missing Search-Before-Edit in Rename Tasks

When renaming identifiers or keys that appear in multiple files, early versions of Prompt A only specified the edit in the primary file. Search-Before-Edit Rule added in v3.

**Risk**: Silent partial rename leaves broken references.

### Pattern 3 — Fake Specificity in Code Briefs

Prompt A said "fix the bug in the authentication flow" without naming the specific symptom, input that triggers it, or expected output. Testable Requirement Conversion added in v3 for code/math tasks.

**Risk**: Agent guesses at the target and may fix the wrong thing.

### Pattern 4 — High-Risk Action Batched With Safe Actions

Without Action Risk Ladder, some Prompt A briefs included a push or deploy step bundled into the execution plan without an approval gate. Action Risk Ladder added in v3.

**Risk**: Irreversible action executed without user knowledge.

---

## Known Limitations (not yet fixed)

### L1 — Multi-language Emotional Register

Light-Touch Mode preserves tone for Chinese and English. For other languages (Japanese, Spanish, Korean), the Skill may still over-structure because the trigger vocabulary is not enumerated.

### L2 — Search-Before-Edit Does Not Handle Binary Files

The Search-Before-Edit Rule applies to text files. Binary assets (images, compiled artifacts) that embed strings are not covered.

### L3 — Testable Requirement Conversion for ML/AI Tasks

TRC works well for deterministic code. For ML model outputs (precision, recall, embedding similarity), the "expected output" field is probabilistic, and the Skill does not yet handle tolerance ranges or statistical acceptance criteria.
