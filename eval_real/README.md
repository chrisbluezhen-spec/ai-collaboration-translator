# eval_real — 真实 Case 盲评轨道

8 条来自 `cases.jsonl` 的用户式 prompt；各版本输出在 `runs/case_NNN/v*_output.md`；oracle 定义在 `oracles.jsonl`。

## 读结论

- **五版本（V0–V4）主报告**：`eval_real_5way_report.md`（2026-05-03）
- **四版本 + 方法论**：`eval_real_4way_report.md`
- **中文长文**：`eval_real_report_detailed_zh.md`

## 复现汇总分数

在**仓库根**（与 `eval_real/` 同级）执行：

```bash
cd "$(git rev-parse --show-toplevel)" 2>/dev/null || exit 1
python3 eval_real/blind_setup.py   # 依赖 runs/ 下已有各版本 output
python3 eval_real/aggregate.py
```

`aggregate.py` / `blind_setup.py` 使用脚本所在目录为 `BASE`，勿写死本机路径。

## 版本快照

`skills/SKILL_v1.md` … `SKILL_v4.md` 用于对照实验；与根目录 `SKILL.md` 对齐的当前规范见 **`SKILL_v4.md`**（应与根 `SKILL.md` 内容一致）。
