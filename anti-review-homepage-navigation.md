# ShiClass 主页与导航视角 · 对抗式审查报告

**审查日期：** 2026-07-12  
**审查范围：** index.html + 30 节课程 HTML 文件  
**审查工具：** 静态代码审查 + 本地 HTTP 服务性能测试

---

## 1️⃣ 主页结构 · 课程卡片入口

**结论：✅ 每节课都有独立卡片入口**

- `index.html` 主页采用 JS 动态渲染：加载 `data/course-catalog.js` 数据，按 `collection` 分组，在 `lesson-grid` 中以卡片形式展示每一节课。
- 每个卡片包含：**标题、副标题、时长、标签**，卡片本身是 `<a>` 链接直接指向课程 HTML。
- 目录空课程自动跳过（`lessons.length === 0` continue），无空白占位。
- 30 节课全部在 `course-catalog.js` 中注册，与实际 30 个 HTML 文件一一对应，**无遗漏**。

**建议优化：**
- 卡片缺少「课程编号 / 封面缩略图」等视觉差异化元素，30 个卡片排布后辨识度不足。
- 卡片不支持「学习进度」标记（已完成 / 进行中 / 未开始）。

---

## 2️⃣ 导航系统

### 2.1 主页 → 课程的入口

- `index.html` 中每个卡片 href 为 `lessons/XXXX-xxx.html` ✅ 路径正确
- 每个课程页面底部都有 `../index.html`（返回课程馆）链接 ✅

### 2.2 课程页面的导航（前后课 + 返回课程馆）

存在 **明显的导航不一致问题**，页面分为两个世代：

#### 世代 A：简化版导航（仅返回课程馆）
| 文件 | 导航 |
|---|---|
| 0000-图像算法安防应用.html | ← 返回课程馆（仅 1 个链接） |
| 0001-研究共同体方向地图.html | ← 返回课程馆（仅 1 个链接） |
| 0002-学术规范职业习惯.html | ← 返回课程馆（仅 1 个链接） |
| 0003-演讲技巧学术表达.html | ← 返回课程馆（仅 1 个链接） |
| 0004-KF-L1-矩阵特征值.html | ← 返回课程馆（仅 1 个链接） |
| 0005-KF-L2-矩阵求逆状态空间.html | ← 返回课程馆（仅 1 个链接） |

**这 6 节课没有任何「上一讲 / 下一讲」链接**，无法在课程间顺序浏览。

#### 世代 B：完整导航（上一讲 + 下一讲 + 返回课程馆）
- **0006 至 0028**：共 24 节课有完整的三个链接
- 0006 的「上一讲」链接标注 `class="disabled"`（是 KF 系列第一讲，不可点击）
- 0012 至 0028：正确使用 `class="prev"` / `class="next"` 样式

### 2.3 ⚠️ 发现的问题

#### 🚨 严重：断裂的导航链接
**0011-KF-L9-最小二乘几何.html** 中「下一讲」链接指向：

```
0012-KF-L10-投影定理随机最小二乘.html
```

但实际文件名为 `0012-KF-L10-投影定理.html`（少了「随机最小二乘」），**点击会 404**。

#### ⚠️ 中等：0028 导航重复
**0028-KF-L18-Bellman方程.html** 的 nav-links 中同时包含：

```html
<a href="../index.html" class="next">🏠 返回课程馆</a>
<a href="../index.html" class="home-link">🏠 返回课程馆</a>
```

两个链接都指向首页，「返回课程馆」重复出现。建议把 next 改为空（末尾课程无下一讲）或移除。

#### ⚠️ 中等：0006 disabled 语义歧义
0006 的 prev 链接 href 实际指向 0005（合法文件），但加了 `class="disabled"`。CSS 的 `pointer-events: none` 使其不可点击。设计意图是「跨 collection 不可回溯」，但会误导用户以为 0005 不存在。

#### ℹ️ 低优先级：0012-0028 有 `class="home-link"` 但 CSS 中无对应样式
home-link 的样式通过 `style="text-align:center;display:block;margin-top:8px"` 内联实现，CSS 文件中未定义 `.home-link`。

---

## 3️⃣ HTML 结构性缺陷

### 3.1 Orphan `<div></div>` 在 lead-grid 前

**影响范围：18 个课程页面**（0012 至 0028）

所有带 `lead-grid` 的页面在 Hero 区到 Lead Grid 之间存在 **冗余的 `<div></div>`**，形如：

```html
<div
</div>

<div class="lead-grid">
```

