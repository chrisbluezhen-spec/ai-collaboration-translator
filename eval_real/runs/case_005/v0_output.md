# Cursor Prompt: 为 Header.tsx 添加深色模式支持

请为我的 React 组件 `Header.tsx` 添加深色模式（Dark Mode）支持。具体要求如下：

## 任务目标
在保持现有功能和布局不变的前提下，让 `Header.tsx` 能够根据当前主题（light / dark）自动切换样式。

## 实现要求

1. **主题切换机制**
   - 使用 Tailwind CSS 的 `dark:` 前缀实现深色模式（假设项目已启用 `darkMode: 'class'`）。
   - 如果项目未使用 Tailwind，请改用 CSS Variables 或 styled-components 主题方案，并在回答前先询问我使用的是哪种样式方案。

2. **样式适配**
   - 背景色：浅色模式使用白色或浅灰，深色模式使用深灰/黑色（如 `bg-white dark:bg-gray-900`）。
   - 文字颜色：浅色模式使用深色文字，深色模式使用浅色文字（如 `text-gray-900 dark:text-gray-100`）。
   - 边框、分隔线、hover 状态、图标颜色都要相应调整。
   - Logo、按钮、链接等子元素也要确保在深色模式下清晰可见。

3. **主题切换按钮（可选但推荐）**
   - 在 Header 右侧添加一个主题切换按钮（图标用太阳 / 月亮）。
   - 使用 `useState` + `useEffect` 管理主题状态，并把 `dark` 类加到 `<html>` 元素上。
   - 把用户偏好保存到 `localStorage`，下次打开时自动恢复。
   - 默认跟随系统主题（`prefers-color-scheme`）。

4. **代码质量**
   - 保留原有 TypeScript 类型定义。
   - 不要破坏已有的 props 接口和组件结构。
   - 添加必要的注释说明深色模式相关的改动。

## 输出格式
- 请直接给出修改后的完整 `Header.tsx` 代码。
- 在代码后用简短的 bullet points 说明你做了哪些改动、为什么这么改。
- 如果需要修改其他配置文件（如 `tailwind.config.js`），也一并列出。

## 我的当前代码
```tsx
// 在这里粘贴你的 Header.tsx 内容
```

请基于上述代码进行修改。如果有任何不清楚的地方，先提问再动手。
