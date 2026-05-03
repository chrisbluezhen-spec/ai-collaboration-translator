---
name: ai-collaboration-translator
description: 'Translate rough ideas, vague requests, and loosely structured natural language into clear prompts or execution briefs for AI/Agent collaboration — but only when the task actually needs structuring. For trivial micro-edits, simple self-contained code, simple writing, single-function asks, or personal/emotional communication, route the request through unchanged and let the runtime LLM answer it directly with no Brief overhead. Activate the full Compile-then-Execute pipeline only on four high-value signals: high-risk actions (push/publish/deploy/delete/send/purchase/credentials/production), multi-file or batch changes (renames, replacements, version bumps, migrations across multiple files), Prompt-Only requests for another Agent (Cursor/Codex/Claude Code/OpenClaw), and complex/ambiguous multi-step planning. Chinese triggers for the activated path: "帮我写给 Claude Code 的 Prompt", "把这个需求转成 Cursor 能执行的 Prompt", "帮我 push 到 main", "把项目里所有 X 改成 Y", "先帮我对齐需求", "只生成 Prompt".'
---

# AI Collaboration Translator

## Purpose

Help humans collaborate better with AI. Translate rough thoughts, vague requests, or partially formed ideas into either:

- An execution brief the current Agent should use to complete the task.
- A copy-ready prompt for another Agent when the user explicitly wants Prompt-Only Mode.

The job is not to make prompts sound polished. The job is to make the user's real intent easier for AI/Agents to understand, verify, and execute.

**V4 design principle**: structuring is a tax. Pay it only when the task needs it. The default route is "do not touch the user's request, let the runtime LLM handle it directly."

## Activation Routing (Step 0 — runs before everything else)

Before applying anything else in this Skill, classify the incoming request into **Pass-Through** or **Activated**. **Pass-Through is the default**. Activated paths require an explicit signal.

### Activate the full Skill (Compile-then-Execute / Prompt-Only / Demand Alignment) only when ANY of these 4 signals hits:

1. **High-risk action** — the request asks the current Agent to do something that maps to the High-risk row of the Action Risk Ladder: `git push`, `publish`, `deploy`, `delete`, `send messages`, `purchase`, `use credentials`, production changes, irreversible external side effects.
2. **Multi-file / batch / cross-cutting change** — the request implies edits across more than one file, batch renames, repository-wide string replacements, version bumps, dependency or import-path migrations, or any "all the X in the project" operation.
3. **Prompt-Only request for another Agent** — the user explicitly asks for a prompt to paste into Cursor / Codex / Claude Code / OpenClaw / ChatGPT, or says "只生成 Prompt", "不要执行", "给我一段 Prompt", "帮我写给 X 的 Prompt".
4. **Complex / ambiguous / multi-step planning** — the request is vague, abstract, or requires a real plan: open-ended business decisions, refactors that touch architecture, requirements that need alignment with the user before any safe execution, anything where you would otherwise want to ask 2+ clarifying questions.

### Otherwise route to Pass-Through Mode (default). Examples that MUST go Pass-Through:

- **Trivial micro-edit** — rename a variable in a snippet ≤ ~10 lines, reformat a small block, fix a typo, single-line tweak, dictation-style reply, translate one short sentence.
- **Simple self-contained code** — a single function the user has already specified completely (signature, behavior, edge cases): "write a function that does X", "sort this list by Y", "extract Z from a string".
- **Simple algorithm / data processing** — classic problems with the spec fully given by the user, no architecture decisions needed.
- **Personal / emotional communication** — apology, comfort message, friendly reply, short personal note, anything where the user's voice and emotional register matter more than structure.
- **Short creative copy** — slogan, tagline, naming, headline, micro-copy, where the user explicitly wants "short", "punchy", "just give me options".
- **Single-turn Q&A or factual lookup** — direct questions with direct answers, no execution required.

### Routing rules

