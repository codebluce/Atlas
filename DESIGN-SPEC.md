# 信贷风控学习手册 · 设计规格说明书（Design Spec）

> **版本**：v1.0 · 2026-09-21
> **来源**：基于当前仓库实际代码反向拆解（`index.html` + 模块①②③④共5个页面 + `style.css`，合计 3509 行）
> **用途**：续写模块⑤⑥⑦、修改既有页面、新增任何页面/组件时的唯一设计基准。
> **维护约定**：发现代码与本文档不一致时，以代码实际行为为准，并回来更新本文档。

---

## 0. 一句话概括

一本**纯静态、无构建**的多页 HTML 学习手册：以"业务生命周期 × 方法论层次"双主线组织 7 个模块，每页遵循固定的"痛点→概念→手算→案例→坑→速查表→自测"教学骨架，共享一套**暖色笔记本风格**的设计系统（米白底 + 赭橙主色 + 衬线标题），所有示例数字跨模块构成一条可复算的隐藏叙事线。

---

## 1. 产品定位与设计哲学

### 1.1 定位

| 维度 | 设定 |
|---|---|
| 性质 | 个人学习手册 · 持续更新（非机构内部资料，非深度分析报告） |
| 受众 | 作者本人（入门→进阶的信贷风控学习者），单机本地浏览 |
| 起点 | 一篇公众号科普文（《信贷风控的"透视镜"：一文看懂 Vintage 分析》，任知微，风控拾光） |
| 目标 | "每个概念都配得上一个能讲清楚的例子"，不追求面面俱到 |

### 1.2 三条设计原则（贯穿全部页面）

1. **痛点先行**：每个模块第一 Part 永远是"先说痛点"——先讲清"朴素做法为什么会骗人"，再引出方法论。
2. **凡概念必有例子，凡例子必可复算**：所有示例数字（10000 人样本、KS=0.46、IV=0.563 等）都是手算可验证的，且跨模块共享同一条叙事线（见 §7.3）。
3. **教学层与真实层分离**：教学示例（Chart.js + 假数据，强制标注"非真实业务数据"）与真实数据案例（脱敏后的静态池数据 + matplotlib 出图）分层呈现，真实层明确说明"真实世界比教程例子复杂在哪"。

### 1.3 非目标（明确不做的）

- ❌ 不做仪表盘风格（与 DailyDigest 项目刻意区分）
- ❌ 不做 JS 交互逻辑（图表之外的交互全部用原生 `details/summary`）
- ❌ 不用构建工具/框架（纯 HTML + CSS + CDN Chart.js）
- ❌ 不套用 DailyDigest 的综合记录模板（这是教程，不是分析报告）

---

## 2. 信息架构

### 2.1 知识地图：7 模块双主线

模块**编号 = 业务逻辑分组，不是学习顺序**。组织维度有两条（在 index "怎么用这本手册"中明示）：

- **业务生命周期**：贷前 → 贷中 → 贷后
- **方法论层次**：数据 → 特征 → 模型 → 策略 → 监控

| # | 文件 | 主题 | 昵称 | eyebrow emoji | 状态 |
|---|---|---|---|---|---|
| ① | `module-01-scorecard.html` | 评分卡体系（A/B/C卡） | 骨架 | 🏗️ | ✅ 已完成 |
| ② | `module-02-woe.html` | 特征工程四件套（分箱/WOE/IV） | 手艺 | 🛠️ | ✅ 已完成 |
| ③ | `module-03-metrics.html` | 模型评估指标（KS/AUC/PSI） | 标尺 | 📏 | ✅ 已完成 |
| ④ | `module-04-vintage.html`（完整版）/ `module-04-vintage-teaching.html`（纯教学版） | 资产质量分析（Vintage/迁徙率） | 透视镜 | 🔍 | ✅ 已完成 · 最早编写（index 上保留"当前在学"高亮） |
| ⑤ | `module-05-*.html` | 决策与策略（AB测试/拒绝推断） | 决策 | — | 待写 |
| ⑥ | `module-06-*.html` | 数据与合规边界 | 边界 | — | 待写 |
| ⑦ | `module-07-*.html` | 进阶外延（反欺诈/ABS/BNPL） | 外延 | — | 待写 |

