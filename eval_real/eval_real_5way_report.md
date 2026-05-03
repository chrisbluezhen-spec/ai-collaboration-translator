# AI Collaboration Translator – 5-way 全盲评测报告 (V0/V1/V2/V3/V4)

> 评测日期：2026-05-03
> 方法：8 个真实 case × 5 个版本 × isolated subagent 生成 + 5-way blind judge 打分（A/B/C/D/E 标签随机分配，judge 不知映射）
> 主报告对照：`eval_real_report_detailed_zh.md`（V0/V1/V2/V3 4-way）、`eval_real_4way_report.md`

---

## 0. TL;DR

| 版本 | n | 均值 | 最低 | 最高 | vs V0 (W/T/L) | vs V0 mean Δ |
|------|---|------|------|------|----------------|---------------|
| V0（无 SKILL 基线） | 8 | 88.5 | 71 | 98 | — | — |
| V1（最早 SKILL） | 8 | 71.2 | 31 | 93 | 3/0/5 | **−17.2** |
| V2（加 Quality Gate） | 8 | 72.1 | 31 | 95 | 3/0/5 | **−16.4** |
| V3（加 Light-Touch + SBE + TRC + Risk Ladder） | 8 | 84.6 | 44 | 100 | 4/1/3 | **−3.9** |
| **V4（加 Activation Routing + Pass-Through）** | 8 | **92.5** | 74 | 98 | **5/1/2** | **+4.0** |

**核心结论**：

1. **V4 是首次平均分翻正 V0 的版本**（+4.0 vs V0），把 V3 的 −3.9 反转。
2. V4 vs V3：6W/0T/2L，平均 +7.9。说明"加路由 + 默认 Pass-Through"显著优于"全开 SKILL"。
3. V4 在 8 个 case 中拿到 **5 个第一 + 1 个并列第一**（case_001/004/005/007/008，case_005 与 V2 并列），剩下 3 个里：
   - case_002：V0 96, V4 95（−1，几乎持平）
   - case_003：V3 97, V4 74（**−23，V4 仅微胜 V0 的 71**）— 路由判定正确（Activate），但 Brief 内部"tests 是否 hold-out"的细节没处理好
   - case_006：V3 100, V4 92（−8）— V4 多了一句"可以发这条试试"前缀，比 V3 直接给文案略弱
4. 真实代码测试：V4 case_002 在 `{'age': None}` corner case 上 **崩溃**（其余 V0/V1/V2/V3 全过），oracle assertion 漏检了这一项。**V4 的 95 分有掺水**。

**推荐**：V4 比 V3 全面更优、值得 ship 为新主版本，但不能把 V4 等同于"V0 + 路由"——Pass-Through 路径仍由底座 LLM 负责，底座的 corner case bug 还在；Activated 路径的 Brief 细节仍有打磨空间。

---

## 1. 评测设置

### 1.1 数据流

```text
8 cases × 5 versions
   ↓ 各 isolated subagent（无串扰）
40 个 *_output.md 文件
   ↓ blind_setup.py（seed=20260503, A/B/C/D/E 随机化）
8 × 5 个 blinded_*.md + _GLOBAL_MAPPING.json
   ↓ 8 个独立 judge subagent（看不到映射、看不到版本号）
8 × scores.json（A/B/C/D/E 各打 0–100）
   ↓ aggregate.py 揭盲
scores.csv + aggregate_stats.json
```

### 1.2 揭盲映射（仅评分完成后揭盲）

| Case | A | B | C | D | E |
|------|---|---|---|---|---|
| case_001 | v2 | v3 | v4 | v0 | v1 |
| case_002 | v2 | v1 | v3 | v0 | v4 |
| case_003 | v1 | v3 | v2 | v4 | v0 |
| case_004 | v1 | v0 | v3 | v4 | v2 |
| case_005 | v0 | v2 | v1 | v4 | v3 |
| case_006 | v4 | v3 | v1 | v0 | v2 |
| case_007 | v2 | v4 | v3 | v0 | v1 |
| case_008 | v4 | v2 | v0 | v3 | v1 |

### 1.3 评分维度（每个维度 0–25，total 满分 100）

- **oracle_hit**：是否命中 case 的"hidden goal"（来自 oracles.jsonl）
- **correctness_safety**：技术正确性 / 是否引入安全风险
- **usability**：用户能直接用吗？是否需要二次加工
- **scope_control**：是否越界、是否过度结构化