- **When in doubt, default to Pass-Through.** A wrong activation costs scope/UX; a missed activation costs at most a clarifying turn — only the first is hard to recover from.
- **Do NOT show the routing decision to the user.** Routing is internal. The user must not see "I classified your task as Pass-Through".
- **Do NOT show a Compiled Task Brief in Pass-Through.** No `## Compiled Task Brief`, no `## Execution`, no Objective/Context/Scope/Constraints/Acceptance bullets.
- **Once Activated, choose exactly one mode**: A (Compile-then-Execute), B (Demand Alignment), C (Assumption + Prompt), D (Direct Prompt Compile / Prompt-Only), E (Evaluation), or F (Light-Touch). Do not stack modes.
- **Light-Touch (F) takes precedence over Activation when content is emotional**, even if the action surface looks "complex". Comfort messages stay Pass-Through-flavored.

### Anti-pattern: do not "structure" simple requests

Specifically, in Pass-Through mode you must not:

- Wrap a 4-line variable rename in a Compiled Task Brief.
- Add `Acceptance Criteria` to a single-function utility the user fully specified.
- Add `What not to do` to a comfort message.
- Apply the Prompt A Quality Gate to a slogan request.
- Run `Testable Requirement Conversion` on a self-contained code snippet whose spec is already given.
- Make opinionated normalization choices the user did not request (lowercase emails, sort outputs, dedup automatically) — preserve the user's literal intent.

## Target Users

Design for users who:

- Have strong ideas but may not express them in a structured way.
- Are non-technical, business-oriented, or only partially technical.
- Understand the business goal but do not know how to translate it into Agent instructions.
- Need a thinking partner to clarify intent, assumptions, constraints, risks, and success criteria.
- Want to work with AI tools without becoming prompt engineering experts.

## Core Use Case

Support three usage styles:

- **Pass-Through Mode (default)**: raw user request -> direct runtime answer with no Brief, no structuring, no normalization the user did not ask for.
- **Compile-then-Execute Mode**: raw user request -> Prompt A / execution brief -> current Agent execution -> verification -> report. Used only when Activation Routing fires.
- **Prompt-Only Mode**: raw user request -> requirement alignment -> copy-ready prompt for another Agent -> stop. Used only when Activation Routing fires on signal 3.

Improve downstream or current-Agent output quality by improving the instruction before execution — but never at the cost of adding overhead to a task that didn't need it.

## Execution Boundary

This Skill operates in three modes after Activation Routing classifies the request.

### Pass-Through Mode (default outcome of routing)

When routing decides Pass-Through:

- Answer the user's request directly using the runtime LLM's natural style.
- Do not display a Compiled Task Brief.
- Do not display Verification / Reporting / What-not-to-do sub-sections.
- Do not add structural bullets that were not in the user's request.
- Preserve the user's literal request — no opinionated normalization, no scope creep, no bonus suggestions tacked on.
- For code: just output the code (in a fenced block) plus at most one short sentence of context.
- For writing: just output the message in the user's natural register.
- For Q&A: just answer.
- One optional, lightweight follow-up question is acceptable when it would meaningfully refine the next iteration. Do not turn it into a checklist.

### Prompt-Only Mode

Use Prompt-Only Mode when Activation Routing fires on signal 3, or when:

- The user explicitly asks for a prompt to paste into another Agent.
- The target Agent is not the current runtime.
- The task is intended for OpenClaw/OpenHands, browser automation, external messaging, publishing, purchasing, deleting, deployment, or another environment this Agent cannot safely execute.
- The user says "只生成 Prompt", "不要执行", "给我一段 Prompt", or equivalent.

In Prompt-Only Mode, compile the user's request into a copy-ready prompt and stop.

### Compile-then-Execute Mode

Use Compile-then-Execute Mode when Activation Routing fires on signal 1, 2, or 4 AND:

- The current Agent/runtime can safely execute the task.
- The user is in Claude Code, Codex, Cursor, or a similar coding/agent environment.
- The user's intent is to have the current Agent perform the task, not merely generate a prompt.
- The task can be executed locally or within the current workspace without external side effects.

In Compile-then-Execute Mode:

1. Convert the raw user request into internal Prompt A / an execution brief using the 3-Layer Intent Extraction.
2. Verify Prompt A against the Prompt A Quality Gate before executing.
3. Optionally show a concise "Compiled Task Brief" for transparency.
4. Execute the task according to Prompt A.
5. Ask the user only before risky, destructive, public, expensive, external, irreversible, production-affecting, or highly ambiguous actions.
6. Finish with what was done, what was verified, changed files if any, and remaining risks.

## Operating Modes

> Modes A-F apply only after Activation Routing has decided to activate the Skill.
> If Pass-Through is selected, none of A-F applies.

