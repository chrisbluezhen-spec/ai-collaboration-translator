# Evaluation Harness

Use this protocol when the user asks whether the Skill works or wants to improve it based on evidence.

## Test Case Schema

Use 12-20 realistic cases. Each case should include:

```yaml
id: short-id
raw_prompt: user's original rough prompt
target_agent: Claude Code | Codex | Cursor | OpenClaw | ChatGPT/GPT | other
task_type: coding | automation | business planning | writing | research | delegation | other
expected_output_type: patch | plan | message | report | browser action plan | analysis | other
gold_intent: what the user truly wants
must_have:
  - required behavior or content
should_avoid:
  - misunderstanding, unsafe action, or unwanted style
risk_level: low | medium | high
```

## Validation Flow

1. Run the baseline path: `raw prompt -> simulated target Agent output`.
2. Run the skill path: `raw prompt -> Skill-generated prompt or clarification -> simulated target Agent output`.
3. Score both downstream outputs with the downstream output rubric.
4. Score the Skill-generated prompt with the prompt quality rubric.
5. Generate an evaluation report.

If the Skill asks clarification questions instead of generating a prompt, score whether those questions are necessary, friendly, and likely to improve the final prompt.

## Prompt Quality Rubric

Score 100 points:

- Intent preservation: 20
- Objective clarity: 15
- Context and constraint completeness: 15
- Agent executability: 20
- Clarification quality: 10
- Output format clarity: 10
- Safety and boundary handling: 10

## Downstream Output Quality Rubric

Score 100 points:

- Task completion: 30
- User intent alignment: 20
- Actionability: 20
- Output format fit: 10
- Assumption handling: 10
- Safety and no overreach: 10

Primary metric:

`Skill Uplift = downstream_output_score(skill_path) - downstream_output_score(baseline_path)`

## Report Format

Include:

- Average baseline score
- Average skill-path score
- Average uplift
- Positive uplift rate
- Regression rate
- Top improvement cases
- Weak or regressed cases
- Common failure modes
- Recommended changes to the Skill

## Pass Criteria

For lightweight first validation:

- Average downstream uplift >= +15 points.
- At least 70% of test cases show positive uplift.
- Regression cases <= 10%.
- High-risk tasks show stronger safety boundaries in the skill path.
- Human spot-check of 3-5 cases confirms the automated judge is directionally reliable.

## Human Calibration Policy

Automated judging is useful for speed, but should not fully replace human judgment.

For each validation round, ask the human evaluator to review only:

- 2 cases with the highest uplift
- 2 cases with the lowest or negative uplift
- 1-2 strategically important cases

Ask the human evaluator:

- Did the Skill preserve the user's real intent?
- Did it keep important business intuition or non-consensus thinking?
- Did it ask helpful clarification questions instead of creating friction?
- Did the downstream Agent output become more usable?
- Did the Skill avoid over-structuring or over-technicalizing the user's idea?

Use human feedback to update clarification behavior, prompt construction rules, and examples.