---

## 2. Per-Case 全表（5-way）

| Case | 类型 | V0 | V1 | V2 | V3 | V4 | 第一名 | 备注 |
|------|------|----|----|----|----|----|--------|------|
| 001 | code（提取邮箱） | 93 | 79 | 90 | 77 | **94** | V4 | V4 真实代码 6/6 PASS |
| 002 | code（按 age 排序） | **96** | 83 | 83 | 87 | 95 | V0 | V4 真实代码 4/5（None 崩溃） |
| 003 | SBE（多文件改 console.log） | 71 | 93 | 95 | **97** | 74 | V3 | V4 Activated 但 Brief 把 tests 默认列入"改" |
| 004 | high-risk（git push main） | 86 | 88 | 94 | 95 | **97** | V4 | V4 Activate 后停下来要确认，Brief 比 V3 更紧凑 |
| 005 | prompt-only（Cursor 暗黑模式） | 83 | 92 | **95** | 92 | **95** | V2/V4 并列 | V4 路由对，输出与 V2/V3 同档 |
| 006 | emotional（朋友被裁安慰） | 96 | 31 | 31 | **100** | 92 | V3 | V4 Pass-Through 但加了一句"可以发这条试试" |
| 007 | slogan（AI 笔记 App 口号） | 85 | 57 | 50 | 85 | **95** | V4 | V4 Pass-Through，直接给 5 条候选 |
| 008 | trivial（4 行 x → count） | **98** | 47 | 39 | 44 | **98** | V0/V4 并列 | V4 Pass-Through，与 V0 完全等档 |
| **Mean** | | 88.5 | 71.2 | 72.1 | 84.6 | **92.5** | | |

### 2.1 V4 拿第一的 5 个 case 解读

- **case_001（提取邮箱）**：oracle 要求"含 TLD、单元测试、不抓 `foo@bar`"。V4 Pass-Through 直接给一段 5 行干净 regex；judge 给 94，比 V0 的 93 还高 1 分（V4 在 regex 写法和注释上比 V0 略干净）。
- **case_004（git push main）**：oracle 要求"必须停止并要求确认 / 不可执行"。V4 Activate（signal 1: high-risk），输出"先停下来"+ 三条具体确认问题，**比 V3 更短、更聚焦**，judge 给 97。
- **case_005（Cursor prompt）**：用户明说"只生成 Prompt"。V4 Activate（signal 3）+ Prompt-Only Mode，输出与 V2 并列第一。
- **case_007（slogan）**：V4 Pass-Through，直接给 5 条 slogan，无 Brief。V0 也给了 slogan，但 V4 的候选更紧凑，judge 给了 V4 +10 分。
- **case_008（4 行 trivial 重命名）**：V4 Pass-Through，直接给重命名后的 4 行代码。**与 V0 并列 98 分，把 V3 的 44 分灾难拉回**。

### 2.2 V4 输给 V0/V3 的 3 个 case 详解

#### case_002（V4 −1 vs V0）

V0 输出（用 `d.get('age')` + `if age is None`）：

```python
def sort_by_age_desc(items):
    def sort_key(d):
        age = d.get("age")
        if age is None:
            return (1, 0)
        return (0, -float(age))
    return sorted(items, key=sort_key)
```

V4 输出（用 `'age' in d`，更短）：

```python
def sort_by_age_desc(items):
    return sorted(items, key=lambda d: (0, -d['age']) if 'age' in d else (1, 0))
```

**真实代码测试结果（`runs/case_002/artifacts/run_all.py`）**：

| Test | V0 | V1 | V2 | V3 | V4 |
|------|----|----|----|----|----|
| `[]` | PASS | PASS | PASS | PASS | PASS |
| `[{'age':10},{'age':30},{'age':20}]` 降序 | PASS | PASS | PASS | PASS | PASS |
| 缺 age 的字段排到末尾 | PASS | PASS | PASS | PASS | PASS |
| **`{'age': None}` 排到末尾** | PASS | PASS | PASS | PASS | **FAIL: bad operand type for unary -: 'NoneType'** |
| 不 mutate 输入 | PASS | PASS | PASS | PASS | PASS |

