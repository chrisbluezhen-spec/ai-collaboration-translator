# AI Collaboration Translator

将模糊想法、口语化需求转成可执行的 Agent 指令或可复制 Prompt；默认**仅在需要时**才套用完整结构化流水线（V4：Activation Routing + Pass-Through）。

**上游仓库**：<https://github.com/chrisbluezhen-spec/ai-collaboration-translator>

## 仓库结构

| 路径 | 说明 |
|------|------|
| `SKILL.md` | 当前发布的 Skill 正文（与 `eval_real/skills/SKILL_v4.md` 同步维护） |
| `references/prompt-patterns.md` | Prompt 模式与反模式参考 |
| `references/evaluation-harness.md` | 评测协议（含 `eval_oracle` 与 `eval_real` 说明） |
| `agents/` | Agent 配置片段 |
| `eval_oracle/` | 24 条 Oracle 门控评测（历史基线） |
| `eval_real/` | 8 条真实 case 的隔离子 Agent 生成 + 全盲打分（V0–V4）；入口说明见 `eval_real/README.md` |

## 快速复现 `eval_real` 汇总

在仓库根目录执行（脚本使用 `__file__` 解析路径，可在任意机器上运行）：

```bash
cd eval_real
python3 blind_setup.py    # 需先有 runs/case_*/v*_output.md
python3 aggregate.py     # 生成 scores.csv、aggregate_stats.json
```

主结论见 `eval_real/eval_real_5way_report.md`（2026-05-03 五版本全盲）。

## 版本快照

`eval_real/skills/` 下保留 `SKILL_v1.md` … `SKILL_v4.md` 用于对照实验与论文式 diff；**对外发布以根目录 `SKILL.md` 为准**。

## 发布到 GitHub（Codex）

1. 确认根目录 `SKILL.md` 即为要发布的版本。
2. 不要提交密钥、本地 MCP 配置或个人路径。
3. 若缩减仓库体积，可考虑将 `eval_real/blinded/` 大段生成物改为 CI 再生成（当前为可复现评测资产，默认保留）。
