---
name: ai-collaboration-translator
description: 'Translate rough ideas, vague requests, and loosely structured natural language into clear prompts or execution briefs for AI/Agent collaboration. In executable environments such as Claude Code, Codex, or Cursor, default to compile-then-execute: clarify only when needed, create an execution brief, and perform the task when safe. Use Prompt-Only Mode when users ask to optimize, clarify, structure, rewrite, compile, or generate a prompt for another model/agent such as Claude Code, Codex, Cursor, OpenClaw/OpenHands, ChatGPT/GPT; Chinese triggers include "帮我写给 Claude Code 的 Prompt", "帮我优化这个指令", "把这个需求转成 Cursor 能执行的 Prompt", "我有个想法，但不知道怎么跟 AI 说", "先帮我对齐需求，再生成 Prompt", "只生成 Prompt".'
---

# AI Collaboration Translator

## Purpose

Help humans collaborate better with AI. Translate rough thoughts, vague requests, or partially formed ideas into either:

- An execution brief the current Agent should use to complete the task.
- A copy-ready prompt for another Agent when the user explicitly wants Prompt-Only Mode.

The job is not to make prompts sound polished. The job is to make the user's real intent easier for AI/Agents to understand, verify, and execute.

## Target Users

Design for users who:

- Have strong ideas but may not express them in a structured way.
- Are non-technical, business-oriented, or only partially technical.
- Understand the business goal but do not know how to translate it into Agent instructions.
- Need a thinking partner to clarify intent, assumptions, constraints, risks, and success criteria.
- Want to work with AI tools without becoming prompt engineering experts.

## Core Use Case

Support two usage styles:

- **Compile-then-Execute Mode**: raw user request -> Prompt A / execution brief -> current Agent execution -> verification -> report.
- **Prompt-Only Mode**: raw user request -> requirement alignment -> copy-ready prompt for another Agent -> stop.

Improve downstream or current-Agent output quality by improving the instruction before execution.

## Execution Boundary

This Skill can operate in two modes.

### Prompt-Only Mode

Use Prompt-Only Mode when:

- The user explicitly asks for a prompt to paste into another Agent.
- The target Agent is not the current runtime.
- The task is intended for OpenClaw/OpenHands, browser automation, external messaging, publishing, purchasing, deleting, deployment, or another environment this Agent cannot safely execute.
- The user says "只生成 Prompt", "不要执行", "给我一段 Prompt", or equivalent.

In Prompt-Only Mode, compile the user's request into a copy-ready prompt and stop.

### Compile-then-Execute Mode

Use Compile-then-Execute Mode when:

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

### A. Compile-then-Execute Mode

Use when the Skill is triggered inside an executable environment such as Claude Code, Codex, or Cursor and the user appears to want the current Agent to complete the task.

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

Use when the user asks whether this Skill is effective or wants validation. Compare Prompt-Only behavior and Compile-then-Execute behavior. Judge downstream or same-Agent output quality, not prompt polish. Read `references/evaluation-harness.md` for the lightweight protocol.

### F. Light-Touch Mode

Use for personal communication, apology emails, emotional writing, sensitive stakeholder replies, and any task where the user's voice and emotional register matter more than structural completeness.

Rules:
- Minimize or skip the visible compiled brief. Do not display a bulleted task structure.
- Avoid corporate boilerplate and clinical bullet lists.
- Preserve the user's original emotional register and vocabulary in the output.
- Produce the natural final message directly unless a critical question is essential.
- The compiled brief, if needed internally, remains invisible to the user.

Triggers: apology messages, personal letters, sensitive stakeholder replies, emotional outreach, "help me write something honest / sincere / personal", expressions of regret or vulnerability.

## Clarification Policy

Bias toward execution in executable environments.

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

## Preserve Human Intent

Do not over-normalize the user's idea into a generic prompt template. Preserve:

- The user's original business intuition.
- Non-consensus, exploratory, or unusual thinking.
- Emotional tone or communication intent when relevant.
- Uncertainty, open questions, and important unknowns.
- Unusual but important constraints.
- The user's vocabulary when it carries meaning.

Make the idea clearer for AI execution without sanding away what makes it valuable.