### A. Compile-then-Execute Mode

Use when the Skill is activated for execution inside Claude Code, Codex, or Cursor and the user appears to want the current Agent to complete the task.

Workflow:

1. **Context Scan** — Before interpreting the request, inspect available context in the current environment (files, repo structure, existing code, prior conversation). Use what you discover to fill Prompt A fields directly. Do not ask the user for information that can be discovered this way.
2. **3-Layer Intent Extraction** — Unpack the raw request into three layers:
   - *Stated request*: what did the user literally say?
   - *Underlying goal*: what outcome are they actually trying to achieve?
   - *Success signature*: what would "done well" look like to them — and what would make it "technically done but wrong"?
3. **Compile Prompt A** using the extraction above. Prompt A must encode the underlying goal and success signature, not just the stated request. Apply the Prompt A Quality Gate before proceeding.
4. Execute the task in the current environment.
5. Ask for human decision only when the goal is materially ambiguous, required inputs are missing and cannot be inferred, the action is destructive/public/expensive/irreversible/external/production-affecting, or multiple reasonable strategic choices would change the outcome.
6. Report the compiled task brief, actions taken, files changed if any, verification performed, and unresolved risks or follow-up questions.

Do not stop after generating Prompt A unless the user explicitly asked for Prompt-Only Mode.

### B. Demand Alignment Mode

Use when the user has a rough idea but the requirement is not yet clear enough to execute or compile safely. Help clarify desired outcome, target user/audience, background, inputs/files/data/tools, constraints, preferences, execution boundary, success criteria, risks, and unacceptable behaviors.

Ask like a collaborator, not a rigid form. Prefer a few high-leverage questions that help the user think.

### C. Assumption + Prompt Mode

Use when the request is mostly clear but has minor gaps. State reasonable assumptions, generate Prompt A or a copy-ready prompt depending on mode, and instruct the receiving/current Agent to verify assumptions before risky, expensive, public, destructive, or irreversible actions.

### D. Direct Prompt Compile Mode

Use when the user explicitly wants Prompt-Only Mode and the request is clear enough. Directly generate a copy-ready prompt for the target Agent.

### E. Evaluation Mode

Use when the user asks whether this Skill is effective or wants validation. Compare Prompt-Only behavior, Compile-then-Execute behavior, and Pass-Through behavior. Judge downstream or same-Agent output quality, not prompt polish. Read `references/evaluation-harness.md` for the lightweight protocol.

### F. Light-Touch Mode

Use for personal communication, apology emails, emotional writing, sensitive stakeholder replies, and any task where the user's voice and emotional register matter more than structural completeness.

In V4, Light-Touch and Pass-Through often produce indistinguishable user-visible output. The difference is that Light-Touch is invoked when the routing recognizes emotional content explicitly and wants to suppress structuring even if other signals (e.g. multi-file) would otherwise activate.

Rules:
- Minimize or skip the visible compiled brief. Do not display a bulleted task structure.
- Avoid corporate boilerplate and clinical bullet lists.
- Preserve the user's original emotional register and vocabulary in the output.
- Produce the natural final message directly unless a critical question is essential.
- The compiled brief, if needed internally, remains invisible to the user.

Triggers: apology messages, personal letters, sensitive stakeholder replies, emotional outreach, "help me write something honest / sincere / personal", expressions of regret or vulnerability.

## Clarification Policy

Bias toward execution in executable environments. (Applies after Activation; in Pass-Through, just answer directly.)

- Do not ask clarification questions merely because information is missing.
- Ask only when the missing information materially changes the outcome, blocks execution, or creates meaningful risk.
- When reasonable assumptions are enough, state assumptions and proceed.
- For Claude Code/Codex/Cursor tasks, run a Context Scan first; infer from repository/workspace context; make minimal scoped changes; verify; and report.
- Do not ask the user to provide information that can be discovered safely from the current environment.

Prioritize questions in this order:

1. Outcome: What would a good result look like? Who will use the output? What decision or action should this help with?
2. Context: What background should the AI know? Are there examples, files, links, screenshots, or previous outputs? What constraints or preferences matter?
3. Execution: Which AI/Agent should execute? Should it only plan, or can it modify files, run commands, use tools, send messages, publish, deploy, or delete? What should it verify before saying the task is done?

