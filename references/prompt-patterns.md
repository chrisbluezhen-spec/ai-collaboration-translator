# Prompt Patterns

Use these patterns as building blocks. Trim sections that do not apply, and preserve the user's language and intent.

## Compile-then-Execute Pattern

Use when the current Agent should execute the task after compiling the user's rough request:

```markdown
I will first translate your rough request into a structured execution brief, then execute it in the current environment.

Compiled Task Brief:
- Objective:
- Context:
- Inputs / discovery plan:
- Scope:
- Constraints:
- Approval gates:
- Acceptance criteria:
- Verification:

Execution Plan:
1. Inspect relevant context/files/tools.
2. Make the smallest coherent change or produce the requested artifact.
3. Stop and ask before destructive, public, expensive, irreversible, external, or production-affecting actions.
4. Verify the result.
5. Report what changed, what was verified, and remaining risks.
```

## Universal Agent Prompt Shell

```markdown
You are an expert [target role] helping me complete [task type].

Goal:
[One concrete outcome.]

Context:
[Relevant background, current state, audience, repo/app/product details, constraints.]

Inputs:
[Files, links, pasted text, screenshots, examples, data, or placeholders for missing inputs.]

Scope:
- Do: [specific actions]
- Do not: [excluded actions, risky changes, style limits]

Workflow:
1. First inspect or restate the relevant context.
2. Ask only for missing information that materially affects the result.
3. Execute the task in small, coherent steps.
4. Verify the result using [tests/checks/review criteria].
5. Report what changed, what was verified, and any remaining risks.

Acceptance criteria:
- [Observable done condition]
- [Quality bar]
- [Verification requirement]

Output format:
[Exact format, file/artifact expectations, tone, length, language.]
```

## Requirement Alignment Pattern

Use when the user has a rough idea but not a structured requirement:

```markdown
Please act as a thinking partner and help me turn this rough idea into a clear task brief for an AI/Agent.

Raw idea:
[user's rough idea]

Help me clarify:
- Desired outcome
- Target user/audience
- Background/context
- Inputs or materials needed
- Constraints and preferences
- Execution boundary
- Success criteria
- Risks or unacceptable behaviors

Ask only the highest-leverage questions first. Do not turn this into a rigid questionnaire.
After alignment, either execute in the current environment if safe or produce a copy-ready prompt for [target Agent/model].
```

## Claude Code / Codex Pattern

Use this for same-runtime execution in Claude Code/Codex, or adapt it for Prompt-Only Mode when the user explicitly asks for a prompt.

```markdown
You are working in the current codebase.

Goal:
[Desired code, review, document, or product outcome.]

Repo context:
- Path/repo: [repo path or "current workspace"]
- Relevant files/modules: [known paths or "discover first"]
- Existing behavior: [current behavior]
- Desired behavior: [target behavior]

Instructions:
1. Inspect the relevant code and docs before deciding.
2. Infer safely from repository context instead of asking for details that can be discovered.
3. Keep changes minimal and scoped to the requested behavior.
4. Preserve existing user changes; do not revert unrelated work.
5. Follow existing project patterns, naming, architecture, and tests.
6. Ask before destructive actions, publishing, deploying, or broad refactors.
7. Run relevant tests/checks if available.

Done when:
- [Acceptance criteria]
- Relevant tests/checks pass or any inability to run them is explained.
- Final response lists changed files, verification performed, and remaining risks.
```

## Cursor Pattern

```markdown
Assume you are working in my current Cursor workspace.

Goal:
[Expected product/code outcome.]

Scope:
- Files/areas likely involved: [paths or feature area]
- Expected behavior: [behavior]
- UI/UX details: [layout, interactions, copy, visual constraints]
- Do not change: [boundaries]

Please inspect the current workspace, propose or apply the smallest coherent change, and verify against:
- [Acceptance criterion 1]
- [Acceptance criterion 2]
- [Test/manual check]
```

## OpenClaw / Browser / Automation Pattern

```markdown
You are operating in [browser/app/environment].

Goal:
[Outcome.]

Environment:
- Target site/app: [URL/app]
- Account/credentials assumption: [already logged in / ask user / not available]
- Allowed actions: [browse, fill forms, draft, click, download, etc.]
- Not allowed without approval: [send, purchase, publish, delete, deploy, change settings]

Workflow:
1. Inspect the current state.
2. Ask for missing credentials or confirmation if blocked.
3. Complete only allowed actions.
4. Stop before any external side effect and ask for approval.
5. Verify the visible result and report what happened.
```

## Business Planning Pattern

```markdown
You are a business/product strategy collaborator.

Goal:
[Decision, plan, strategy, or recommendation needed.]

Context:
[Market, product, customer, team, constraints, current state.]

Please produce:
- Key assumptions
- Options or tradeoffs
- Recommendation
- Risks and mitigations
- Milestones or next actions
- Open questions

Keep the user's original business intuition visible, even if it is non-consensus or exploratory.
```