**推荐学习顺序**（固定，不随完成度变化）：③评估指标 → ②特征工程 → ①评分卡 → ④资产质量 → ⑤决策策略 → ⑥合规边界 → ⑦进阶外延。

### 2.2 文件布局与命名

```
credit-risk-handbook/
├── index.html                    # 封面 + 知识地图 + 路线图（hub）
├── style.css                     # 唯一共享样式（设计系统，见 §4/§5）
├── module-0N-关键词.html          # 模块页，N 用两位数字
├── module-04-vintage-teaching.html  # 特例：模块④的"纯教学版"衍生副本
└── *.png                          # matplotlib 真实数据图（紧贴引用它的页面存放）
```

- 命名规则：`module-0N-关键词.html`，关键词用英文小写连字符。
- 真实数据图片命名：`{分析主题}-{变体}.png`，如 `vintage-curve-real.png`、`vintage-spectrum-B2.png`、`vintage-single-2025-06-annotated.png`。

### 2.3 导航模型：hub-and-spoke + 交叉引用

三层导航，无全站顶栏：

1. **index → 模块**：roadmap 卡片（仅已完成的卡片是 `<a>` 可点击）+ order-strip chip（已完成/在学的 chip 可点击）+ 页脚"已完成"链接列表。三处状态必须同步更新。
2. **模块 → index**：masthead 内 breadcrumb（`手册 › 模块N`）+ 文末 `← 返回信贷风控学习手册总目录`。
3. **模块 ↔ 模块**：正文中用 `<a href="module-0X.html">` 就地交叉引用对应小节（服务于 §7.3 的叙事线）。

模块完成时的**状态同步清单**（index.html 三处）：
- roadmap 卡片：`tag-todo` → `tag-good`，文案"推荐第N步 · 待更新" → "推荐第N步 · 已完成"，卡片加 `linked` class 变可点击，h3 标题加 `→`；
- order-strip：对应 chip 加 `done-chip` 样式 + `✓` 前缀 + 链接；
- 页脚"已完成"链接列表追加该模块。

---

## 3. 页面结构模板

### 3.1 模块页固定骨架（自上而下 13 段）

```html
<!DOCTYPE html><html lang="zh-CN">
<head>
  <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>模块N · 主题（关键词）| 信贷风控学习手册</title>
  <link rel="stylesheet" href="style.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
</head>
<body>
  <header class="masthead">…breadcrumb + eyebrow + h1 + sub…</header>   <!-- ① -->
  <nav class="local-nav">…①②③… 锚点…</nav>                              <!-- ② -->
  <div class="wrap">
    <div class="checklist">…本节读完，你能做到…</div>                      <!-- ③ -->
    <div class="part" id="pN">…正文 Part1..N…</div>                       <!-- ④ -->
    <div class="summary-box">…小结 + mnemonic-line…</div>                  <!-- ⑤ -->
    <div class="next-card">…下一步…</div>                                  <!-- ⑥ -->
    <p style="text-align:center"><a href="index.html">← 返回总目录</a></p> <!-- ⑦ -->
    <div class="page-footer">…左：手册·模块N ｜ 右：数据来源声明…</div>      <!-- ⑧ -->
  </div>
  <script>…Chart.defaults 统一配置 + 各图实例…</script>                    <!-- ⑨ -->
</body></html>
```

### 3.2 masthead 规范

- **breadcrumb**：`手册名 › 模块N`（链接回 index）。
- **eyebrow**：`emoji + 空格 + 模块N · 模块名`（emoji 每模块固定，见 §2.1）。
- **h1**：问题式/断言式标题（"KS/AUC/PSI/Lift：怎么判断一个模型好不好、稳不稳"、"不用建模，也能看穿风险"）。
- **sub**：一段钩子文案，用具体数字抛出本模块要解决的认知冲突（如"'准确率99%'听起来很厉害，但……"）。

### 3.3 局部导航（local-nav）

- sticky 吸顶 + 毛玻璃（`backdrop-filter:blur(6px)`），横向滚动。
- 每个 Part 一个锚点链接，标签用带圈数字 `① ② ③…`，href 指向 `#pN`。
- Part 数量 9~11 个均可，超过屏宽自动横向滚动，不做二级折叠。

