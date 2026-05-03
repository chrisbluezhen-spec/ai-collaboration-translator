下面是可复制给 Cursor 的 Prompt：

---

你是这个 React + TypeScript 项目里的协作开发者。请为 `Header.tsx` 这个组件加上深色模式（Dark Mode）支持。

## 目标
让 `Header.tsx` 在浅色和深色两种主题下都有良好的视觉表现，并能跟随项目当前的主题切换机制自动响应主题变化。

## 上下文发现（在动手前先做）
1. 在仓库内定位 `Header.tsx` 的实际路径，读完整文件，列出它当前用到的所有颜色、背景、边框、阴影、图标颜色等视觉相关样式。
2. 判断项目当前使用的样式方案，并按以下优先级匹配并复用，**不要新引入一套机制**：
   - Tailwind CSS（检查是否已配置 `darkMode: 'class'` 或 `'media'`，以及是否使用 `next-themes` / `useTheme` 等）
   - CSS Modules / 原生 CSS（检查是否已有 `:root` / `[data-theme="dark"]` / `.dark` 等 CSS 变量约定）
   - styled-components / emotion（检查是否已有 `ThemeProvider` 与 `theme.colors.*` 约定）
   - Material UI / Ant Design / Chakra 等组件库（检查是否已有 `ThemeProvider` 或 `ConfigProvider`）
3. 确认项目里是否已经存在主题切换的状态来源（context、store、`next-themes`、`prefers-color-scheme` 等）。如果存在，**直接接入**，不要自己再造一个。

如果以上信息能从仓库读出来，就直接照做；如果发现项目里**根本没有任何深色模式基础设施**，先停下来在回答里告诉我，并给出两到三个最贴合本项目的接入方案让我选，再继续动手。

## 范围
- 只修改 `Header.tsx` 以及它直接依赖的样式文件（例如它自己的 `Header.module.css` / `Header.styles.ts` 等）。
- 如果发现项目缺少深色色值定义、且必须新增极少量 token 才能让 Header 工作，可以新增，但要集中在已有的主题/变量文件里，并在回答里明确说明新增了什么。
- **不要**顺手改其他组件、不要重构 Header 内部逻辑、不要改动路由/状态管理/构建配置。
- **不要**自己新建主题切换按钮或全局主题 Provider，除非我明确要求。

## 实现要求
- 深色模式下的对比度需满足 WCAG AA（正文文字与背景对比度 ≥ 4.5:1，大字号/图标 ≥ 3:1）。
- 颜色不要硬编码。统一走项目已有的主题机制（Tailwind dark: 前缀 / CSS 变量 / theme tokens / 组件库 token）。
- 主题切换时不应有视觉闪烁；如果项目用 SSR/Next.js，要避免主题 hydration 不一致。
- 保留 Header 现有的所有功能、布局、可访问性属性（aria-*、role、键盘焦点样式），**只改视觉层**。
- 焦点态（focus-visible）、hover 态、disabled 态在深色模式下也要看得清。

## 验收标准（你自己要能验证）
1. `Header.tsx` 在浅色模式下视觉与改动前一致或基本一致（无意外回归）。
2. 切换到深色模式后，背景、文字、图标、边框、阴影、hover/focus/active 态全部有合理的深色版本，没有任何"白底黑字浮在黑色页面上"的破图情况。
3. 主题切换是响应式的，不需要刷新页面。
4. TypeScript 类型检查通过，项目原有的 lint 规则通过。
5. 改动是最小集，diff 易读。

## 不要做的事（避免"技术上做完了但方向错了"）
- 不要把颜色硬编码成 `#fff` / `#000` / `bg-white` 这种没有 dark 变体的写法。
- 不要为了加深色模式重写整个 Header 的结构或类名体系。
- 不要新增依赖（`next-themes` 等）除非项目里已经在用，或我明确同意。
- 不要顺带"优化"无关代码。

## 输出
1. 先用 3-6 行说明你在仓库里发现的主题方案，以及你打算怎么接入。
2. 给出 `Header.tsx` 及相关样式文件的完整修改 diff。
3. 最后列出：改了哪些文件、是否新增了 token / 变量、有没有遗留风险或我需要二次确认的点。