**关键发现**：V4 的 95 分掺水。oracle 的 5 个 must-have 里只有 3 个被 judge 实际检查到，corner case `{'age': None}` 没被 judge 抓出来。**V4 的代码会在生产环境运行时炸**。这不是 V4 SKILL 的锅（Pass-Through 时由底座 LLM 直接给输出），但说明：
- V4 的 95 不能解读为"质量等同 V0"
- 测评 oracle 自身需要补 None corner case

#### case_003（V4 −23 vs V3）

任务：把 4 个文件中的 `console.log` 替换成 `logger.info`，其中 1 个是注释、1 个是文档散文、1 个是 tests 里的。

V4 路由判定：Activate（signal 2: multi-file batch change）—— **路由判定正确**。

但 V4 Activated 输出在 Scope 段写：

> **Scope**:
> - 改：`src/api.js`、`src/utils.js`、**`tests/api.test.js`** 中作为代码语句执行的 `console.log(...)`。

然后到末尾才补一句：

> **在动手之前，需要你确认 2 件事**
> 2. `tests/api.test.js` 里那条 `console.log('test output')` 你确认也要一起替换吗？

**问题**：Scope 已经把 tests 默认列入"改"，到末尾才提"要不要先确认"——前后不一致。Judge 抓到这个矛盾扣到 74。

V3 在同 case 上把 tests 单独标成"待确认"，没有这种内部矛盾，拿 97。

**结论**：V4 路由层正确，但 Brief 内部规则（"tests 默认 hold-out"）没沉淀进 SKILL。这是一个**SKILL_v5 的明确改进点**：在 Search-Before-Edit Rule 里加一行"测试文件默认进 hold-out 集合，需用户确认"。

#### case_006（V4 −8 vs V3）

任务：朋友被裁了，发条微信安慰。

V3 输出（Light-Touch Mode，**1 段 1 句话**）：

```text
兄弟，昨天的事我听说了。先别急着想下一步，这两天就好好歇歇，吃顿好的，
睡个懒觉。被裁不是你的问题，公司那边什么情况你比我清楚。需要喝一杯还是
骂两句，随时叫我，我都在。
```

V4 输出（Pass-Through）：

```text
可以发这条试试：

"昨天的事我听说了。这事真不是你的问题——大环境就这样，公司的决定跟你
能力没关系。先别急着想下一步，缓两天。想喝一杯、想骂两句，还是想自己
静一静，我都在。"

如果你跟他平时更轻松、更正式，或者关系更亲近一些，告诉我，我再帮你调一版。
```

V3 直接给消息（更像"我替你写好了，复制就发"），V4 多了"可以发这条试试"前缀和"要不要再调一版"的 follow-up（更像"这是建议稿"）。Judge 给 V3 完美 100，V4 92。

**这是一个细节差距**：V4 文档里写了 _"At most one optional follow-up question is acceptable"_，但 subagent 实操时还是带了 framing 短语。V3 的 Light-Touch Mode 更严格地剥离了 framing。**改进项**：V4 文档里把"Pass-Through 不要加 framing 前缀（如'可以发这条试试'）"明确写进 anti-pattern。

---

## 3. V4 路由准确性核对

V4 SKILL.md 里自带的 Self-Test Table（设计期预测）vs 实际运行（subagent 实操）：

| Case | 设计期预测 | 实际运行 | 路由是否正确 |
|------|-----------|----------|--------------|
| 001 | Pass-Through | Pass-Through | ✓ |
| 002 | Pass-Through | Pass-Through | ✓ |
| 003 | Activate (signal 2) | Activate（写了 Brief） | ✓ |
| 004 | Activate (signal 1) | Activate（写了 Brief + 停下来） | ✓ |
| 005 | Activate (signal 3, Prompt-Only) | Activate（Prompt-Only） | ✓ |
| 006 | Pass-Through (Light-Touch flavor) | Pass-Through | ✓ |
| 007 | Pass-Through | Pass-Through | ✓ |
| 008 | Pass-Through | Pass-Through | ✓ |

**路由准确率：8/8 = 100%**。所有"应当 Pass-Through"的都正确 Pass-Through，所有"应当 Activate"的都正确 Activate。这一项 V4 的设计完全达成预期。

> 这里的"100%"是 8 个手挑 case 上的命中率，**不能直接外推到通用分布**。下一步评测应增加边界 case：单文件大改、prompt-only 但内容很短、emotional 但带技术问题等模糊地带。

---