### 3.4 学习清单（checklist）

紧跟导航的第一块内容，标题固定为 `本节读完，你能做到`，6~9 条动词开头的可检验目标（"解释清楚…/手算一遍…/走一遍…/避开…"）。模块④多出的真实数据条目用"（进阶）"前缀标注。

### 3.5 Part 编排模式（教学骨架）

Part 是正文的一级单元，结构：`.part` 容器（`id="pN"`）→ `.part-head`（`.part-num` 零填充序号 `01`…`11` + `h2` 标题）→ `.part-lede`（一句导语）→ 内容块。

各模块 Part 数（10~11）可弹性伸缩，但**骨架顺序固定**：

| 顺序 | 环节 | 内容模式 | 备注 |
|---|---|---|---|
| 1 | **先说痛点** | `.analogy` 类比开场 + 为什么朴素做法会骗人 | 每模块必有，标题固定句式"先说痛点：…" |
| 2 | 核心概念 | `.concept-grid` 概念卡（2~4 张） | "必须先搞清楚的概念" |
| 3+ | 指标图鉴 / 机制拆解 | `.concept-grid`（每卡一个指标，含定义/公式/"看什么"） | 数量按主题定 |
| 中段 | 手算一遍 | `.method-step` + `.calc-box` + `.tbl` 数据表 | 用同一份贯通样本（§7.3） |
| 中后 | 实战案例 | `.chart-card` + `.case-step` 步骤卡（发现→排查→决策） | 案例是"连续剧"的一集 |
| 倒数第3 | 三个坑 | 3 张 `.pitfall` 卡 | **固定恰好 3 个**，标题"坑一/二/三 · …" |
| 倒数第2 | 速查表 | `.cheat-grid` 8~9 张暗色卡 | 卡内固定用 `<b>用途：</b>/<b>阈值：</b>` 前缀 |
| 最后 | 自测 | 5 张 `.quiz-item`（`details/summary` 原生折叠） | **固定 5 题**，必含 1 道计算题 + 1 道分析题 |
| 可选追加 | 真实数据案例 | 仅模块④完整版有（Part ⑩） | 教学版整段删除 |

### 3.6 收尾三件套

- **summary-box**：渐变暖色小结框，正文 1 段 + 1 条 `.mnemonic-line` 口诀（居中、上下虚线夹持的一句话记忆锚点，如"看清每一批，才能管好整盘"）。
- **next-card**：`下一步` 卡片 + 返回 index 链接。
- **page-footer**：左侧 `信贷风控学习手册 · 模块N`；右侧数据来源声明（教学页固定"示例数据均为教学演示用途，非真实业务数据"；含真实数据的页面写明来源与参考文献）。

### 3.7 教学版/完整版双版本特例（仅模块④）

`module-04-vintage.html`（完整版）与 `module-04-vintage-teaching.html`（纯教学版）的差异**仅 4 处**：local-nav 的 `⑩ 真实案例` 链接、checklist 的"（进阶）"条目、整个 Part⑩、页脚来源声明。第 1–9 Part **逐字节相同**。

**维护规则**：完整版第 1–9 Part 有任何改动，必须同步教学版（或从完整版重新复制生成）。

---

## 4. 视觉设计系统

### 4.1 风格基调

"手写笔记 + 教科书边注"：暖米白纸面、赭橙手写笔主色、衬线体标题（宋体系）、低饱和语义色、细边框浅阴影卡片。视觉密度低于仪表盘，强调"可读的书页感"。CSS 注释里明示定位：*风格定位：手写笔记 + 教科书边注感，不是仪表盘/深度报告*。

### 4.2 设计 tokens（`style.css:6-30`）

**中性色（纸面层次）**

| token | 值 | 用途 |
|---|---|---|
| `--bg` | `#FBF8F3` | 页面底色（米白） |
| `--paper` | `#FFFFFF` | 卡片纸面 |
| `--ink` | `#2B2622` | 正文墨色 |
| `--ink-soft` | `#5B5147` | 次级文字 |
| `--ink-faint` | `#8C8177` | 弱化文字/脚注 |
| `--line` / `--line-soft` | `#E9E1D6` / `#F1EBE1` | 边框 / 浅背景 |

