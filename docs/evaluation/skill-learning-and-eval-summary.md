# AI Collaboration Translator — Skill 学习与评测简报 / Skill Learning and Evaluation Summary

**版本 / Version**: v4（Activation Routing + Pass-Through）
**日期 / Date**: 2026-05-03

---

## 两套评测分别是什么

| 目录 | 规模 | 用途 |
|------|------|------|
| **`eval_oracle/`** | 24 条合成用例 | Oracle 门控、发布门叙事、竞品方法论沉淀（见下文 v3 摘要） |
| **`eval_real/`** | 8 条真实 prompt + 隔离子 Agent 输出 + 全盲 judge | 验证 V0–V4 在「有 V0 基线锚定」下的相对表现；主报告：`eval_real/eval_real_5way_report.md` |

二者互补：**eval_oracle** 偏制度与覆盖率；**eval_real** 偏真实分布与盲评锚定效应。

---

## v4 相对 v3 的增量（2026-05-01 → 2026-05-03）

- **Activation Routing（Step 0）**：默认 Pass-Through，仅在「高风险 / 多文件批量 / 显式 Prompt-Only / 复杂模糊规划」四信号之一命中时激活完整 Skill。
- **动机**：4-way 盲评显示 V3 在简单任务上相对 V0 的「结构化税」被 judge 重罚；V4 把税收到高价值场景。
- **证据**：`eval_real` 五版本全盲均值 V4 **92.5** > V0 **88.5**（Skill uplift 翻正）；细节、局限与 case_002 真实单测 corner case 见 `eval_real/eval_real_5way_report.md`。

---

## 中文摘要（eval_oracle / v3 基线，仍有效）

### 本次学习了什么（方法论来源）

1. **Agent Prompt Optimizer** → Action 安全分级（Safe / Low / Medium / High-risk）
2. **EARS-style Requirement Optimizer** → 模糊需求 → 可测试验收标准
3. **PromptHub/LangSmith** → 评测作为持续发布门
4. **自身 B02 回归** → 情感写作不能套用结构化 Brief

### v3 起新增内容（已并入当前根 `SKILL.md`，部分仅在 Activated 路径生效）

| 新增内容 | 目的 |
|---------|------|
| Light-Touch Mode（Mode F） | 情感写作保留语气 |
| Action Risk Ladder | 高风险动作审批门 |
| Search-Before-Edit Rule | 多文件替换先搜后改 |
| Testable Requirement Conversion | 代码/数据任务可测试化 |
| Oracle Eval as Release Gate | 发布门制度 |
| **v4：Activation Routing + Pass-Through** | 简单任务不交「结构化税」 |

### eval_oracle 评测结果（历史记录）

- 24 个用例，平均 Oracle Uplift **+29.4**（相对上一轮 +27.6）
- 胜率 96%，B02 类回归已修
- 8 条发布门通过 — **该轨道裁定：PASS**

---

## English Summary (eval_oracle baseline — still valid)

Competitor learnings → Action Risk Ladder, TRC, SBE, Light-Touch, continuous eval gate. v4 adds **routing** so overhead applies only when signals fire. For **empirical blind scores on real cases**, see `eval_real/eval_real_5way_report.md`.

---

## Files Modified / Created（滚动清单，截至 2026-05-03）

```
SKILL.md                                      ← V4 canonical（与 eval_real/skills/SKILL_v4.md 同步）
AGENTS.md                                     ← 仓库内 Agent 约定
README.md                                     ← 人类与 Codex 接入说明
.gitignore                                    ← .DS_Store / venv 等
references/prompt-patterns.md                 ← 模式参考
references/evaluation-harness.md              ← 协议 + eval_real 指针
eval_oracle/*                                 ← 24-case Oracle 轨道
eval_real/*                                   ← 8-case 盲评轨道与报告
docs/evaluation/skill-learning-and-eval-summary.md  ← 本文件
```