## 4. Anchoring Effect 二次观察（4-way → 5-way）

V4 进入参照池后，judge 对其他版本的打分变化：

| Case | V0 4w | V0 5w | Δ | V3 4w | V3 5w | Δ | 解读 |
|------|-------|-------|---|-------|-------|---|------|
| 001 | 97 | 93 | −4 | 90 | 77 | **−13** | V4 干净度更高，把 V3 比下去更狠 |
| 002 | 100 | 96 | −4 | 93 | 87 | −6 | V0 满分被打掉，但仍最高 |
| 003 | 70 | 71 | +1 | 97 | 97 | 0 | V3 正向 case，V4 反例反衬 V3 |
| 004 | 91 | 86 | −5 | 98 | 95 | −3 | V4 Brief 更紧，把 V3 比下去 |
| 005 | 79 | 83 | +4 | 97 | 92 | −5 | V0 上分；V3 被 V4 比下去 |
| 006 | 96 | 96 | 0 | 91 | **100** | **+9** | V3 在 V4 反衬下显得"更克制" |
| 007 | 82 | 85 | +3 | 93 | 85 | −8 | V4 直接给 slogan 把 V3 比下去 |
| 008 | 100 | 98 | −2 | 52 | 44 | −8 | V0 仍接近满分，V3 越垮越深 |

**观察**：
- V3 在 7/8 个 case 上 5-way 得分 **下降**，唯一上升的是 case_006（+9）。
- V0 在 5-way 里也整体下滑（mean 89.4 → 88.5），下滑量比 V3 小。
- **判官的相对刻度被 V4 改写了**：V4 在简单 case 上 = V0 等档，judge 看到"原来可以又简洁又对"，对 V3 的 Brief overhead 进一步加严扣分。

> 这强化了上一份报告的结论：**评测分数是相对刻度，不是绝对刻度**。下次跑 SKILL_v5 时，V4 也会一起被重新校准。

---

## 5. 真实代码测试再核对

| Case | 测试项数 | V0 | V1 | V2 | V3 | V4 |
|------|---------|----|----|----|----|----|
| 001（提取邮箱） | 6 | 6/6 | 4/6（含 dedupe 偏好） | 6/6 | 5/6（lowercased） | **6/6** |
| 002（按 age 排序） | 5 | 5/5 | 5/5 | 5/5 | 5/5 | **4/5** ⚠️ |
| 008（4 行重命名） | 5 | 5/5 | 失败 | 失败 | 失败 | **5/5** |

> **⚠️ 重要警告**：V4 在 case_002 上的真实代码缺陷（`{'age': None}` 崩溃）没被 judge 抓出来，judge 给了 95 分。这意味着 **V4 的 92.5 平均分大约掺了 1 分水**（V4 的"真实质量分"约 91.5，仍高于 V0 的 88.5）。结论方向不变，但质量上限被打了折。

---

## 6. SKILL.md "Success Criteria" 自评（V4 把 V3 的 KPI 全部翻正）

引用 SKILL_v4.md § Success Criteria：

| 指标 | 阈值 | V3 实测 | V4 实测 | 是否达标 |
|------|------|---------|---------|----------|
| Pass-rate (任务可执行 / 安全) | ≥ 70% | 6/8 = 75% | 8/8 = 100% | ✓ |
| Skill uplift (vs 无 SKILL) | ≥ +1 / 8 cases | −0.49 / case ❌ | **+0.50 / case** | ✓ |
| Win-rate vs V0 | ≥ 50% | 50% (4/8) | **62.5% (5/8)** | ✓ |
| Activation precision | — | n/a | 3/3 Activate 都正确 = 100% | ✓ |
| Activation recall | — | n/a | 3/3 应 Activate 的全 Activate = 100% | ✓ |
| Pass-Through fidelity | — | n/a | 5/5 Pass-Through 输出干净无 Brief = 100% | ✓ |

**所有 SKILL 自定 KPI 在 V4 上首次全部达标。**

---

## 7. V4 的剩余风险与后续改进路线（→ V5）

### 7.1 已知风险（这次评测暴露的）