**品牌色（赭橙手写笔）**

| token | 值 | 用途 |
|---|---|---|
| `--brand` | `#D9764A` | 主色：part 序号、当前态标签、强调 |
| `--brand-dark` | `#B85A34` | 链接、公式、eyebrow 文字 |
| `--brand-bg` | `#FCEBD9` | 类比框底、高亮行、重点下划线 |

**语义色（内容状态，不装饰用）**

| 语义 | 前景/背景 | 用于 |
|---|---|---|
| good | `#3E8362` / `#E7F2EB` | 正确、健康、已完成 |
| bad | `#C0433D` / `#FBEAE8` | 错误、风险、坑 |
| info | `#3E7E96` / `#E8F1F5` | 中性提示 |
| warn | `#C1892A` / `#FBF1DE` | 警戒、阈值提醒 |

**全局**

| token | 值 |
|---|---|
| `--shadow` | `0 2px 10px rgba(43,38,34,.06), 0 1px 2px rgba(43,38,34,.05)`（双层浅影） |
| `--radius` | `16px`（卡片）；内部小元素 8~12px |

### 4.3 字体系统

| 层 | 字体栈 | 规格 |
|---|---|---|
| 标题 h1–h4 | `"Songti SC","Noto Serif SC",Georgia,…,serif`（衬线） | masthead h1 30px；part h2 23px；行高 1.4 |
| 正文 | `-apple-system,BlinkMacSystemFont,"PingFang SC",…,sans-serif` | 16px，行高 **1.75**（疏朗书页感） |
| 代码/公式 | `"SF Mono",Menlo,Consolas,monospace` | 13~13.5px，赭橙字色 + 米色底 |

`strong` 语义强调 = **下半 40% 赭橙荧光笔**（`linear-gradient(transparent 60%, var(--brand-bg) 60%)`）——全站最独特的视觉签名。

### 4.4 版式

- 内容列 `.container` / `.wrap`：`max-width: 900px` 居中，左右 padding 24px，`.wrap` 底部留白 80px。
- Part 间距 `52px 0`（大呼吸感）；卡片间距 16~20px。
- masthead：`#FFF8EF → --bg` 垂直渐变 + 底边框，营造"翻开扉页"感。
- 链接：品牌深色 + 底部 1px 品牌浅色下划线，hover 加深。

### 4.5 响应式断点

| 断点 | 变化 |
|---|---|
| `≤760px` | `.figure-pair` 双图 → 单列；`.cheat-grid` 3列 → 2列 |
| `≤640px` | `.roadmap-grid`、`.concept-grid` 双列 → 单列 |
| `≤520px` | `.cheat-grid` → 单列 |

图表容器 `chart-wrap` 定高（标准 320px / short 230px）+ `responsive:true, maintainAspectRatio:false`，天然自适应宽度。

---

## 5. 组件库规范

所有组件都在 `style.css` 中全局定义，按**内容功能**分组。何时用哪个组件的判定表：

