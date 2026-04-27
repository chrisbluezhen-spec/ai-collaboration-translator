# AI Collaboration Translator / AI 协作翻译器

## 中文说明

**AI Collaboration Translator** 是一个帮助用户更好地和 AI/Agent 协作的 Skill。

它不是普通的 Prompt Optimizer。它的核心作用是：帮助非技术用户、业务用户，或者“很有想法但表达不够结构化”的用户，把粗糙想法、模糊需求、半成品指令，转化成 AI/Agent 更容易理解、执行、验证的 Prompt。

核心流程：

```text
粗糙想法 / 模糊需求
→ 需求对齐
→ 必要时澄清
→ 结构化任务说明
→ 适配目标 Agent 的 Prompt
→ 下游 Agent 执行
```

这个 Skill 的目标不是让 Prompt 看起来更“专业”，而是让接收 Prompt 的 AI/Agent 更少误解、更少猜测，并更容易产出可用的第一版结果。

## 适合谁使用

- 有明确想法，但表达还不够结构化的人
- 非技术用户、业务用户、产品/运营/管理者
- 知道业务目标，但不知道如何把目标翻译成 Agent 指令的人
- 想先和 AI 对齐需求，再交给 Cursor、Claude Code、Codex、OpenClaw/OpenHands、ChatGPT/GPT 或其他 Agent 执行的人
- 想提升 AI 协作质量，但不想成为 Prompt Engineering 专家的人

## 如何使用

你可以把粗糙需求直接交给这个 Skill，例如：

- “我有个想法，但不知道怎么跟 AI 说”
- “帮我写给 Claude Code 的 Prompt”
- “把这个需求转成 Cursor 能执行的 Prompt”
- “先帮我对齐需求，再生成 Prompt”
- “帮我优化这个指令，让 Agent 更容易执行”

Skill 会根据需求清晰度选择不同模式：

- **需求对齐模式**：当想法还模糊时，先提出少量高价值问题。
- **假设 + Prompt 模式**：当需求大体清楚但有小缺口时，说明假设并生成 Prompt。
- **直接编译模式**：当需求已经足够清楚时，直接生成可复制的 Prompt。
- **评估模式**：当你想验证这个 Skill 是否有效时，比较原始 Prompt 路径和 Skill 路径的下游输出质量。

## 非执行边界

这个 Skill 只负责澄清需求和生成 Prompt，不负责执行 Prompt 背后的实际任务。

例如：

- 如果你要给 Claude Code 或 Codex 一个修改代码仓库的 Prompt，本 Skill 只生成 Prompt，不直接改代码。
- 如果你要给 Cursor 一个工作区任务，本 Skill 只生成 Prompt，不直接修改文件。
- 如果你要给 OpenClaw/OpenHands 或浏览器自动化 Agent 一个发送、发布、购买、删除、部署等任务，本 Skill 会生成 Prompt，并加入人工确认边界。

## 文件结构

```text
ai-collaboration-translator/
├── SKILL.md
├── README.md
├── .gitignore
├── references/
│   ├── prompt-patterns.md
│   └── evaluation-harness.md
└── agents/
    └── openai.yaml
```

## 主要文件

- [SKILL.md](SKILL.md)：Skill 的触发说明、工作流、澄清策略、输出规则和评估标准。
- [references/prompt-patterns.md](references/prompt-patterns.md)：不同目标 Agent 和任务类型的 Prompt 模式。
- [references/evaluation-harness.md](references/evaluation-harness.md)：用于评估 Skill 是否改善下游 Agent 输出的轻量协议。
- [agents/openai.yaml](agents/openai.yaml)：Skill 的界面元数据。

## 验证方法

基础结构校验：

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py ./ai-collaboration-translator
```

效果验证建议使用 12-20 个真实或接近真实的测试案例：

```text
Baseline path: 原始 Prompt → 目标 Agent → 输出
Skill path: 原始 Prompt → 本 Skill → 优化后的 Prompt → 目标 Agent → 输出
```

重点比较下游输出质量，而不是只比较 Prompt 是否更好看。

核心指标：

```text
Skill Uplift = downstream_output_score(skill_path) - downstream_output_score(baseline_path)
```

详见 [references/evaluation-harness.md](references/evaluation-harness.md)。

---

## English

**AI Collaboration Translator** is a Skill for helping people collaborate better with AI agents.

It is not a generic prompt optimizer. Its purpose is to help non-technical users, business users, and people with strong ideas but loosely structured expression turn rough thoughts, vague requirements, or half-formed instructions into prompts that AI agents can understand, execute, and verify.

Core workflow:

```text
Rough idea / vague request
→ Requirement alignment
→ Clarification when needed
→ Structured task brief
→ Target-agent-specific prompt
→ Downstream Agent execution
```

The goal is not to make every prompt sound polished. The goal is to preserve the user's real intent and make it easier for the receiving AI/Agent to produce a useful first-pass result with fewer corrections.

## Who It Is For

- Users with strong ideas but loosely structured expression
- Non-technical users, business users, product operators, and managers
- People who understand the business goal but do not know how to translate it into Agent instructions
- Users who want to align requirements before asking Cursor, Claude Code, Codex, OpenClaw/OpenHands, ChatGPT/GPT, or another Agent to execute
- People who want better AI collaboration without becoming prompt engineering experts

## How It Works

The Skill chooses the right collaboration mode based on how clear the request is:

- **Demand Alignment Mode**: asks a few high-leverage questions when the idea is still rough.
- **Assumption + Prompt Mode**: states reasonable assumptions and generates a copy-ready prompt when the request is mostly clear.
- **Direct Prompt Compile Mode**: directly produces a prompt when the task is clear enough.
- **Evaluation Mode**: compares raw-prompt results against Skill-path results to judge whether downstream output improves.

## Non-Execution Boundary

This Skill clarifies and compiles prompts. It does not perform the underlying task unless separately asked outside this Skill.

Examples:

- For a Claude Code or Codex repo-editing prompt, it generates the prompt only; it does not edit the repo.
- For a Cursor workspace prompt, it generates the prompt only; it does not modify files.
- For OpenClaw/OpenHands or browser automation tasks involving sending, publishing, purchasing, deleting, or deploying, it generates the prompt and includes human approval gates.

## Repository Structure

```text
ai-collaboration-translator/
├── SKILL.md
├── README.md
├── .gitignore
├── references/
│   ├── prompt-patterns.md
│   └── evaluation-harness.md
└── agents/
    └── openai.yaml
```

## Files

- [SKILL.md](SKILL.md): Skill trigger description, workflow, clarification policy, output rules, and success criteria.
- [references/prompt-patterns.md](references/prompt-patterns.md): Prompt patterns for different target agents and task types.
- [references/evaluation-harness.md](references/evaluation-harness.md): Lightweight protocol for evaluating downstream output improvement.
- [agents/openai.yaml](agents/openai.yaml): Skill interface metadata.

## Validation

Basic structure validation:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py ./ai-collaboration-translator
```

For effectiveness validation, use 12-20 realistic cases:

```text
Baseline path: raw prompt → target Agent → output
Skill path: raw prompt → this Skill → improved prompt → target Agent → output
```

Compare downstream output quality, not just prompt polish.

Primary metric:

```text
Skill Uplift = downstream_output_score(skill_path) - downstream_output_score(baseline_path)
```

See [references/evaluation-harness.md](references/evaluation-harness.md) for the full lightweight evaluation protocol.