这会在页面顶部产生一个空行或零高度空白块。虽然不影响功能，但不符合 W3C 规范，且可能在某些浏览器中触发布局偏移。

同时造成 `<div>` 开闭数量不匹配（多 1 个 `</div>`）。

### 3.2 Obsidian Markdown 图片引用未转换

| 文件 | 内容 |
|---|---|
| 0001-研究共同体方向地图.html | `![[Pasted image 20260515200829.png]]` |
| 0002-学术规范职业习惯.html | `![[Pasted image 20260515201413.png]]` |

这两个 `![[...]]` 是 Obsidian 的 wiki 链接语法，在浏览器中直接显示为纯文本，**图片完全不显示**。PDF 转 Markdown 后再转 HTML 时未做这步图片路径转换。

---

## 4️⃣ 页面加载性能

### 4.1 HTML 文件体积

| 文件 | 体积 | 加载时间 (localhost) |
|---|---|---|
| index.html | 6.2 KB | ~1 ms |
| 典型课程页 (小型) | ~5 KB | ~1-2 ms |
| 典型课程页 (大型, 含MathJax) | ~17 KB | ~1-2 ms |
| course-catalog.js | 17 KB | — |
| shiclass.css | 7.4 KB | — |
| shiclass.js | 0.9 KB | — |

### 4.2 外部依赖（可能影响实际加载速度）

每个课程页面都引用：

| 资源 | 类型 | 说明 |
|---|---|---|
| Google Fonts (Inter/Noto Serif SC/JetBrains Mono) | 字体 | `preconnect` + `stylesheet`，国内可能需要代理 |
| MathJax 3 (tex-svg.js) | CDN | `https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js`，约 2-3 MB |
| course-catalog.js | 本地 /data/ | 同步加载（阻塞渲染） |
| shiclass.css | 本地 /assets/ | 同步加载 |
| shiclass.js | 本地 /assets/ | 部分课程引入 |

### 4.3 性能评估

- **纯静态 HTML 加载极快**（< 2 ms 本地测试）
- **无大图片**：项目中 467 MB 的 `course-notes/` 和 115 MB `videos/` 未被 HTML 直接引用
- **瓶颈在外部 CDN**：MathJax CDN (~2MB JS) 是最大性能负担，首次加载约需 1-3 秒（取决于网络）
- **index.html 无「骨架屏 / 加载态」**：由于依赖 JS 渲染，JS 执行前页面是空的 `<main id="mainContent">`

---

## 5️⃣ 公式渲染（MathJax）

**结论：✅ 所有课程页面均已配置 MathJax**

- 30/30 的课程 HTML 文件包含 MathJax 配置块和 CDN 引用
- 配置统一：
  - 渲染器：`tex-svg.js`（SVG 输出，适用性最广）
  - 行内公式：`$...$`
  - 块级公式：`$$...$$`
  - `fontCache: 'global'`（全局字体缓存，减少重复渲染）
- `defer` 加载，不阻塞页面渲染
- index.html 无需 MathJax ✅

---

## 6️⃣ 综合评估与优先级排序

| 严重程度 | 问题 | 涉及范围 |
|---|---|---|
| 🔴 **高** | 0011 导航「下一讲」链接断裂 → 404 | 1 个文件 |
| 🟡 **中** | 6 节早期课程无前后课导航 | 6 个文件 |
| 🟡 **中** | 18 个页面 HTML 结构缺陷（多余的 `</div>`） | 18 个文件 |
| 🟡 **中** | 2 个页面 Obsidian 图片引用不渲染 | 2 个文件 |
| 🟢 **低** | 0028 导航重复（重复的"返回课程馆"） | 1 个文件 |
| 🟢 **低** | 主页卡片缺少视觉差异化 | index.html |
| 🟢 **低** | index.html 无加载骨架屏 | index.html |
| 🟢 **低** | home-link 无 CSS class（靠内联样式） | 18 个文件 |

### 建议立即修复

1. **0011 导航链接断裂** — 将 href 从 `0012-KF-L10-投影定理随机最小二乘.html` 改为 `0012-KF-L10-投影定理.html`
2. **0000-0005 缺少前后导航** — 补上 prev/next 链接（或统一模板重新生成）
3. **18 个页面的 orphan `<div></div>`** — 删除 Hero 区到 lead-grid 之间的多余 `</div>`
4. **0001/0002 的 Obsidian 图片** — 将 `![[...]]` 转为 `<img>` 标签或删除

---

*审查结束 · 3 项严重/中等问题建议优先处理*