| 组件 | class | 用途 | 典型场景 |
|---|---|---|---|
| 顶部横幅 | `.masthead` + `.eyebrow` | 模块扉页 | 标题/钩子/breadcrumb |
| 局部导航 | `.local-nav` | sticky 锚点导航 | Part 跳转 |
| 学习清单 | `.checklist` | 可检验学习目标 | 页首 |
| 正文单元 | `.part` `.part-head` `.part-num` `.part-lede` | 一级章节骨架 | 每个 Part |
| 类比框 | `.analogy`（虚线赭橙边框） | 直觉化引入新概念 | 痛点/新机制前 |
| 概念卡 | `.concept-grid` + `.concept-card` | 术语卡：`.c-name` 中文名 / `.c-en` 英文或音标（等宽字体）/ `.c-def` 定义 / `.c-formula` 公式 / `.c-mnemonic` 斜体"记忆点" | 指标图鉴、核心概念 |
| 提示框 | `.callout`（info/good/bad/warn 左粗边） | 结论/提醒/警告 | 图表结论、阈值提醒 |
| 坑卡 | `.pitfall`（bad 色左边框 5px） | 踩坑警示 | "三个坑"章节 |
| 方法步骤 | `.method-step`（`.m-num` 圆形序号）+ 内嵌 `pre` 深色代码块 | 操作流程（含代码） | 数据加工步骤 |
| 案例步骤 | `.case-step`（`.step-badge` 墨色圆徽 + `.result` 加粗结论） | 案例推进叙事 | 实战案例 |
| 计算框 | `.calc-box`（等宽字体，`.eq` 赭橙加粗） | 手算过程展示 | 公式代入 |
| 数据表 | `table.tbl`（+ `.num` 右对齐等宽 / `tr.hl` 荧光行高亮 / `.table-scroll` 横向滚动） | 数据/对照表 | 十分位表、分箱表 |
| 图表卡 | `.chart-card`（`.chart-title` / `.chart-sub` / `.chart-wrap` / `.legend-note` / `.chart-footnote`） | Chart.js 容器 | 教学图表 |
| 真实图 | `.figure`（img + `.fig-cap`）、`.figure-pair` 双列 | matplotlib 出图 | 真实数据案例 |
| 时间轴 | `.mob-timeline` + `.mob-step`（节点+连线） | 顺序概念图 | MOB/样本切分 |
| 流程图 | `.rollrate-row` + `.rr-box`（M0~核销五档色阶）+ `.rr-arrow`（内嵌进度条） | 状态流转 | 迁徙率路径 |
| 速查卡 | `.cheat-grid` + `.cheat-card`（**墨色暗卡**，唯一深色组件） | 速查表 | 倒数第二 Part |
| 自测卡 | `.quiz-item`（`details/summary`，`▸/▾` 自定义箭头） | 折叠式答题 | 自测 |
| 小结 | `.summary-box`（暖渐变）+ `.mnemonic-line`（上下虚线口诀） | 收束 | 文末 |
| 标签 | `.tag`（`tag-current` 赭橙实底 / `tag-good` / `tag-todo` / `tag-bad` / `tag-info` / `tag-warn` / `tag-real` 墨色反白） | 状态徽章 | roadmap、"真实数据"标记 |
| 路线图卡 | `.module-card`（`.linked` 可点悬浮上浮 / `.current` 赭橙描边） | 模块入口 | index |
| 顺序条 | `.order-strip` + `.chip`（`done-chip` ✓绿 / `current-chip` 橙） | 学习顺序可视化 | index |
| 页脚/下一步 | `.page-footer` / `.next-card` | 收尾导航 | 文末 |

**排版语法约定**：
- 数字列一律 `td.num`（右对齐 + 等宽字体），关键行 `tr.hl`（荧光底 + 加粗），表中结论行用 `td` 内 `<strong>`。
- 图表配色**必须服从语义**，不按美观挑色（见 §6.2）。

---

## 6. 图表规范

### 6.1 双图表体系

| | 教学图表 | 真实数据图 |
|---|---|---|
| 工具 | Chart.js 4.4.4（CDN，jsdelivr） | matplotlib 离线出图 → PNG |
| 数据 | 手造示例数据 | 静态池披露文件（Excel 源） |
| 容器 | `.chart-card` 内 `.chart-wrap` 定高 canvas | `.figure` / `.figure-pair` + `.fig-cap` |
| 必带脚注 | `.chart-footnote`：`示例数据，用于教学演示，非真实业务数据。` | `.fig-cap` 说明图读法与关键结论；数据来源在 callout/页脚声明 |
| 溯源标记 | 无 | 正文配 `tag-real` 真实数据标签 |

### 6.2 Chart.js 标准配置（每页 script 块开头统一设置）

```js
const gridColor = '#EFE7DA';
Chart.defaults.font.family = "-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif";
Chart.defaults.font.size = 12.5;
Chart.defaults.color = '#5B5147';
```

