# AI Collaboration Translator / AI 协作翻译器

## 中文说明

**AI Collaboration Translator** 是一个帮助用户更好地和 AI/Agent 协作的 Skill。

它不是普通的 Prompt Optimizer。它的核心作用是：帮助非技术用户、业务用户，或者“很有想法但表达不够结构化”的用户，把粗糙想法、模糊需求、半成品指令，转化成 AI/Agent 更容易理解、执行、验证的执行 Brief 或 Prompt。

核心流程：

```text
粗糙想法 / 模糊需求
→ 需求对齐
→ 必要时澄清
→ 结构化执行 Brief 或 Prompt
→ 当前 Agent 执行，或交给目标 Agent 执行
→ 验证与汇报
```

这个 Skill 的目标不是让 Prompt 看起来更“专业”，而是让 AI/Agent 更少误解、更少猜测，并更容易产出可用的第一版结果。

## 两种使用方式

### Compile-then-Execute Mode

当它运行在 Claude Code、Codex、Cursor 或类似可执行 Agent 环境里，并且任务可以在当前工作区安全完成时，这是默认模式。

Skill 会先把你的粗糙需求编译成一个结构化执行 Brief，然后把这个 Brief 当作当前 Agent 的任务说明继续执行。它会优先检查当前仓库或工作区，做最小范围的合理修改或产出，并在完成后汇报修改内容、验证结果和剩余风险。

只有在遇到关键决策、缺失的关键信息，或破坏性、公开、昂贵、外部、不可逆、影响生产环境的动作时，才应该停下来问你。

### Prompt-Only Mode

当你明确想要一段给另一个 Agent 粘贴的 Prompt，或者任务属于当前环境无法安全执行的外部自动化、发消息、发布、购买、删除、部署等场景时，使用 Prompt-Only Mode。

例如：

- “只生成 Prompt，不要执行”
- “给我一段给 Cursor 的 Prompt”
- “帮我写给 OpenClaw 的浏览器自动化 Prompt”

在 Prompt-Only Mode 下，Skill 只生成可复制 Prompt，然后停止。

## 适合谁使用

- 有明确想法，但表达还不够结构化的人
- 非技术用户、业务用户、产品/运营/管理者
- 知道业务目标，但不知道如何把目标翻译成 Agent 指令的人
- 想先和 AI 对齐需求，再交给当前 Agent 或另一个 Agent 执行的人
- 想提升 AI 协作质量，但不想成为 Prompt Engineering 专家的人

## 如何使用

你可以把粗糙需求直接交给这个 Skill，例如：

- “我有个想法，但不知道怎么跟 AI 说”
- “帮我写给 Claude Code 的 Prompt”
- “把这个需求转成 Cursor 能执行的 Prompt”
- “先帮我对齐需求，再生成 Prompt”
- “Update README.md to clarify the new behavior. Keep the edit minimal.”

Skill 会根据需求清晰度和执行环境选择模式：

- **Compile-then-Execute Mode**：可安全执行时，先编译执行 Brief，再直接执行。
- **Prompt-Only Mode**：用户明确只要 Prompt，或任务属于另一个环境时，只生成 Prompt。
- **需求对齐模式**：当想法还不够清楚或执行风险较高时，先提出少量高价值问题。
- **评估模式**：当你想验证这个 Skill 是否有效时，比较原始路径和 Skill 路径的输出质量。

## 执行边界

这个 Skill 可以执行当前环境中安全、局部、可验证的任务，也可以只生成 Prompt。

它不应该在没有确认的情况下执行以下动作：

- 删除或覆盖重要数据
- 发送消息、提交表单、发布内容
- 购买、付款或产生费用
- 部署、改生产配置、影响外部系统
- 执行不可逆或高风险动作

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

- [SKILL.md](SKILL.md)：Skill 的触发说明、工作流、执行边界、澄清策略、输出规则和评估标准。
- [references/prompt-patterns.md](references/prompt-patterns.md)：不同目标 Agent 和任务类型的 Prompt / Brief 模式。
- [references/evaluation-harness.md](references/evaluation-harness.md)：用于评估 Skill 是否改善 AI/Agent 输出的轻量协议与自测案例。
- [agents/openai.yaml](agents/openai.yaml)：Skill 的界面元数据。

## 验证方法