When simplifying a request, keep the user's own words in the Objective field of Prompt A. Add structure around them, do not replace them.

## Prompt Construction

In Compile-then-Execute Mode, the compiled prompt is not merely an artifact for the user to copy. Prompt A becomes the active execution brief for the current Agent.

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

For tasks involving identifier renames, string replacements, config key changes, version bumps, or import path changes:

1. Search all occurrences across the repo before editing.
2. Edit all intended locations in one pass.
3. Verify no unintended occurrences remain after editing.
4. Report what changed and what was intentionally left unchanged.

Include this rule in Prompt A whenever the task involves a name, key, or value that may appear in multiple files.

### Testable Requirement Conversion

For code, math, algorithm, data-processing, and structured-output tasks, convert vague goals into testable acceptance criteria before compiling Prompt A:

- State at least one concrete expected input/output example.
- Enumerate edge cases that must not break.
- Specify algorithmic constraints (complexity, precision, format, schema).
- Define regression checks: what currently works that must continue to work.
- Keep scope minimal: fix the stated problem, not surrounding issues.

Do not apply this to personal writing, emotional communication, or open-ended exploratory requests.

### Prompt A Anti-Patterns

Never include these in Prompt A:

- **Vague verbs without criteria**: "improve", "optimize", "make it better", "review everything". Replace with a specific, observable outcome.
- **Unbounded scope**: "fix all issues", "update the docs", "check the whole repo". Replace with bounded scope and explicit out-of-scope statements.
- **Missing verification**: no observable done-condition means the Agent cannot self-verify and will either over-deliver or under-deliver.
- **Fake specificity**: adding structure around a vague goal does not make it specific. "Objective: improve user experience" is still vague. Add a measurable target.
- **Restating raw words without extracting intent**: Prompt A must encode what the user means, not what they said. A raw copy-paste of the user's request is not a compiled brief.

## Prompt A Quality Gate

Before executing in Compile-then-Execute Mode, verify Prompt A against all five checks. If any check fails, revise Prompt A before proceeding.

1. **Unambiguous objective**: Can the Agent identify exactly one interpretation of what "done" means?
2. **Observable acceptance criterion**: Can the Agent verify completion without asking the user?
3. **Bounded scope**: Are the in-scope and out-of-scope boundaries explicit?
4. **Failure modes named**: Does Prompt A specify at least one thing that would make the result "technically done but wrong"?
5. **No vague verbs**: Does Prompt A contain zero instances of "improve", "optimize", "review", "update", "fix" without a specific target and success condition?

If checks 1–3 fail, return to the intent extraction and clarify the underlying goal and success signature.
If checks 4–5 fail, add a "What not to do" clause and tighten the objective with a measurable target.

## Output Format

Choose output based on mode.

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

North-star metric: "Can the receiving or current AI/Agent produce a useful first-pass result with less user correction than it would from the raw prompt?"

Evaluate three layers:

- Prompt/Brief Quality: preserves real intent; makes objective, context, inputs, constraints, output format, and success criteria explicit; avoids fake specificity; gives the Agent enough information to act without guessing.
- Agent Execution Quality: increases first-pass usable output; reduces misunderstanding, hallucinated assumptions, and repeated corrections; improves safety boundaries; improves verification and final reporting.
- User Collaboration Experience: helps non-technical or loosely structured users express what they want; asks friendly, high-leverage questions; preserves the user's voice; helps the user learn better AI collaboration over time.

## Measurement Rubric

Prompt/brief quality score, 100 points:

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

Primary metric: `Skill Uplift = output_score(skill_path) - output_score(baseline_path)`.

Lightweight first-validation pass criteria:

- Average uplift >= +15 points.
- At least 70% of test cases show positive uplift.
- Regression cases <= 10%.
- High-risk tasks show stronger safety boundaries in the skill path.
- In executable-Agent contexts, the Skill proceeds to execution when safe instead of stopping at Prompt A.
- Human spot-check of 3-5 cases confirms the automated judge is directionally reliable.

## References

- Read `references/prompt-patterns.md` for target-specific prompt shells and adapters.
- Read `references/evaluation-harness.md` when validating whether this Skill improves AI/Agent results.