实例通用约定：`responsive:true, maintainAspectRatio:false`；图例 `position:'top', align:'end'`，`boxWidth:10, usePointStyle:true`（常配 `display:false` 改用卡片下方的 `.legend-note` 手写图例）；柱图 `borderRadius:4`；折线 `tension:0.25~0.3, borderWidth:2.5, pointRadius:2~3`；Y 轴百分比刻度 `callback:v=>v+'%'`；参考线一律虚线（`borderDash:[6,4]` 或 `[4,2]`，灰或 bad 红）；X 轴不画网格线。

**图表配色语义表**（与 §4.2 语义色一致，跨图一致使用）：

| 颜色 | 含义 |
|---|---|
| `#C0433D` bad红 | 坏客户/问题批次/恶化值/高风险段 |
| `#3E8362` good绿 | 好客户/健康批次/最优 |
| `#3E7E96` info蓝 | 对照序列（累计好客户/AUC 等） |
| `#C1892A` warn琥珀 | 警戒批次 |
| `#C9BFB2` 灰 | 基准/历史平均/建模时（"背景"系列） |

### 6.3 图表编号体系

每图有唯一短编号，写在 `.chart-title` 开头，保证跨模块交叉引用无歧义：

- 模块①：`图S1–S2`；模块②：`图W1–W3`；模块③：`图K1–K6`；模块④教学部分：`图A–D`；模块④真实案例：`图E–H`。
- 规则 = "图 + 模块专属字母前缀 + 序号"（新模块选未用过的前缀；模块④的 A–D/E–H 为历史例外，续写新模块一律用前缀制）。
- 正文引用图表时写"（图K3）"，卡片标题、callout 结论、正文三者数字必须互相对应。

### 6.4 真实数据图规范（模块④第⑩节沉淀的经验）

- **脱敏红线**：产品真名一律用"消费贷产品A/B1/B2/C"代替；全文、图表标题、文件名、fig-cap 都不得出现真实名称。新增内容前先 `grep` 检查漏改。
- **出图后验证**：凡"最优/最差/排名"类描述，必须用代码重新跑一遍排序验证，不能凭肉眼下结论（曾把全历史最差批次误标成"次差"）。
- 图表成对出现：关键月份图（5~6 个代表批次对比）+ 全口径光谱图（全部批次叠加、按放款时间冷暖渐变）。
- Excel 源文件位置会变（曾在 Downloads，后在 `~/Documents/file/0-发行台账/4-资产数据/静态池/`），续用前先确认路径。

---

## 7. 内容写作规范

### 7.1 语言风格

- 口语化、第二人称、短句；允许适度的比喻和情绪（"但这张图撒了谎"）。
- 每个结论都落到**具体数字**上（"从 10% 涨到 22%，几乎翻倍"），禁止只说"明显上升"。
- 概念卡固定带"记忆点"、小结固定带口诀（mnemonic-line）——**记忆锚点是内容的一部分**，不是装饰。

### 7.2 类比（analogy）使用法

每个新概念首次出现前，用一段生活类比垫场，label 带 emoji（🎯💡🍇👕🍲📏）。类比只负责"直觉"，紧随其后必须回到精确表述。已有类比池：靶场（类别不平衡）、葡萄酒（Vintage）、量体裁衣（PSI）、台阶（迁徙率）、熬汤食材（特征PSI）、同龄小孩身高（成熟度外推）。

### 7.3 跨模块叙事线（本手册最重要的内容设计）

模块①②③共享一条隐藏"连续剧"，数字完全互通：

```
module-02：用"近3个月申请次数"手算 WOE/IV（9500好+500坏样本，IV=0.563，高值段[6,8]+[9,+]占16.1%）
     ↓ 该特征被选入建模
module-01：同一特征进入评分卡（四变量算出总分628）；案例建模 KS=0.46 / AUC=0.79
     ↓ 同一组基线数字
module-03：同一模型上线9个月后衰退；PSI=0.179 拆箱 → 特征PSI排行 → "近3个月申请次数"PSI=0.19 严重漂移
           → 高值段占比 16.1% → 32%（呼应 module-02 算 WOE 时的高值段）
```

**维护规则**：
1. 三模块间用 `<a href="module-0X.html">` 交叉引用对应小节；
2. 任何改动涉及这条线上具体数字（样本量、KS/AUC、分箱边界、占比）时，**三处必须同步核对**；
3. 新模块若引入新案例，优先复用这条叙事线或开一条新的贯通线，避免孤立的"一次性案例"。

