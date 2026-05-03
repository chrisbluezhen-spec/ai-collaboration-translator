下面是可复制给 Cursor 的 Prompt：

```
# 任务：为 Header.tsx 添加深色模式支持

## Objective
为现有的 React 组件 `Header.tsx` 增加深色模式（Dark Mode）支持，使其能够根据当前主题（light / dark）自动切换样式，并保持原有的功能、布局、交互行为完全不变。

## Context
- 目标文件：`Header.tsx`（请先打开并读取该文件，理解当前的样式实现方式）
- 在动手前先识别项目当前的主题方案，按以下优先级判断：
  1. 如果项目使用 Tailwind CSS：使用 `dark:` 前缀类名（基于 `class` 策略）。
  2. 如果项目使用 CSS Modules / styled-components / emotion：使用 CSS 变量 + `[data-theme="dark"]` 或 `prefers-color-scheme` 切换。
  3. 如果项目已有 ThemeProvider / ThemeContext：复用现有 context，不要新建。
  4. 如果以上都没有：默认使用 `prefers-color-scheme: dark` 媒体查询 + CSS 变量方案，并在文件顶部注释说明该假设。
- 不要引入新的 UI 库或主题库（如 next-themes、MUI 等），除非项目已经在使用。

## Inputs / Discovery
- 读取 `Header.tsx` 全文。
- 检查同目录及项目根的：`tailwind.config.*`、`package.json`（dependencies）、`globals.css` / `index.css` / `App.css`、是否存在 `ThemeContext` / `ThemeProvider`。
- 根据发现结果决定走哪条主题方案路径，并在最终回复中说明你选择了哪种方案以及为什么。

## Scope
- 仅修改 `Header.tsx` 一个文件，以及为深色模式必要的最小样式改动（例如同文件相邻的 CSS Module 或 Header 自己的样式文件）。
- 不要重构组件结构、不要改 props API、不要改 DOM 结构、不要重命名。
- 不要触碰 Header 之外的其他组件、路由、全局布局。
- 不要新增主题切换按钮（除非用户明确在 Header 里要求过）。

## Constraints
- 保持原有的浅色（light）外观与当前一致，深色模式只是新增分支，不能让浅色看起来不一样。
- 颜色对比度需满足 WCAG AA（正文文字对背景对比度 ≥ 4.5:1）。
- 不要使用内联硬编码的十六进制颜色去做条件判断（避免 `isDark ? '#fff' : '#000'` 这种散落写法），优先用 CSS 变量或 Tailwind dark: 类。
- TypeScript 严格模式下不能产生新的类型错误。

## Acceptance Criteria（可观察）
1. 在 `<html>` 上添加 `class="dark"` 或 `data-theme="dark"`（取决于所选方案）后，Header 的背景、文字、图标、边框、hover 状态都呈现为深色风格，且无残留的浅色硬编码颜色。
2. 移除该深色标识后，Header 外观与改动前完全一致（视觉回归）。
3. `Header.tsx` 不报 TS 错误，不产生新的 ESLint 错误。
4. Header 的所有原有功能（点击、链接跳转、菜单展开、响应式断点）行为不变。

## What NOT to do（避免"技术上完成但错了"）
- 不要把浅色样式整体替换成深色——必须是"两套都在，按主题切换"。
- 不要新建主题 context / provider / hook，除非项目已有同类设施需要复用。
- 不要修改 `Header.tsx` 之外不相关的文件。
- 不要顺手"优化"或"重构" Header 的其他部分。
- 不要引入新依赖。

## Reporting Format
完成后请回复：
1. 你识别出的项目主题方案（Tailwind dark: / CSS 变量 / 现有 ThemeContext / 默认假设）以及判断依据（看到了哪些文件 / 配置）。
2. 修改了哪些文件、每个文件的关键 diff 摘要。
3. 如何手动验证深色模式效果（例如：在 devtools 里给 `<html>` 加 `class="dark"` 应该看到什么变化）。
4. 还有哪些遗留风险或需要我确认的点。
```
