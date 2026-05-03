下面是可复制给 Cursor 的 Prompt：

---

**任务：为 React 组件 `Header.tsx` 添加深色模式（Dark Mode）支持**

## 目标
在不破坏现有功能和视觉效果的前提下，为当前项目中的 `Header.tsx` 组件添加深色模式支持，使其能够在浅色 / 深色主题之间正确切换。

## 上下文 / 你需要先做的事
1. 在工作区中定位 `Header.tsx`（如果存在多个，列出来让我确认；如只有一个直接处理）。
2. 阅读该文件，识别：
   - 现有的样式方案（Tailwind / CSS Modules / styled-components / 普通 CSS / inline style 等）。
   - 当前所有显式颜色（背景色、文字、边框、阴影、icon、hover/active 状态）。
   - 是否已有主题上下文（如 `ThemeContext`、`next-themes`、`useColorScheme` 等）。
3. 在仓库内简单搜索一下项目是否已经存在主题切换机制（关键词参考：`dark`, `theme`, `ThemeProvider`, `next-themes`, `data-theme`, `prefers-color-scheme`）。
   - 如果**已存在**主题机制：沿用项目现有方案，不要引入新的依赖或新的切换逻辑。
   - 如果**不存在**：仅在 `Header.tsx` 内部使用 `prefers-color-scheme` 或 Tailwind 的 `dark:` 变体（取决于项目当前样式方案），不要全局新增 Provider，把改动控制在最小范围；并在最后给出"如何在全局添加完整主题切换"的简短建议。

## 范围（Scope）
- 只修改 `Header.tsx` 以及它直接依赖的、与 Header 视觉强相关的样式文件。
- **不要**重写组件结构、不要修改 props API、不要顺手重构无关代码。
- 不要新增依赖；如确有必要，先停下来问我。

## 实现要求
1. 深色模式下：
   - 背景、文字、边框、分隔线、图标、hover/active/focus 状态都要有合理的深色配色，保证对比度（WCAG AA 起步）。
   - 任何写死的浅色（如 `#fff`, `bg-white`, `text-black` 等）都要替换为可随主题变化的写法。
2. 保持现有的浅色模式视觉效果**不退化**。
3. 切换主题时不应出现颜色闪烁（FOUC）级别的明显问题；如项目已有的方案足够则沿用即可。
4. 类型保持严格，不要引入 `any`。

## 完成标准（Acceptance Criteria）
- `Header.tsx` 在浅色模式下与改动前视觉一致或更好。
- 切到深色模式时，Header 整体可读、协调，没有遗漏的"亮瞎眼"区域。
- 没有破坏现有 props、事件、可访问性属性。
- TypeScript 编译通过，无新增 lint 错误。

## 输出
1. 修改后的完整 `Header.tsx`（以及必要的样式文件 diff）。
2. 一段简短说明：你采用了哪种深色模式方案、为什么、以及如果项目尚未接入全局主题，我接下来需要做什么才能真正切换主题。

## 不要做的事
- 不要修改与 Header 无关的组件或全局配置。
- 不要新增 npm 依赖（除非先征求我的同意）。
- 不要假设我用的是某个具体框架，请先看代码再下手。