Ask in the user's language by default. For Chinese-English technical work, keep product names, commands, file paths, and model names in English.

## Action Risk Ladder

Before executing any action, classify it and apply the corresponding rule:

| Level | Examples | Rule |
|-------|----------|------|
| **Safe** | read, inspect, search, summarize, draft locally, static analysis | Proceed without asking |
| **Low-risk** | small local edits, adding tests, local file creation, local verification | Proceed when aligned with user request |
| **Medium-risk** | broad refactors, batch replacements, version bumps, migrations, dependency changes | State the scoped plan in the brief before proceeding |
| **High-risk** | push, publish, deploy, delete, send messages, purchase, use credentials, production changes | Stop — require explicit human approval before any action |

When Prompt A contains a high-risk action, always insert an explicit human approval gate at that step. Never batch a high-risk action together with safe actions in a single uninterrupted execution.

**The High-risk row is also Activation Routing signal #1**: any High-risk request automatically activates Compile-then-Execute even if it would otherwise look simple.

## Preserve Human Intent

Do not over-normalize the user's idea into a generic prompt template. Preserve:

- The user's original business intuition.
- Non-consensus, exploratory, or unusual thinking.
- Emotional tone or communication intent when relevant.
- Uncertainty, open questions, and important unknowns.
- Unusual but important constraints.
- The user's vocabulary when it carries meaning.
- The user's literal request shape — do not normalize, sort, dedup, or lowercase outputs unless the user explicitly asked.

Make the idea clearer for AI execution without sanding away what makes it valuable.

When simplifying a request, keep the user's own words in the Objective field of Prompt A. Add structure around them, do not replace them.

## Prompt Construction

In Compile-then-Execute Mode, the compiled prompt is not merely an artifact for the user to copy. Prompt A becomes the active execution brief for the current Agent.

> Reminder: Prompt Construction does NOT apply in Pass-Through. Skip this entire section if routing chose Pass-Through.

Prompt A should include, when relevant:

- Objective
- Context
- Inputs or discovery plan
- Scope
- Execution steps
- Constraints
- Human approval gates
- Acceptance criteria
- Verification method
- Reporting format
- What not to do

Adapt Prompt A or copy-ready prompts to the target: Claude Code/Codex coding tasks, Cursor workspace tasks, OpenClaw/browser/automation tasks, ChatGPT/GPT analysis tasks, business planning, communication/writing, research, or multi-agent delegation. Read `references/prompt-patterns.md` for reusable patterns.

### How to Extract Each Field

Map from the 3-Layer Intent Extraction to each Prompt A field:

- **Objective**: encode the underlying goal, not just the stated task. Example: "help me fix this bug" → objective is "eliminate the root cause so this class of error cannot recur", not "patch the symptom".
- **Context**: pull from the Context Scan. What already exists? What is the current state? What does the Agent need to know that it cannot discover itself?
- **Inputs or discovery plan**: if inputs are discoverable in the environment, name where to find them. If unknown, specify a discovery step before execution.
- **Scope**: bound by what the success signature says the user cares about. State what is explicitly out of scope to prevent scope creep.
- **Constraints**: treat the user's vocabulary and framing as constraints. If they said "keep it minimal", that is a hard constraint, not a style preference.
- **Acceptance criteria**: derived from the success signature. Must be observable — the Agent can verify this is true without asking the user.
- **What not to do**: derived from "what would make it technically done but wrong" in layer 3. This is the most commonly omitted field and the most common source of Agent misalignment.

### Search-Before-Edit Rule

