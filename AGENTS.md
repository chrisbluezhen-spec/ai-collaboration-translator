# AGENTS — AI Collaboration Translator

面向在本仓库内工作的 AI Agent（含 Codex、Claude Code、Cursor）。

## 事实

- **当前 Skill 版本**：V4（根目录 `SKILL.md`）。核心变化：Step 0 **Activation Routing**；默认 **Pass-Through**，仅在四信号命中时进入完整 Compile-then-Execute / Prompt-Only / Demand Alignment。
- **历史对照**：`eval_real/skills/SKILL_v{1,2,3,4}.md` 仅用于评测与 diff，不要与根 `SKILL.md` 分叉维护内容——改 Skill 时以根 `SKILL.md` 为准，再按需拷贝到 `SKILL_v4.md`。
- **评测两套**：`eval_oracle/`（24 条、门控叙事）；`eval_real/`（8 条、隔离生成 + 盲评）。新结论以 `eval_real/eval_real_5way_report.md` 为主。

## 约定

- `eval_real/aggregate.py`、`blind_setup.py`、`aggregate_4way.py` 的 `BASE` 均相对脚本所在目录，禁止写死用户主目录路径。
- 修改评测流程时同步更新 `references/evaluation-harness.md` 与 `docs/evaluation/skill-learning-and-eval-summary.md`。
- 文档中示例命令使用「仓库根」或 `eval_real/` 相对路径，不写本机绝对路径。

## 红线

- 不在未授权时代用户执行 git push、部署、删库、发消息、付款等高风险动作；Skill 内 Action Risk Ladder 与路由层已要求审批门。