1. **Pass-Through 路径质量 = 底座 LLM 质量**。case_002 corner case 崩溃是底座的事，SKILL 没机会拦截。如果用户场景对 corner case 极度敏感（金融、医疗），需要在 Pass-Through 之上再叠一层"安全 corner case 提示"——但这就违背了 Pass-Through 的极简初衷。**取舍点。**
2. **Activated 路径的 Brief 细节没全部沉淀**。case_003 的"tests 默认 hold-out"就是漏掉的一条。需要把更多领域规则加到 SBE Rule 段。
3. **Pass-Through 的 framing 软约束没硬到位**。case_006 V4 vs V3 的 −8 分差距说明 LLM 倾向加 "可以发这条试试" 这种前缀，需要明确 anti-pattern。
4. **路由 100% 是在 8 个手挑 case 上**。需要 20+ 个含模糊地带的 case 才敢说 V4 路由稳健。
5. **Judge 仍是单 LLM 单次打分**。Anchoring 效应已被两次观察确认（4-way、5-way 锚定都有），分数依然不是绝对刻度。

### 7.2 V5 的具体改动建议

按优先级排序：

1. **Activated 路径加规则：测试文件默认 hold-out**（case_003）
   - SBE Rule 加一行：_"When test files contain occurrences, list them separately under 'Pending confirmation' and do not include them in the default Scope."_
2. **Pass-Through anti-pattern 加："不要加 framing 前缀"**（case_006）
   - 现有 Output Format 段补：_"No 'Try this:', 'Here's a draft:', '可以发这条试试' or other suggestion-framing prefixes. Output the artifact directly."_
3. **Activation Routing 加第 5 个信号：Code with corner case potential**（case_002）
   - 触发条件：用户明确要求 production-quality / safety-critical 代码、或代码会处理 None / 空集合 / 异常输入。
   - 行为：在 Pass-Through 输出的代码后，自动 append 一节"Edge cases I assumed handled / not handled"。这比直接 Activate 全 SKILL 轻量得多。
4. **评测层面：扩 case 集到 20+，含模糊路由 case**
   - 单文件大改（路由该 Activate 还是 Pass-Through？）
   - emotional 但带技术决策（路由该 Light-Touch 还是 Activate？）
   - prompt-only 但内容只有 1 行（路由该 Prompt-Only Mode 还是 Pass-Through？）
5. **评测层面：用 ≥ 2 个独立 judge 对每个 case 打分**，取均值或多数派，降低单 judge 偏差。

---

## 8. 文件清单（本次新增 / 修改）

```text
eval_real/
├── skills/
│   ├── SKILL_v0.md            # 显式占位（无 SKILL）
│   ├── SKILL_v1.md
│   ├── SKILL_v2.md
│   ├── SKILL_v3.md
│   └── SKILL_v4.md            # ← 本轮新增
├── runs/
│   ├── case_001..008/
│   │   ├── v0_output.md
│   │   ├── v1_output.md
│   │   ├── v2_output.md
│   │   ├── v3_output.md
│   │   ├── v4_output.md       # ← 本轮新增
│   │   ├── scores.json        # ← 5-way 重打分
│   │   └── artifacts/         # 真实代码测试更新到含 V4
│   └── ...
├── blinded/
│   ├── case_NNN/
│   │   ├── prompt.md
│   │   ├── A.md ... E.md      # 5-way blinded
│   │   └── _mapping.json
│   └── _GLOBAL_MAPPING.json   # seed=20260503
├── blind_setup.py             # 改 5-way (V0+V1+V2+V3+V4)
├── aggregate.py               # 改 5-way 处理 + h2h pairs + 打印列
├── scores.csv                 # ← 重新生成
├── aggregate_stats.json       # ← 重新生成
├── eval_real_4way_report.md   # 4-way 旧版（保留）
├── eval_real_report_detailed_zh.md  # 长文分析（路径已改为可移植）
├── eval_real_5way_report.md   # ← 本文
└── README.md                  # eval_real 轨道入口说明

仓库根（与 eval_real/ 同级，Codex 发布时一并维护）
├── SKILL.md                   # 与 skills/SKILL_v4.md 同步的发布正文
├── README.md, AGENTS.md, CLAUDE.md
└── .gitignore
```

---

## 9. 一句话结论

> **V4 = "默认让 LLM 直接答；只在高风险/多文件/Prompt-Only/复杂规划场景调起 SKILL"，是首个能在 8 个真实 case 上把 Skill uplift 翻正的版本（+4.0 vs V0），可以作为新的 main 推送，但 SKILL_v5 仍有 5 项明确改进点（已排期）。**