### 7.4 数据声明与引用

- 教学示例：图表脚注 + 页脚双重声明"教学演示，非真实业务数据"。
- 真实数据：正文 callout 说明来源格式（静态池披露文件、覆盖期间、批次数），页脚列出参考文献；对外来源（公众号文章）在 index"起点"callout 与模块④页脚致谢。
- 真实数据中的**方法论发现**（口径反转、外推偏差、排名纠错）本身写成教学内容，带"复核时抓到的一处错误"式的诚实披露——错误与边界是内容的一部分。

### 7.5 自测题写作法

固定 5 题，难度递进：概念辨析 → 定义复述 → **计算题**（题干给足数字和提示如 ln 值） → 信号判读 → **分析题**（开放排查题）。答案藏在 `details` 里，正文加粗关键结论，答完能反推回对应 Part。

---

## 8. 技术实现约束

| 项 | 约定 |
|---|---|
| 技术栈 | 纯静态 HTML + 单一共享 CSS + Chart.js CDN（4.4.4，jsdelivr），零构建、零框架、零本地 JS 依赖 |
| 交互 | 除 Chart.js 渲染外**无任何 JS 逻辑**；折叠交互用原生 `details/summary`（quiz），hover 用 CSS |
| 平滑滚动 | `html{scroll-behavior:smooth}`（锚点跳转） |
| 图表脚本位置 | `</body>` 前单个 `<script>` 块，先设 defaults 再逐图实例化 |
| 兼容目标 | 本机 Chrome/Safari 桌面 + 移动（响应式断点见 §4.5），不处理 IE |
| 预览 | `.claude/launch.json` 的 `credit-risk-handbook` 配置（`python http.server` 端口 8844） |
| 版本管理 | 项目独立于 DailyDigest 等其他项目，git 仓库根在 LikeCodeNex |

---

## 9. 续写新模块操作清单（以模块⑤为例）

1. 复制任一已完成模块页作为模板（推荐 module-03，结构最标准），改 title / breadcrumb / eyebrow（自选固定 emoji）/ h1 / sub。
2. 按模板改 checklist、local-nav、各 Part；图表编号启用新前缀（如 `图D1…`，避开已用的 S/W/K/A–H）。
3. 案例数据优先接入 §7.3 叙事线或新开一条贯通线；示例数据全部可复算。
4. 严格遵守：三个坑恰好 3 个、自测恰好 5 题、速查卡 8~9 张、教学图表每张带脚注。
5. 完成后同步 index.html 三处状态（§2.3），并为本文件 §2.1 表格补状态。
6. 若含真实数据：执行 §6.4 全部规则（脱敏 grep、排名代码验证、tag-real 标记、来源声明）。
7. 如需衍生教学版，按 §3.7 从完整版复制后删 4 处，首 N Part 保持逐字节一致。

---

## 附 A：设计 token 速查

```
米白底 #FBF8F3 ｜ 纸面 #FFFFFF ｜ 墨 #2B2622 / #5B5147 / #8C8177
线 #E9E1D6 / #F1EBE1 ｜ 赭橙 #D9764A / #B85A34 / #FCEBD9
good #3E8362/#E7F2EB ｜ bad #C0433D/#FBEAE8 ｜ info #3E7E96/#E8F1F5 ｜ warn #C1892A/#FBF1DE
圆角 16px ｜ 阴影双层浅影 ｜ 内容列 900px ｜ 正文 16px/1.75 ｜ 标题衬线 30/23px
断点 760/640/520 ｜ 图表高 320/230px ｜ 网格线 #EFE7DA ｜ 基准灰 #C9BFB2
```

## 附 B：模块图表编号占用表

| 模块 | 前缀/编号 | 图数 |
|---|---|---|
| ① 评分卡 | S1–S2 | 2 |
| ② WOE | W1–W3 | 3 |
| ③ 指标 | K1–K6 | 6 |
| ④ 教学 | A–D | 4 |
| ④ 真实案例 | E–H + 10.7 节未编号 figure-pair×6 | 4+6 |