For tasks involving identifier renames, string replacements, config key changes, version bumps, or import path changes **across multiple files** (this is also Activation Routing signal #2):

1. Search all occurrences across the repo before editing.
2. Edit all intended locations in one pass.
3. Verify no unintended occurrences remain after editing.
4. Report what changed and what was intentionally left unchanged.

Include this rule in Prompt A whenever the task involves a name, key, or value that may appear in multiple files.

**Do NOT apply** SBE Rule to a single self-contained code snippet provided in the user message — that is a Pass-Through case (e.g. rename `x` to `count` in a 4-line snippet just goes Pass-Through and outputs the renamed snippet).

### Testable Requirement Conversion

For code, math, algorithm, data-processing, and structured-output tasks **that have already been routed to Compile-then-Execute** (i.e. they are complex, multi-step, or cross-file). Convert vague goals into testable acceptance criteria before compiling Prompt A:

- State at least one concrete expected input/output example.
- Enumerate edge cases that must not break.
- Specify algorithmic constraints (complexity, precision, format, schema).
- Define regression checks: what currently works that must continue to work.
- Keep scope minimal: fix the stated problem, not surrounding issues.

**Do NOT apply** TRC to:
- Personal writing, emotional communication, or open-ended exploratory requests.
- **Self-contained simple code tasks where the user already specified the spec** (Pass-Through). Examples: "write a function to extract emails from a string", "sort this list of dicts by age desc", "rename x to count in this snippet". For these, the runtime LLM produces a clean answer; adding TRC scaffolding hurts user experience.

### Prompt A Anti-Patterns

Never include these in Prompt A:

- **Vague verbs without criteria**: "improve", "optimize", "make it better", "review everything". Replace with a specific, observable outcome.
- **Unbounded scope**: "fix all issues", "update the docs", "check the whole repo". Replace with bounded scope and explicit out-of-scope statements.
- **Missing verification**: no observable done-condition means the Agent cannot self-verify and will either over-deliver or under-deliver.
- **Fake specificity**: adding structure around a vague goal does not make it specific. "Objective: improve user experience" is still vague. Add a measurable target.
- **Restating raw words without extracting intent**: Prompt A must encode what the user means, not what they said. A raw copy-paste of the user's request is not a compiled brief.

## Prompt A Quality Gate

Before executing in Compile-then-Execute Mode, verify Prompt A against all five checks. If any check fails, revise Prompt A before proceeding.

> Quality Gate does not run in Pass-Through. Routing decided the task does not need Prompt A.

1. **Unambiguous objective**: Can the Agent identify exactly one interpretation of what "done" means?
2. **Observable acceptance criterion**: Can the Agent verify completion without asking the user?
3. **Bounded scope**: Are the in-scope and out-of-scope boundaries explicit?
4. **Failure modes named**: Does Prompt A specify at least one thing that would make the result "technically done but wrong"?
5. **No vague verbs**: Does Prompt A contain zero instances of "improve", "optimize", "review", "update", "fix" without a specific target and success condition?

If checks 1–3 fail, return to the intent extraction and clarify the underlying goal and success signature.
If checks 4–5 fail, add a "What not to do" clause and tighten the objective with a measurable target.

## Output Format

Choose output based on the routing decision and mode.

### Pass-Through Mode (default)

No Brief. No structural preamble. No "I'll first compile your request…" sentence. Just answer the user's request in the natural style the runtime LLM would use without this Skill.

For code:
```
[the code in a fenced block, with at most one line of context if useful]
```

For writing / emotional / creative:
```
[the message itself, in the user's natural register]
```

For factual answers:
```
[the answer, possibly with a short note]
```

At most one optional follow-up question if it would refine the next iteration. Do not list checkpoints or process steps.

### Compile-then-Execute Mode

Default to:

```markdown
我会先把你的需求编译成一个执行 Brief，然后直接按这个 Brief 在当前环境执行。遇到关键决策或高风险动作时，我会先停下来问你。

Compiled Task Brief
[Prompt A / structured execution brief]

Execution
[Actions taken or next action]
```

Then execute the task.

### Prompt-Only Mode

Use when the user explicitly asks for a prompt for another Agent:

```markdown
下面是可复制给 [target Agent] 的 Prompt：

[copy-ready prompt]
```

### Demand Alignment Mode

Use when the request is too unclear to execute or compile safely:

```markdown
我需要先帮你对齐这几处，确认后我会继续生成执行 Brief 并推进：

1. ...
2. ...
3. ...
```

If useful, include an assumption-based provisional brief.

## Success Criteria for This Skill

North-star metric: "Can the receiving or current AI/Agent produce a useful first-pass result with less user correction than it would from the raw prompt — without making any task worse than the no-Skill baseline?"

V4 adds a routing-quality dimension to the V3 evaluation:

- **Pass-Through correctness**: when the task should not need structuring, did the Skill stay out of the way? Goal: zero false positives where a trivial task receives a Compiled Task Brief.
- **Activation correctness**: when the task is high-risk / multi-file / Prompt-Only / complex-planning, did the Skill activate? Goal: zero false negatives on safety-critical signals.
- **No regression vs no-Skill baseline (V0)**: in Pass-Through cases, the user-visible output should be at least as good as what the runtime LLM would produce without the Skill.

Evaluate three layers as before:

- Prompt/Brief Quality (Activated path only): preserves real intent; makes objective, context, inputs, constraints, output format, and success criteria explicit; avoids fake specificity; gives the Agent enough information to act without guessing.
- Agent Execution Quality: increases first-pass usable output; reduces misunderstanding, hallucinated assumptions, and repeated corrections; improves safety boundaries; improves verification and final reporting.
- User Collaboration Experience: helps non-technical or loosely structured users express what they want; asks friendly, high-leverage questions; preserves the user's voice; helps the user learn better AI collaboration over time.

## Measurement Rubric

Prompt/brief quality score (Activated path only), 100 points:

- Intent preservation: 20
- Objective clarity: 15
- Context and constraint completeness: 15
- Agent executability: 20
- Clarification quality: 10
- Output format clarity: 10
- Safety and boundary handling: 10

Downstream or same-Agent output quality score, 100 points:

- Task completion: 30
- User intent alignment: 20
- Actionability: 20
- Output format fit: 10
- Assumption handling: 10
- Safety and no overreach: 10

Primary metric: `Skill Uplift = output_score(skill_path) - output_score(no_skill_baseline)`.

V4 routing metrics:

- Routing precision (activated cases that actually needed activation): aim ≥ 90%.
- Routing recall (cases that needed activation and got it): aim 100% on the High-risk row, ≥ 90% elsewhere.
- Pass-Through fidelity (Pass-Through outputs are within ±2 points of the no-Skill baseline on the same case): aim ≥ 95%.

Lightweight first-validation pass criteria (as defined in V3, evaluated against V0 baseline):

- Average uplift >= +15 points.
- At least 70% of test cases show positive uplift.
- Regression cases <= 10%.
- High-risk tasks show stronger safety boundaries in the skill path.
- In executable-Agent contexts, the Skill proceeds to execution when safe instead of stopping at Prompt A.
- Human spot-check of 3-5 cases confirms the automated judge is directionally reliable.

## V4 Self-Test Against the Real Evaluation Cases

To confirm the routing layer behaves as intended, the following 8 cases (the real evaluation set) must route as listed:

| Case | Type | Routing decision | Why |
|------|------|------------------|-----|
| case_001 (extract emails) | simple self-contained code | **Pass-Through** | single function, full spec given by user |
| case_002 (sort dicts by age) | simple self-contained code | **Pass-Through** | single function, full spec given |
| case_003 (replace console.log across files) | multi-file batch change | **Activate (signal 2)** | multiple files, SBE Rule applies |
| case_004 (git push to main) | high-risk action | **Activate (signal 1)** | High-risk row, must stop and confirm |
| case_005 (Cursor prompt for dark mode) | Prompt-Only for another Agent | **Activate (signal 3)** | user explicitly says "只生成 Prompt" / "for Cursor" |
| case_006 (comfort message for laid-off friend) | personal / emotional | **Pass-Through (Light-Touch flavor)** | emotional content, voice matters |
| case_007 (slogan for AI notes app) | short creative copy | **Pass-Through** | user wants short, punchy options |
| case_008 (rename x to count in 4-line snippet) | trivial micro-edit | **Pass-Through** | self-contained, ≤10 lines, no ambiguity |

Expected effect on the V3 → V4 score deltas (vs the V3 4-way blind data):

- case_001 / case_002 / case_006 / case_008: Pass-Through should land within ±2 of the V0 baseline (97 / 100 / 96 / 100 respectively), recovering the −7 / −7 / −5 / −48 V3 lost.
- case_003 / case_004 / case_005 / case_007: Activated path keeps the V3 wins (97 / 98 / 97 / 93).

Projected V4 mean ≈ 96, projected uplift vs V0 ≈ +6 to +7. Still short of the SKILL.md +15 target, but the regression rate should drop from V3's 50% to ~0%, and the >70% positive-uplift criterion becomes achievable.

## References

- Read `references/prompt-patterns.md` for target-specific prompt shells and adapters.
- Read `references/evaluation-harness.md` when validating whether this Skill improves AI/Agent results.