## Communication / Writing Pattern

```markdown
You are helping me write for [audience].

Message goal:
[What the message should accomplish.]

Relationship/context:
[Recipient relationship, prior conversation, sensitivity.]

Tone:
[Direct, warm, executive, casual, apologetic, persuasive, etc.]

Requirements:
- Length: [length]
- Language: [language]
- Must say: [points]
- Avoid saying: [points]
- Call to action: [desired next step]

Preserve my intent and voice; do not make it sound generic or overly polished.
```

## Research / Analysis Pattern

```markdown
You are a research and analysis assistant.

Research question:
[Question.]

Context:
[Why this matters, decision to support, constraints.]

Source expectations:
[Official sources, primary sources, recent sources, citations, no web, etc.]

Please provide:
- Short answer / conclusion
- Evidence or citations
- Assumptions
- Confidence level
- Unknowns or caveats
- Recommended next steps

Do not overstate certainty. Distinguish facts, inference, and opinion.
```

## Multi-Agent Delegation Pattern

```markdown
Coordinate this task across multiple agents/workers.

Overall goal:
[Goal.]

Subtasks and owners:
- Owner A: [scope/files/output]
- Owner B: [scope/files/output]
- Reviewer/integrator: [review criteria and integration responsibility]

Handoff artifacts:
- [Plans, diffs, summaries, test results, reports]

Rules:
- Avoid overlapping write scopes unless explicitly coordinated.
- Each worker should verify their own output.
- The integrator should check consistency, conflicts, and acceptance criteria.
```

## Evaluation Harness Pattern

```markdown
Evaluate whether ai-collaboration-translator improves AI/Agent output.

Use 12-20 realistic test cases. For each case:
1. Classify whether it should use Prompt-Only Mode, Compile-then-Execute Mode, or Demand Alignment Mode.
2. Generate baseline output from the raw prompt.
3. Generate skill-path Prompt A / execution brief or copy-ready prompt.
4. If executable, simulate same-Agent execution from Prompt A; if prompt-only, simulate target-Agent output from the copy-ready prompt.
5. Score baseline and skill-path outputs with the downstream/same-Agent output rubric.
6. Score Prompt A or the copy-ready prompt with the prompt/brief quality rubric.
7. Report average scores, uplift, regressions, mode-selection failures, and recommended Skill changes.

Primary metric:
Skill Uplift = output_score(skill_path) - output_score(baseline_path)
```

## Light-Touch Pattern

Use for emotional, personal, or tone-first writing where structure would feel cold or corporate.

```markdown
Help me write [message type] to [recipient].

Context:
[Relationship, what happened, what I want the reader to feel or do.]

My tone should be:
[honest / warm / apologetic / direct / personal — user's own words preferred]

Key points to convey:
- [point 1]
- [point 2]

Avoid: corporate language, bullet lists in the message, generic phrases.
Preserve: my voice, sincerity, any specific phrases I care about.

Length: [short / medium / as long as needed to feel genuine]
```

## Search-Before-Edit Pattern

Use when renaming identifiers, keys, paths, or values that appear across multiple files.

```markdown
You are about to rename / replace [identifier/key/value] in this codebase.

Step 1 — Search:
Find all occurrences of [old name] across the repo. Report the list before editing.

Step 2 — Edit:
Replace all intended occurrences in one pass.
Explicitly skip: [list of locations that should NOT be changed, if any]

Step 3 — Verify:
After editing, search again for [old name] to confirm no unintended occurrences remain.

Step 4 — Report:
List changed files, skipped files, and remaining occurrences with rationale.
```

## Testable Requirement Pattern

Use for code, math, algorithm, or data-processing tasks.

```markdown
You are implementing / fixing [task description].

Expected behavior:
- Input: [concrete example]
- Output: [concrete expected result]

Edge cases that must not break:
- [edge case 1]
- [edge case 2]

Constraints:
- [time complexity / memory / precision / format / schema]

Regression guard:
- [existing behavior that must continue to work]

Scope:
- Fix only the stated problem. Do not refactor unrelated code.
- If you discover a related issue, report it but do not fix it unless asked.

Done when:
- The above input/output example produces the correct result.
- Edge cases pass.
- Existing tests still pass or inability to run them is explained.
```

## Anti-Patterns

- Stopping at a copy-ready prompt in Claude Code/Codex/Cursor when the user expected current-Agent execution.
- Executing when the user explicitly asked for "只生成 Prompt", "不要执行", or a prompt for another Agent.
- Vague verbs without criteria: "improve this", "make it better", "optimize everything".
- Unbounded scope unless truly needed.
- Missing verification method.
- Conflicting priorities with no ranking.
- Hidden side effects such as publishing, sending, deleting, charging, or deploying.
- Over-technicalizing a business user's intent.
- Turning every idea into the same generic professional prompt.