基础结构校验：

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py ./ai-collaboration-translator
```

效果验证建议使用 12-20 个真实或接近真实的测试案例：

```text
Baseline path: 原始请求 → Agent 直接处理 → 输出
Skill path: 原始请求 → 本 Skill → 执行 Brief 或 Prompt → 执行 → 输出
```

重点比较最终输出质量，而不是只比较 Prompt 是否更好看。

核心指标：

```text
Skill Uplift = output_score(skill_path) - output_score(baseline_path)
```

详见 [references/evaluation-harness.md](references/evaluation-harness.md)。

---

## English

**AI Collaboration Translator** is a Skill for helping people collaborate better with AI agents.

It is not a generic prompt optimizer. Its purpose is to help non-technical users, business users, and people with strong ideas but loosely structured expression turn rough thoughts, vague requirements, or half-formed instructions into execution briefs or prompts that AI agents can understand, execute, and verify.

Core workflow:

```text
Rough idea / vague request
→ Requirement alignment
→ Clarification when needed
→ Structured execution brief or prompt
→ Current-Agent execution, or target-Agent execution
→ Verification and report
```

The goal is not to make every prompt sound polished. The goal is to preserve the user's real intent and help the responsible AI/Agent produce a useful first-pass result with fewer corrections.

## Two Usage Styles

### Compile-then-Execute Mode

This is the default when the Skill runs inside Claude Code, Codex, Cursor, or a similar executable Agent environment and the task can be safely performed in the current workspace.

The Skill compiles the raw request into a structured execution brief, then treats that brief as the active task instruction for the current Agent. It should inspect the relevant workspace context, make the smallest coherent change or produce the requested artifact, verify the result, and report changed files, checks, and remaining risks.

It should ask the human only when there is a real decision, missing critical information, or a destructive, public, expensive, external, irreversible, or production-affecting action.

### Prompt-Only Mode

Use this when the user explicitly wants a prompt for another Agent, or when execution belongs to another environment or involves external side effects such as browser automation, sending messages, publishing, purchasing, deleting, or deployment.

Examples:

- "Only generate the prompt; do not execute."
- "Give me a prompt for Cursor."
- "Write an OpenClaw browser automation prompt."

In Prompt-Only Mode, the Skill generates a copy-ready prompt and stops.

## Who It Is For

- Users with strong ideas but loosely structured expression
- Non-technical users, business users, product operators, and managers
- People who understand the business goal but do not know how to translate it into Agent instructions
- Users who want to align requirements before asking the current Agent or another Agent to execute
- People who want better AI collaboration without becoming prompt engineering experts

## How It Works

The Skill chooses the right collaboration mode based on clarity, user intent, and execution environment:

- **Compile-then-Execute Mode**: compile an execution brief and execute when safe.
- **Prompt-Only Mode**: generate a prompt only when explicitly requested or execution belongs elsewhere.
- **Demand Alignment Mode**: ask a few high-leverage questions when the idea is too unclear or risky.
- **Evaluation Mode**: compare raw-path results against Skill-path results to judge whether output improves.

## Execution Boundary

This Skill may execute safe, local, scoped, and verifiable tasks in the current environment. It may also generate prompts for other Agents.

It should not proceed without confirmation before:

- Deleting or overwriting important data
- Sending messages, submitting forms, or publishing content
- Purchasing, paying, or creating costs
- Deploying, changing production configuration, or affecting external systems
- Performing irreversible or high-risk actions

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

- [SKILL.md](SKILL.md): Skill trigger description, workflow, execution boundary, clarification policy, output rules, and success criteria.
- [references/prompt-patterns.md](references/prompt-patterns.md): Prompt and brief patterns for different target agents and task types.
- [references/evaluation-harness.md](references/evaluation-harness.md): Lightweight protocol and self-tests for evaluating AI/Agent output improvement.
- [agents/openai.yaml](agents/openai.yaml): Skill interface metadata.

## Validation

Basic structure validation:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py ./ai-collaboration-translator
```

For effectiveness validation, use 12-20 realistic cases:

```text
Baseline path: raw request → Agent handles it directly → output
Skill path: raw request → this Skill → execution brief or prompt → execution → output
```

Compare final output quality, not just prompt polish.

Primary metric:

```text
Skill Uplift = output_score(skill_path) - output_score(baseline_path)
```

See [references/evaluation-harness.md](references/evaluation-harness.md) for the full lightweight evaluation protocol.
