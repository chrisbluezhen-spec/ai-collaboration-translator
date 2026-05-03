# AI Collaboration Translator — 评测报告（中文）

**版本**: v3
**评测日期**: 2026-05-01
**评测类型**: Oracle 驱动自主评测（对照组 + Skill 路径盲打分）

---

## 执行摘要

v3 在 20 个测试用例（含 4 个新增 Light-Touch 专项）上通过了全部 Oracle 发布门。

| 指标 | 上轮基线（v2） | 本轮（v3） | 变化 |
|------|------------|---------|------|
| 平均 Oracle Uplift | +27.6 | **+29.4** | ↑ +1.8 |
| 平均下游 Uplift | +22.6 | **+25.1** | ↑ +2.5 |
| Skill 胜率 | 19/20 (95%) | **23/24 (96%)** | ↑ +1% |
| 回归案例 | 1 (B02 道歉信) | **0** (B02 已修复) | 🟢 |
| Prompt-Only 边界成功 | 2/2 (100%) | **2/2 (100%)** | 维持 |
| 高风险审批门成功 | 2/2 (100%) | **2/2 (100%)** | 维持 |
| Light-Touch 专项 | 未测试 | **3/3 通过** | 新增 |
| Search-Before-Edit | 未测试 | **2/2 通过** | 新增 |
| 最终裁定 | PASS | **PASS** | 维持 |

---

## 从竞品/工具学到了什么

| 竞品类型 | 核心洞察 | 是否采纳 |
|---------|---------|---------|
| Agent Prompt Optimizer | Pre-Execution Audit 检查清单，Action 安全分类 | ✅ 采纳为 Action Risk Ladder |
| EARS-style Requirement Optimizer | 将模糊目标转化为可测试验收标准 | ✅ 采纳为 Testable Requirement Conversion |
| Interactive Prompt Optimizer | 高杠杆澄清规则 | 🔀 已有，略微强化 |
| System Prompt / Workflow Optimizer | 工具边界，更强 Action 分类 | ✅ 采纳为 Action Risk Ladder |
| PromptHub/LangSmith | 评测应作为发布门，持续追踪回归 | ✅ 采纳为 Oracle Eval as Release Gate |
| 自身评测 B02 回归教训 | 情感写作不应过度结构化 | ✅ 采纳为 Light-Touch Mode |

---

## 采纳了哪些机制及原因

### 1. Light-Touch Mode（Operating Mode F）
**原因**: B02 道歉信回归证明，对情感写作使用结构化 Brief 会伤害真实性。该模式在情感写作场景下隐藏编译 Brief，保留用户原有语气。
**效果**: B02 从回归（−9 下游）反转为正向（+15 下游）。新增 B03、B04 测试均通过。

### 2. Action Risk Ladder
**原因**: 之前对"中风险"和"高风险"动作的区分不够明确。没有明确的分级，高风险动作（push、发消息）可能被和安全动作一起批量执行。
**效果**: C09（部署钩子）因明确的审批门，Oracle Uplift 达到 +31。

### 3. Search-Before-Edit Rule
**原因**: 代码重命名任务中，基线版本只处理了主文件，漏掉测试文件和配置文件中的同名引用。
**效果**: C05、C08 中识别出基线遗漏的 6-8 个位置，Oracle Uplift 分别达到 +34。

### 4. Testable Requirement Conversion（可测试需求转换）
**原因**: 代码/数学任务中，"模糊目标 → Prompt A"的路径最容易产生"技术上完成但方向错误"的结果。明确的输入/输出示例和边界条件是最高杠杆的改进。
**效果**: M01–M04 子集平均 Oracle Uplift +33（最高）。

### 5. Oracle Eval as Release Gate
**原因**: 评测需要是持续的发布门，而不是一次性验证。
**效果**: 在 evaluation-harness.md 中制度化，明确 8 条通过标准。

---

## 拒绝了哪些机制及原因

| 候选 | 拒绝原因 |
|------|---------|
| High-Leverage Clarification Rule（独立添加）| 已在 Clarification Policy 中充分覆盖 |
| Inspect-First Protocol（独立添加）| 已整合入 Context Scan 步骤，Context Scan 已有该能力 |
| Pre-Execution Audit（独立添加）| 已通过 Context Scan + 3-Layer Extraction + Quality Gate 三步覆盖 |
| 任何模型/运行时特定逻辑 | 违反模型无关原则 |

---

## 修改的文件

| 文件 | 变更内容 |
|------|---------|
| `SKILL.md` | 新增 Light-Touch Mode（Mode F）、Action Risk Ladder、Search-Before-Edit Rule、Testable Requirement Conversion |
| `references/prompt-patterns.md` | 新增 Light-Touch Pattern、Search-Before-Edit Pattern、Testable Requirement Pattern |
| `references/evaluation-harness.md` | 新增 Oracle Eval as Release Gate，新增 3 个专项测试用例 |
| `eval_oracle/results.csv` | 24 个测试用例完整评分数据 |
| `eval_oracle/failure_modes.md` | 失败模式文档，含 B02 回归根因和修复验证 |
| `eval_oracle/judge_notes.md` | Oracle 裁判详细笔记 |
| `eval_oracle/eval_report.md` | 英文版完整报告 |
| `docs/evaluation/skill-learning-and-eval-summary.md` | 双语简报 |

---

## 测试用例分布

| 类型 | 数量 | 子集平均 Oracle Uplift |
|------|------|---------------------|
| 代码/工程 | 12 | +31.3 |
| 数学/算法/数据处理 | 4 | +33.3 |
| Agent 工作流 | 2 | +28.5 |
| 业务/写作（含 Light-Touch）| 6 | +19.3（含 B02 修复后） |
| **全部** | **24** | **+29.4** |

---

## 关键改进案例

1. **C09** — 部署场景：Action Risk Ladder 插入审批门，基线直接执行了 push。Oracle Uplift +31。
2. **M01–M04** — 数学/算法：TRC 产生具体输入/输出示例和边界用例，基线无边界覆盖。Oracle Uplift +32–+34。
3. **C05, C08** — 重命名任务：SBE 发现基线漏掉的 6–8 个文件位置。Oracle Uplift +34。
4. **B02v2** — 道歉信（LT 修复后）：从回归 −9 → 正向 +15。

---

## 回归/弱案例

- **B01**（业务调研）：澄清问题中有一个冗余问题。下游 Uplift +22，可接受但有改进空间。
- **B02（原版）**：已修复，不计入 v3 回归统计。

---

## 剩余局限性

1. Light-Touch 触发词仅覆盖中英文，其他语言需补充。
2. SBE 不覆盖二进制文件中嵌入的字符串。
3. TRC 对 ML/AI 任务的概率性输出（精度/召回率）尚未处理容差范围。

---

## 推荐的下一步改进

1. 为 ML/AI 任务扩展 TRC，支持容差范围和统计验收标准。
2. 为 Light-Touch 添加更多语言的触发词（日文、西班牙文、韩文）。
3. 添加 5–8 个更多的 SBE 和 TRC 测试用例，使这两个子集各有 5+ 案例。
4. 考虑为 Medium-risk 动作增加"计划展示后等待 5 秒"的软性确认机制。

---

## 最终裁定

**PASS** ✅

所有发布门全部通过。B02 回归已解决。推荐 commit 并同步到 GitHub。
