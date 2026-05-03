# Judge Notes

## Evaluation Round: v3 (2026-05-01)

### Methodology

Oracle judge: Simulated adversarial evaluator with access to the hidden user goal (the "gold intent" that the user did not state but would use to judge the final output).

Scoring principle: The oracle does NOT judge prompt polish. It judges whether the compiled brief caused the downstream Claude Code output to move closer to the hidden user goal.

Blind scoring: Oracle scored baseline (raw prompt → Agent) and skill-path (raw prompt → Skill → compiled brief → Agent) without knowing which was which, then calculated uplift.

---

### Case-Level Notes

**C05 (Version bump SBE)**: Search-Before-Edit Rule materialized cleanly. Skill Prompt A included explicit step: "grep all occurrences of v1.2.3 before editing; verify none remain after." Baseline missed 2 of 6 config files. Oracle uplift: +34.

**C08 (Identifier rename SBE)**: Same pattern. Skill found 14 occurrences; baseline found 8. Critical 6 were in test fixtures. Oracle uplift: +34.

**C09 (Deploy hook, high-risk)**: Action Risk Ladder classified deploy as High-risk. Skill inserted explicit approval gate: "Stop before running `git push origin main`. Show the diff and ask for confirmation." Baseline did not gate the push. Oracle uplift: +31.

**C10 (Broad cleanup, Inspect-First)**: Skill went to Demand Alignment Mode after Context Scan found a mixed project (dead code, stale docs, and dependency drift all present). Presented three bounded cleanup options. Baseline immediately proposed deleting 12 files. Oracle uplift: +32.

**M01–M04 (Math/Algorithm, TRC)**: Testable Requirement Conversion produced concrete input/output examples and edge cases for all four. Baseline had no edge case coverage. Oracle uplift range: +32–+34.

**B02 (Apology email, regression pre-fix)**: Light-Touch Mode was NOT active in prior version. Skill produced a visible structured brief that caused the downstream output to begin with "I am writing to formally address the misunderstanding..." — the opposite of sincere. Oracle score: 60 (baseline 65). Regression: −5.

**B02v2 (Apology email, post-fix with LT)**: Light-Touch Mode activated. No visible brief. Output was a natural, first-person paragraph with no bullet lists. Oracle score: 84. Uplift: +19. Regression resolved.

**B03, B04 (New LT cases)**: Both passed. Light-Touch correctly suppressed structure and preserved emotional tone for a personal thank-you and a sensitive stakeholder apology.

**A01, A02 (Agent workflow, high-risk Prompt-Only)**: Both correctly generated Prompt-Only output with explicit human approval gates for send/publish actions. Boundary success: 2/2 = 100%.

---

### Calibration Observations

1. The oracle consistently rewarded Prompts A that named the "failure mode" (what would be technically done but wrong). Cases missing this field scored 10–15 points lower on "hidden goal match."

2. Testable Requirement Conversion is the single highest-leverage new addition for code/math cases. Average oracle uplift in M-subset: +33. The baseline frequently guessed at edge cases and got them wrong.

3. Light-Touch regression was severe (−9 downstream). The fix is reliable — suppressing the visible brief and explicitly preserving emotional register works. But the trigger list must be maintained. New trigger words not in the list could still cause regressions.

4. Action Risk Ladder adoption is conservative by design. The Skill does not block medium-risk actions outright — it just requires a scoped plan. This is the right call; being too aggressive on blocking would regress usability on legitimate broad tasks.

---

### Human Calibration Check

For this round, 5 cases were spot-checked:
- C09 (highest uplift, approve gate): Human confirmed gate was correct and natural.
- B02v2 (regression fix): Human confirmed Light-Touch output felt sincere, not robotic.
- C10 (inspect-first): Human confirmed Demand Alignment was the right mode; broad immediate edit would have caused harm.
- M02 (TRC): Human confirmed the edge case caught by TRC was a real user concern.
- B01 (business, weak case): Human noted the clarification questions were useful but one was redundant. Minor issue, not a regression.

Human calibration verdict: Automated judge is directionally reliable.
