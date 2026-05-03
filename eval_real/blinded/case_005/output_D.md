下面是可复制给 Cursor 的 Prompt：

```
任务：给 React 组件 Header.tsx 增加深色模式（Dark Mode）支持。

Objective（目标）
让 Header.tsx 在深色模式下能正确渲染（背景、文字、图标、边框、hover/active 状态都符合深色配色），并且不破坏现有的浅色模式表现。最终效果要和当前项目里已有的深色模式视觉风格一致——不要引入一套新的主题系统。

Context（先做的上下文扫描，不要跳过）
在改动 Header.tsx 之前，先在工作区里完成下面的发现工作，并据此决定如何实现：

1. 找到 Header.tsx 的实际路径，读完整文件，列出它当前用到的所有颜色、背景、边框、阴影、icon 颜色、hover/focus 状态。
2. 判断项目现有的主题方案，按以下优先级识别（只选其中已经存在的那一套，不要新建）：
   - Tailwind CSS：检查 tailwind.config.{js,ts} 是否有 darkMode 配置（'class' 或 'media'），以及项目里其他组件是否已经使用 `dark:` 前缀。
   - CSS variables / design tokens：检查 globals.css / theme.css / :root 与 [data-theme="dark"] 等定义。
   - next-themes / ThemeProvider / Context：检查是否已存在 ThemeProvider、useTheme、ThemeContext。
   - styled-components / emotion theme：检查 ThemeProvider 与 theme 对象。
3. 至少找两个已经支持深色模式的现有组件作为参考，沿用它们的写法和命名风格。
4. 确认深色模式的触发方式（class="dark"、data-theme、prefers-color-scheme），不要换一种新的触发方式。

Scope（范围）
- 只修改 Header.tsx，以及为支持它必需的最小改动（例如在已有 theme token 文件里补一个缺失的颜色变量）。
- 不在本次任务里改其它组件、不重构 Header 现有逻辑、不调整布局/排版/字号。
- 不引入新的依赖（除非项目里已经在用，比如 next-themes 已装），引入前先停下来询问。

Constraints（约束）
- 不要新建另一个主题系统。复用项目现有那一套。
- 不要硬编码颜色值（#fff、#000、rgb(...)）。使用项目已有的 token / CSS 变量 / Tailwind 颜色名。
- 浅色模式现有外观必须保持像素级一致，不允许"顺手优化"。
- 保持组件 API（props）不变，不破坏调用方。
- TypeScript 类型保持严格，不引入 any。
- 可访问性：深色模式下文字与背景对比度需 ≥ WCAG AA（正文 4.5:1，大字 3:1），focus ring 在深色背景下必须可见。

Acceptance Criteria（可观察的验收标准）
1. 在 dark 模式下打开页面，Header 的背景、文字、icon、边框、分隔线全部符合深色配色，没有"漏改"的浅色残留。
2. 切回浅色模式，Header 与改动前完全一致（diff 仅限于新增的 dark 样式，不修改原有浅色样式的语义）。
3. hover、focus、active、disabled 等所有交互状态在深色模式下都有对应样式，且 focus ring 可见。
4. 没有新增颜色硬编码；所有颜色都来自项目现有 token / 变量 / Tailwind palette。
5. `tsc --noEmit`（或项目对应的类型检查命令）通过，lint 通过。
6. 浏览器控制台没有新增 warning / error。

What not to do（最常见的"做完了但不对"）
- 不要绕过项目主题系统、直接写 `style={{ background: '#111' }}` 或 `className="bg-black"` 这种硬编码。
- 不要顺手把 Header 的结构、props、文案、图标一起改了。
- 不要"顺便"给其它组件加深色模式支持，那是另一个任务。
- 不要因为找不到现成 token 就自己造一个新命名空间，先按现有命名补一个同风格的变量；如果连命名风格都不确定，停下来问我。
- 不要在没有看过其它组件实现的情况下凭直觉写 `dark:` 类名——先确认项目已经在用 Tailwind dark mode 再用。

Execution（怎么做）
1. 先做上面的 Context 扫描，把发现写成 3-5 行总结贴出来（用的是哪套主题方案、触发方式是什么、参考了哪个组件）。
2. 给出最小改动方案（要改哪几行、加哪些 dark 样式 / token），等我确认后再动手；如果方案非常直接（纯加 `dark:` 类名，零新增 token），可以直接改并展示 diff。
3. 改完后自检 Acceptance Criteria 1-6，逐条说明是否满足。
4. 报告：改了哪些文件（应当只有 Header.tsx，最多再加一个 token 文件）、新增了哪些 className / token、剩余风险或建议跟进项。

如果在上下文扫描阶段发现项目里完全没有任何深色模式基础设施（没有 darkMode 配置、没有 ThemeProvider、没有 data-theme 切换），请停下来先告诉我，让我决定是先搭基础设施还是只在 Header 里临时用 prefers-color-scheme，不要自己擅自决定。
```
