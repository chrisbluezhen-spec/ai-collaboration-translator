# 把所有 console.log 改成 logger.info

我会处理项目里的 `console.log` 调用，改成 `logger.info`。下面是我打算做的修改：

## 要修改的文件

### 1. `src/api.js`
- 把 `console.log('api ready')` 改成 `logger.info('api ready')`
- 注释里的 `// console.log here for debug` **保持不动**（只是注释，不是实际调用）

### 2. `src/utils.js`
- 把 `console.log(data)` 改成 `logger.info(data)`

### 3. `tests/api.test.js`
- 把 `console.log('test output')` 改成 `logger.info('test output')`

### 4. `docs/README.md`
- **不修改**。这里的 "console.log" 是文档说明文字，不是代码调用。

## 具体 diff

```diff
# src/api.js
- console.log('api ready')
+ logger.info('api ready')
  // console.log here for debug   ← 保留
```

```diff
# src/utils.js
- console.log(data)
+ logger.info(data)
```

```diff
# tests/api.test.js
- console.log('test output')
+ logger.info('test output')
```

## 几个需要你确认的点

1. **`logger` 从哪里来？** 这几个文件目前看起来没有 import `logger`。我需要在每个改动的文件顶部加上 import 语句吗？比如：
   ```js
   import { logger } from './logger'    // 或者你项目里实际的路径
   ```
   如果你已经有全局 logger（例如挂在 global 上），就不用加。请告诉我你项目用的是哪种方式。

2. **测试文件要不要一起改？** 我默认也改了 `tests/api.test.js`，但有些团队倾向于测试里继续用 `console.log`（方便调试输出直接进 stdout）。如果你想跳过测试文件，告诉我一声。

3. **注释和文档我都没动**，因为它们不是真实的调用。如果你希望连注释和 README 里的字样也一起替换，我再处理。

需要我按上面的方案执行吗？还是先按你的反馈调整一下范围？
