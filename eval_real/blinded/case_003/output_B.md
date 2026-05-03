我会先把你的需求编译成一个执行 Brief，然后直接按这个 Brief 在当前环境执行。这个任务涉及跨文件批量替换，我会按 Search-Before-Edit 规则处理，并明确把注释、文档散文和测试输出隔离在范围之外。如果你对范围判定有不同意见，请在我执行前打断我。

## Compiled Task Brief

**Objective**
把项目源码中所有"实际生效的 `console.log(...)` 调用语句"替换为 `logger.info(...)`，让生产代码统一走 logger，而不是把字符串 "console.log" 在仓库里全局替换。

**Context（来自 Context Scan）**
- `src/api.js`：包含 `console.log('api ready')`（生效调用）和 `// console.log here for debug`（注释，未执行）
- `src/utils.js`：包含 `console.log(data)`（生效调用）
- `tests/api.test.js`：包含 `console.log('test output')`（测试 setup 中的生效调用）
- `docs/README.md`：包含 `use console.log to debug`（文档散文，描述用法，不是代码）
- 仓库里没有提到现成的 `logger` 模块来源，需要在替换时一并处理 import。

**Inputs / Discovery Plan**
1. 先用 `rg -n "console\.log"` 全仓库扫描，列出所有命中位置和所在行的上下文。
2. 对每个命中位置分类：① 源码中的真实调用 ② 注释 ③ 文档散文 ④ 测试代码。
3. 确认项目中 `logger` 的来源（搜 `from .*logger`、`require\(.*logger`、`logger\.`），如果不存在则在 brief 的 Risk 部分标记需要新建/约定。

**Scope**
- 在范围内：`src/api.js`、`src/utils.js` 中的真实 `console.log(...)` 调用 → 替换为 `logger.info(...)`，并在文件顶部确保有 `logger` 的 import（沿用项目既有 logger，若无则停下询问）。
- 显式不在范围：
  - `src/api.js` 中的注释 `// console.log here for debug`（不动，注释里的字符串不是调用）
  - `docs/README.md` 中的散文 `use console.log to debug`（文档讲解概念，改了会让文档失真）
  - `tests/api.test.js` 中的 `console.log('test output')`（测试输出属于调试断言习惯，统一走 logger 可能会影响测试日志捕获，先不改，单独询问）

**Execution Steps**
1. `rg -n "console\.log" .` 列出全部命中。
2. 确认 `logger` 模块路径（若项目无 logger，停下询问，不擅自新建）。
3. 编辑 `src/api.js`：把第 N 行 `console.log('api ready')` → `logger.info('api ready')`；保留注释行原样；如缺 import 则补 `import { logger } from '...'` 或等价 require。
4. 编辑 `src/utils.js`：把 `console.log(data)` → `logger.info(data)`；同样确认 import。
5. 不动 `tests/api.test.js` 和 `docs/README.md`。
6. 替换完成后再次 `rg -n "console\.log" src/` 验证 src 下无残留生效调用。

**Constraints**
- 只改"实际调用"，不改注释和文档字符串。
- 单次最小化改动，不顺手重排 import、不格式化无关代码。
- 不引入新的 logger 实现，沿用项目既有；若没有，停下询问。

**Human Approval Gates**
- 如果项目里不存在 `logger` 模块，停下询问用户："要我用哪个 logger？沿用某个第三方包，还是新建一个 wrapper？"
- 测试文件中的 `console.log('test output')` 是否一并替换：默认不动，等用户决定。

**Acceptance Criteria**
- `rg -n "console\.log\(" src/` 返回 0 行。
- `src/api.js` 第二处的注释 `// console.log here for debug` 仍在原处、未被改动。
- `docs/README.md` 中的 `use console.log to debug` 文本未被改动。
- `tests/api.test.js` 中的 `console.log('test output')` 未被改动（除非用户另有指示）。
- 改动后的 `src/*.js` 在静态层面引用得到的 `logger` 是已 import 的标识符，不是未定义变量。

**What Not To Do（"技术上做完了但其实做错"清单）**
- 不要做全局字符串替换 `s/console\.log/logger.info/g`，这会污染注释和 README。
- 不要顺手把 README 里讲解 `console.log` 用法的句子改写。
- 不要悄悄把 test 里的 `console.log` 也改了——测试日志习惯属于另一类决策。
- 不要在没有确认 logger 来源的情况下编造一个 import 路径。

**Reporting Format**
执行完成后报告：
- 改了哪些文件、哪些行
- 哪些命中点被有意保留及原因
- `rg` 验证结果
- 待确认事项（logger 来源 / 测试文件是否处理）

---

## Execution

按上面的 Brief，我现在会执行的动作（在真实环境中将逐步落地）：

1. 运行 `rg -n "console\.log" .`，确认命中位置与上面 Context 一致。
2. 运行 `rg -n "logger" src/` 找 logger 来源；如果项目没有 logger，**这里停下来问你**：
   > 项目里我没有找到现成的 `logger` 模块。你希望我：
   > A. 沿用某个已有包（请告诉我包名/路径）
   > B. 新建一个 `src/logger.js` 简单 wrapper（默认转发到 console）
   > C. 暂停，等你先把 logger 接好再让我替换
3. 假设 logger 路径已确认为 `./logger`，进行最小化替换：
   - `src/api.js`：第 X 行 `console.log('api ready')` → `logger.info('api ready')`；顶部按需补 `import { logger } from './logger'`。注释行不动。
   - `src/utils.js`：`console.log(data)` → `logger.info(data)`；顶部按需补 import。
4. `tests/api.test.js` 和 `docs/README.md` 不改。
5. `rg -n "console\.log\(" src/` 复核应为 0 行；`rg -n "console\.log" .` 应只剩注释 + README 散文 + 测试文件三处。
6. 最终报告：
   - Changed: `src/api.js`, `src/utils.js`
   - Intentionally unchanged: `src/api.js` 的注释行、`docs/README.md` 的散文、`tests/api.test.js` 的测试日志
   - Open question: 测试文件里的 `console.log('test output')` 是否也要统一为 `logger.info`？
