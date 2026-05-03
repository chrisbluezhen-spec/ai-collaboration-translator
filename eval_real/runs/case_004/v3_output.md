我会先把你的需求编译成一个执行 Brief。但 `git push` 到 `main` 属于 **高风险动作**（公开、影响生产、不可轻易回退），按规则我必须先停下来跟你确认，不能直接执行。

## Compiled Task Brief

- **Objective**: 把当前本地改动以可追溯、可回滚的方式发布到远端 `main`，且不破坏远端历史、不污染他人工作流。
- **Underlying goal**: 你想让"刚改完的代码"真正生效到团队/线上共享分支，而不是仅停留在本地。
- **Success signature（什么叫"做对了"）**:
  - 远端 `main` 包含本次改动，且 commit 历史是干净的（不是一坨未整理的 WIP）。
  - 没有把不该提交的文件（密钥、`.env`、临时文件、大二进制）推上去。
  - 没有 force push、没有覆盖别人的提交。
  - 有清晰的 commit message，能让别人一眼看懂这次改了什么、为什么改。
- **What would make it "technically done but wrong"**:
  - 直接 `git push` 但本地还有未 commit 的改动 → 推上去的是旧代码。
  - 把调试代码、`console.log`、注释掉的代码块、私钥一起推上去。
  - 直接推到 `main` 而团队约定走 PR / code review 流程。
  - commit message 是 "update" / "fix" / "改了点东西" 这种无信息量的内容。
  - 远端 `main` 有别人的新提交，你本地没 pull，导致冲突或被迫 force push。

## Context Scan（我注意到的）

- 你说的是"刚改完代码"，但没说：是否已经 `git add` + `git commit`？是否已经跑过测试？这个仓库是否有 PR 流程约定？
- 当前会话上下文里没有具体仓库路径，我无法直接看 `git status` / `git log` / 远端配置。

## 我需要你先确认这几件事（高风险审批门）

1. **改动是否已经 commit？**
   - 如果还没：你希望我先帮你看 `git status` / `git diff`，再帮你 commit 一次，还是你自己来？
   - commit message 想用什么？或者要我根据 diff 起一个？

2. **你们团队对 `main` 分支的约定是什么？**
   - (a) 可以直接 push 到 `main`（个人项目 / 小团队约定）
   - (b) 必须走 PR：那我应该 push 到一个新分支，然后开 PR，而不是直接推 `main`
   - 如果你不确定，**默认走 PR 是更安全的选择**。

3. **远端 `main` 是否需要先 pull / rebase？**
   - 如果其他人可能已经推过新提交，直接 push 会失败或产生 merge commit。我会先 `git fetch` + 检查是否需要 rebase。

4. **是否要跑测试 / lint / 构建再推？**
   - 如果项目有 CI，可以让 CI 跑；如果没有，我建议本地先验证一遍。

## 我建议的执行路径（等你确认后再动）

**安全路径（推荐，走 PR）:**
```
1. git status / git diff           # 先看清楚改了什么
2. （如未 commit）git add -p + git commit -m "<具体信息>"
3. git fetch origin
4. git checkout -b <feature-branch>（如果当前在 main）
5. git push -u origin <feature-branch>
6. gh pr create                    # 走 review 流程
```

**直推路径（仅在你明确说"这个项目可以直推 main"时）:**
```
1. git status / git diff
2. （如未 commit）git add -p + git commit -m "<具体信息>"
3. git fetch origin
4. git pull --rebase origin main   # 避免不必要的 merge commit
5. （本地验证：测试 / 构建）
6. git push origin main            # 不加 --force
```

## 我不会做的事

- 不会用 `--force` / `--force-with-lease`，除非你明确要求。
- 不会跳过 hooks（`--no-verify`）。
- 不会 `git add .` / `git add -A` 一把梭，避免误提交敏感文件。
- 不会在你确认前真的执行 `git push`。

---

**请回我**：
- 当前在哪个仓库？（贴个路径就行）
- 走 PR 还是直推 `main`？
- 改动 commit 了没？

我看到回复后就继续推进。
