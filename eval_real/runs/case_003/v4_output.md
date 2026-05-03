我会先把你的需求编译成一个执行 Brief，然后直接按这个 Brief 在当前环境推进。遇到关键决策或不可逆动作时，我会先停下来问你。

## Compiled Task Brief

**Objective**: 把项目中真实的 `console.log(...)` 日志调用统一改成 `logger.info(...)`，使运行时日志走 logger；同时不破坏注释里、文档散文里作为"概念名词"出现的 "console.log" 文本。

**Context (来自你给的项目结构)**:
- `src/api.js`：一处真实调用 `console.log('api ready')`，外加一行注释 `// console.log here for debug`
- `src/utils.js`：一处真实调用 `console.log(data)`
- `tests/api.test.js`：测试 setup 里一处 `console.log('test output')`
- `docs/README.md`：散文中出现 "use console.log to debug" 字样（在介绍 `console.log` 这个 API）

**Scope**:
- 改：`src/api.js`、`src/utils.js`、`tests/api.test.js` 中**作为代码语句执行的** `console.log(...)`。
- 不改：`src/api.js` 中那条 `// console.log here for debug` 注释；`docs/README.md` 全部内容。

**Execution Plan (遵循 Search-Before-Edit)**:
1. 全仓搜：`rg -n 'console\.log' src tests docs`，确认现在有几处真实代码调用、几处是注释或文档。
2. 在被修改的源文件里确保 `logger` 已经被引入（按项目模块系统选 `require('./logger')` 或 `import logger from './logger'`）。
3. 把 3 处真实调用替换成 `logger.info(...)`，参数原样保留。
4. 改完再搜一次 `console.log`，确认剩下的命中只剩 `src/api.js` 那行注释 + `docs/README.md` 散文。

**Constraints**:
- 严格按"代码中的实际调用"来替换，注释和文档保留原文。
- 不顺手做无关重构（不动变量命名、其它日志风格、依赖版本）。
- 不在没有 logger 模块的情况下凭空 `require('logger')`。

**Acceptance Criteria**:
- `rg 'console\.log\(' src tests` → 0 条命中。
- `src/api.js` 中 `// console.log here for debug` 注释仍在原处、原样。
- `docs/README.md` 字节完全不变。
- 3 个被改的文件都能解析到 `logger` 引用，不会因为漏 import 而运行时崩。

**What not to do (避免"看起来做完了但其实做错了"的几个坑)**:
- 不要把 `// console.log here for debug` 也替换掉——它是注释，不是日志调用。
- 不要把 `docs/README.md` 里 "use console.log to debug" 改成 "use logger.info to debug"——那段是文档在解释 `console.log` 这个 API，不是项目自己在打日志。
- 不要把测试断言或 mock 里其它带 "console" 的代码也一起动了——只替换字面上的 `console.log(...)` 调用本身。

**Human approval gate**: 如果仓库里还没有 `logger` 模块，我会停下来问你 logger 的引入路径，再继续替换。

## Execution

下面是我打算落到这三个文件的具体改动（`docs/README.md` 不动）：

### src/api.js

```diff
- console.log('api ready')
+ logger.info('api ready')
  // console.log here for debug
```

文件顶部按项目模块约定补：

```js
// CommonJS
const logger = require('./logger')
// 或 ESM
// import logger from './logger'
```

注释那一行保持不变。

### src/utils.js

```diff
- console.log(data)
+ logger.info(data)
```

同样在文件顶部确保 `logger` 已被引入。

### tests/api.test.js

```diff
- console.log('test output')
+ logger.info('test output')
```

测试文件 setup 也要拿到 `logger`，按项目里测试现有的 import/require 写法补上即可。

### docs/README.md

不动。"use console.log to debug" 是在描述 `console.log` 这个 API，不是项目自身的日志调用。

## 验证

改完会执行：

```bash
rg 'console\.log\(' src tests   # 期望: 0 条
rg 'console\.log'   src tests   # 期望: 仅剩 src/api.js 的注释那一行
rg 'console\.log'   docs        # 期望: README 那一处仍在
```

## 在动手之前，需要你确认 2 件事

1. 项目里 `logger` 模块**是否已经存在**？引入路径是什么（比如 `./logger`、`./utils/logger`、还是某个第三方包）？如果暂时还没有，你希望我顺手建一个最简的 `logger.js`（先直接代理到 `console`），还是先停下来等你提供？
2. `tests/api.test.js` 里那条 `console.log('test output')` 你确认也要一起替换吗？有些团队会刻意让测试输出仍走 `console`，避免被 logger 的 transport / level 影响。

这两点确认完，我就直接把上面的改动落到文件里，然后跑一遍验证命令并把结果回报给你。
