# 信贷风控学习手册 · 设计规格说明书（Design Spec）

> **版本**：v1.1 · 2026-09-21
> **来源**：基于当前仓库实际代码反向拆解（`index.html` + 模块①②③④共5个页面 + `style.css`，合计 3509 行）
> **用途**：①续写文章模块⑤⑥⑦、修改既有页面；②作为**其他 topic/领域生成学习手册的范本**——§10 和附 C/D 是泛化/复刻的入口。
> **维护约定**：发现代码与本文档不一致时，以代码实际行为为准，并回来更新本文档。

## v1.1 → v1.0 增量

- §2.3 增补「index 页面骨架 §2.4」：以前只有状态同步清单，现在补齐 index 自身结构（masthead/kicker 命名表/order-strip 约定/起点 callout）。
- §4.6 新增「组件微观细节表（含动效/特殊元件/未文档化的内联样式）」：m-num、case-step 徽章细节、quiz 箭头、dark-code block 7 个 spec 漏写的组件级细节全部补齐。
- §5 增补「组件调用矩阵（按内容场景反查）」：按"我要表达X"→"用哪个组件"的映射，给泛化场景用。
- §7.6 新增「内容节奏规则（密度/字数/心声）：电池、阈值表、反直觉、口语计数」。
- §7.7 新增「泛化用：本手册的设计参数」，把隐含的风格判定参数化。
- **§10（全文重写）新增「泛化驱动器：用本 spec 生成新领域手册」**：这是最泛化的一节——把"换一个 topic"的操作拆成必须替换/可以复用/必须重写三档，给出了新领域启动的 6 步范式。
- 附 C「跨领域复用判定表」：23 个组件/范式按 3 档通用性分组（直接复用/改样式/重新设计）。
- 附 D「模块页最小可复刻骨架（带组件序列）」：泛化 agent 可直接照着写的 9 槽骨架。

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

### 2.4 index 页面骨架（hub 页的结构规范）

index 自身也有固定骨架（index.html 共 100 行，高度模板化）：

```html
<header class="masthead">…eyebrow(📓 手册定位标签) + h1 + sub…</header>
<div class="wrap">
  <div class="part" style="margin-top:36px;">…MAP 段：说明双主线组织方式…</div>
  <div class="roadmap-grid">…7 张 module-card，已完成是 <a>，未完成是 <div>…</div>
  <div class="order-strip">…推荐学习顺序 chip 链，用 → 箭头连接…</div>
  <div class="callout info">…学习路径解释（"为什么先学模块四"）…</div>
  <div class="callout warn">…起点：种子文章/原始触发源，带外链和致谢…</div>
  <div class="page-footer">…左：定位声明 ｜ 右：已完成模块链接列表…</div>
</div>
```

**module-card 的 kicker 命名规范**（每模块的别名必须是一字中文，与 eyebrow emoji 对应，见 §2.1）：
- 命名逻辑 = 该模块在整个知识体系中扮演的角色，用一个名词概括。
- 已用：①骨架🏗️ ②手艺🛠️ ③标尺📏 ④透视镜🔍 ⑤决策 ⑥边界 ⑦外延。
- 泛化时给新模块取名的判定标准：能不能在 3 秒内让学习者猜到这个角色是干嘛的。

**order-strip 的箭头与 chip 文案**：未完成模块的 chip 不带序号箭头之后的✓，已完成模块 chip 前缀`✓ `；推荐学习顺序与模块编号的映射写在 chip 上的阿拉伯数字上（`①②③④⑤⑥⑦` = 模块编号，前缀数字 + 短横线才是学习顺序）。注意 index.html 用 `推荐第③步 · 已完成` 标签格式明示顺序——第一个数字是全站在用的推荐顺序编号，别和模块编号弄混；当前在学模块用 `tag-current` + 卡片 `.current` 高亮（模块④的"当前在学"是历史遗留，写新模块时应把"当前在学"移到最新写的模块上）。

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

### 4.6 组件微观细节表（v1.0 漏写的组件级规格）

上表（§5）只写了组件"是什么、什么时候用"，下面这些是泛化/复刻时必须写对、但 v1.0 没写清的细节：

| 组件 | 隐藏的硬规则 |
|---|---|
| `.masthead .sub` | `max-width:640px`，超了自动换行但不截断——留给钩子文案的"单行视觉上限"参考 |
| `.breadcrumb a` | 有专属样式：颜色 `--ink-faint` + `border-bottom:1px dotted var(--line)`（不是普通链接样式），是"低调可点" |
| `.tag` | 所有徽章统一 `border-radius:100px` 药丸形 + `letter-spacing:.02em`；`tag-real` 是墨色底+米色字（唯一反白徽章，区别于所有语义色徽章） |
| `.checklist li::before` | ✓ 前缀是伪元素，不是文本；换 li 的前缀符号要改 CSS 不是改 HTML |
| `.analogy .label` | 类比框的 label 没有底部边框（区别于 callout 的 label）；且类比框**只有** `.analogy` 一种样式，不做语义分级（不能加 `.analogy.warn`） |
| `.m-num`（method-step） | 背景/前景用 **info 蓝系**（`--info-bg`/`--info`），而且是固定 `width:26px`、`margin-top:2px`——序号必须在圆内垂直居中，不能换色 |
| `.step-badge`（case-step） | 背景 `--ink` 对白字、固定 `width:22px`、与 `.m-num` 同一个圆形但**颜色不同**；除了第一步，**后续步骤都不用再显示徽章**（靠 `margin-left:38px` 的缩进表示"属于同一步骤流"）——这个 38px 现在靠内联样式硬编码，泛化时可以直接复用这个值 |
| `.quiz-item summary` | 自定义箭头 `▸/▾`；`list-style:none` + `::-webkit-details-marker{display:none}` 把原生 marker 隐藏，否则会出现两套箭头；`cursor:pointer` 是必写 |
| `.cheat-card b` | cheat 卡里 `<b>用途：</b>/<b>阈值：</b>` 的前缀被加了赭橙色（`color:var(--brand)`）——这就是为什么速查卡里标签会发光，泛化时这个 `<b>` 前缀必须保留 |
| `.mnemonic-line` | 上下两条**虚线**（`border-top/bottom:1px dashed var(--brand)`），不是单虚线边框——口诀要"被夹起来"的视觉感 |
| `.mob-step::after` | 时间轴的连接线是伪元素画的：`top:6px; left:50%; width:100%; height:2px`，最后一个 step 的 `::after` 被隐藏（`display:none`）——新增 step 不用管，CSS 自动处理连线 |
| `.figure img` | `border-radius:12px` + `border:1px solid var(--line)`：图表有明确的"卡片"边界，不是裸贴 |
| `.figure-pair .fig-cap` | 双图模式下 caption **居中**（区别于 `.figure` 单图左对齐）——泛化时 figure-pair 的 fig-cap 天然居中 |
| `.page-footer` | `flex-wrap:wrap; gap:10px`：左右两栏在窄屏自动换行到两行，不重叠 |
| `.next-card .n-arrow` | `font-size:22px; flex-shrink:0`：箭头不会跟随 flex 被压缩，始终维持恒定大小 |
| `strong` | `padding:0 1px`：`linear-gradient` 下 60% 的荧光笔区域太贴字会糊，加 1px 内边距拉开 |
| `code` | 前景色 `--brand-dark` 不是黑色——行内代码在视觉上=赭橙色的"笔记批注"，不是等宽字体的默认灰 |
| `.part-lede` | `margin-top:-4px`：视觉补偿 part-head 和 lede 之间的间距，泛化时不要发现 lede 贴近就自行加 margin |

**4 个未文档化的内联样式**（HTML 里散落的，泛化时当作规范确认）：

1. `.checklist` 在模块页上 `style="margin-top:32px"`——checklist 是页面第一个元素，需要和 sticky nav 拉开距离；
2. `.case-step` 带 `style="margin-left:38px;"`（见上）——这个缩进表示"同一个 case 动作链里的后续步骤"；如果新 case 串了 6 个 step，第 1 个保留正常 `.case-step` 带徽章，第 2~6 个全加 `margin-left:38px` 且不写徽章；
3. `h3`（`font-size:17px; margin-top:32px/36px`）——模块内子章节（如真实数据案例 10.1~10.7）的 H3 用内联样式控制字号，这个 17px 也是模块内 H4（`font-size:15.5px; margin:24px 0 6px`）对照出的规范；泛化时模块内子章节就按这对值写；
4. 段落字号的局部覆写：`style="font-size:14.5px; color:var(--ink-soft);"`（普通段落在某些案例/列表里的微调版），`style="margin:6px 0 0; padding-left:20px; font-size:14.5px;"`（case-step 里 ul 的专用样式）。

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

### 5.1 组件调用矩阵（按"我要表达什么"反查）

泛化到新领域时，不知道该用哪个组件 → 查这张表（内容功能 → 组件 → 判定标准）：

| 我想表达 | 首选组件 | 不用它的判断标准（什么时候退到别的） |
|---|---|---|
| "先泼冷水，打破你的错误直觉" | `.analogy` | ≥2 个连续错误直觉 → 拆两个 analogy 段；纯粹的结论/提醒（没有类比） → 用 `.callout` |
| "这是一个术语/概念/指标" | `.concept-card`（grid 布局） | 这个概念有公式/记忆点 → 必须填 `.c-formula`/`.c-mnemonic`；没有 → 考虑合并到列表里而不是膨胀卡片 |
| "按步骤做这件事" | `.method-step`（含代码） + 内嵌 `pre` | 步骤不涉代码（纯概念操作） → 用 `.case-step` 降为"纯叙事步骤" |
| "发生了一个故事，有先后顺序" | `.case-step`（第一步带徽章，后续 `margin-left:38px`） | 只有 1~2 步 → 不启用 `.case-step`，直接用 `<p>` 或 `.callout` |
| "展示一段手算/公式代入" | `.calc-box`（`.eq` 高亮关键代入值） | 超过 3 行 → 拆成多个 calc-box 或者用表格替代；⚠️ calc-box 不是列表容器，不要塞 `<ul>` |
| "列出对比表/数据表" | `table.tbl`（+ `num` 右对齐数字列 + `tr.hl` 高亮关键行） | 列数过多（~>6） → 改用 `.table-scroll` 包裹；行数 >13 且是无序列 → 考虑改用 `.concept-grid` |
| "画一张图" | `.chart-card`（必带 `.chart-footnote` 声明"示例数据"） | 真实数据 → `.figure` + `tag-real`；'图 + 文字说明' → 拆成 `chart-card` + `.callout` 结论 |
| "展示一个序列/时间线" | `.mob-timeline`（节点数 ≤ 9 个为宜） | 节点代表"状态"而非"时间" → 不要用时间轴，用 `.rollrate-row`；纯编号列表 → `ol/ul` |
| "展示流程/状态流转" | `.rollrate-row` + `rr-box`（M0~CO 五档色阶） | 流转不是单向的（有分叉、有回溯） → 不要用流程图，用 `.tbl` 的"来源→去向"对照表 |
| "提醒一个容易踩的坑" | `.pitfall`（恰好 3 个，见 §3.5） | 不是"坑"（只是普通提醒） → `.callout.warn`；坑有变形（多种情况） → 拆成多个 `.pitfall` 每张一个变型 |
| "小结/收尾金句" | `.summary-box` + `.mnemonic-line` | 已经有一句口诀 → 复用同一 `.mnemonic-line`；想得到下一个动作 → 在 `next-card` 里指向 |
| "一个词/徽章就够了" | `.tag`（6 个语义色 + `tag-real`） | "当前在学/推荐第N步/已完成/待更新" → 模块卡片专属语义；真实数据 → `tag-real` 只配真实数据页 |
| "一个指标、阈值、用法" | `.cheat-card`（速查卡：`<b>用途：</b>/<b>阈值：</b>` 前缀） | 不是速查表（正文内的补充） → 不要拉 `.cheat-grid`，放 `.callout` |
| "一串同主题入口（模块间跳转）" | module-card（非泛化 scope） | 模块内内联交叉引用 → 直接 `<a href="module-0X.html">` |
| "下钻某点、链接到本模块其他 Part" | 内文 `<a href="#pN">` | 指向其他模块 → `href="module-0X-keyword.html"`，文本里明确写'见模块X' |

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

实例通用约定：`responsive:true, maintainAspectRatio:false`；图例 `position:'top', align:'end'`，`boxWidth:10, usePointStyle:true`（常配 `display:false` 改用卡片下方的 `.legend-note` 手写图例）；柱图 `borderRadius:4`；折线 `tension:0.25~0.3, borderWidth:2.5, pointRadius:2~3`；参考线一律虚线（`borderDash:[6,4]` 或 `[4,2]`，灰或 bad 红）；X 轴不画网格线。

**⚠️ 坐标轴单位一致性（硬规则）**：**凡是承载百分比数值的轴，无论 X 还是 Y，刻度都要带 `%`**——`ticks:{ callback:v=>v+'%' }`。一张图里绝不允许出现"Y 轴带 %、X 轴不带 %"这种一图两制。只有轴承载的是**分类标签**（分箱区间、十分位、MOB、月份、IV/PSI 这类无量纲比值）时才不加单位。

| X 轴承载 | 轴类型 | 刻度写法 |
|---|---|---|
| 分类标签（`[500,550)`、`十分位1`、`MOB3`、`25-06`） | 默认 category（`labels:[...]`） | 原样，不加单位 |
| 百分比数值（FPR 累计好%） | `type:'linear'` + 数据用 `{x,y}` | `callback:v=>v+'%'` |
| 无量纲比值（IV、PSI、WOE、Odds） | `type:'linear'` | 不加单位，单位写在 `title.text` |

百分数 X 轴实例（图K2 ROC 曲线）：数据必须是 `{x,y}` 点对而非 `labels` 数组——用 `labels` 会把连续比例当成等距分类，"随机基准线"也会被凑成斜线假象。正确写法：

```js
data: { datasets: [
  { label:'ROC曲线（AUC≈0.79）', data:[{x:0,y:0},{x:8.9,y:30.0},{x:18.2,y:54.0}, /* … */ {x:100,y:100.0}], /* … */ },
  { label:'随机模型基准线（AUC=0.5）', data:[{x:0,y:0},{x:20,y:20},{x:40,y:40},{x:60,y:60},{x:80,y:80},{x:100,y:100}], /* … */ }
]},
scales: {
  y: { type:'linear', min:0, max:100, ticks:{ callback:v=>v+'%' }, /* … */ },
  x: { type:'linear', min:0, max:100, ticks:{ stepSize:20, callback:v=>v+'%' }, grid:{ display:false }, /* … */ }
}
```

参照线若是"y=x 对角基准"，必须写成真实等值点对 `{x:20,y:20}`，不要写 `[0,10,20,…]` 靠分类索引凑出视觉斜线。

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

### 7.6 内容节奏规则（密度/字数/心流）

v1.0 只写了"痛点先行""凡例子必可复算"两条内容原则，下列四项是从 4 个模块正文里反推出的**隐性节奏**，泛化最容易写崩的就是它们：

**(i) 电池式标题（电量只剩 60% 时最刺眼）** 📏
- 每个指标/概念在第一次出现在 `.chart-title` 里时，写法固定：`图K3 · 评分分布对比：建模时 vs 9个月后`——冒号前是对象，冒号后是对比/发现/结论（"KS 曲线：两条累计占比曲线之间垂直距离最大的地方，就是 KS"）。**冒号后的那句脑补比图表本身更能教会人**。
- h1 页面标题也是问题式/结论式而非描述式（模块1 是"A卡/B卡/C卡…概率怎么变成分数"，模块3 是"KS/AUC/PSI/Lift：怎么判断一个模型好不好、稳不稳"）——标题本身就是钩子。

**（ii) 阈值表：每一组成组指标都必须配"`→业务判断`"表**
- KB/AUC/PSI/Gini 各自的区间判断表（`table.tbl` + "AUC 区间 → 业务判断"）；老猫的 P0/PDO 也同表对照。**没有阈值表的指标 = 教学失败**——学习者不知道"这个数字还算不算行"。

**（iii) 反直觉（consistent surprise)：每隔 2~3 个 Part 必须有一个"你以为 X，其实 Y"的强调**
- 模块④的"逾期率环比下降反而说明风险变好了→错"、模块③的"准确率99%却拒绝上线"、模块①的"C卡分数高≠该少催"。
- 手法固定：**先给一句表面上合理的结论，然后立刻用 `.callout.bad` 或 `.pitfall` 戳破**，并落到具体数字（"从 10% 涨到 22%，几乎翻倍"）。
- 泛化时：如果写完感觉通篇没有"打脸点"，数据故事太平——大概率回顾 §3.5 的"痛点先行"做的不到位，这个模块要么不该写，要么知识密度不够。

**（iv) 口语计数："举个例子"的精确呈现**
- 范例不是"比如某特征很重要"，而是"模型从上线时 KS=0.46 / AUC=0.79，9个月后降到 0.38 / 0.74，PSI 从 0.02 爬到 0.179——三条线同时报警，这就是该迭代了"。
- 计时感：数字**必须跟时间、量级、对比对象绑定**（"上线时 / 9个月后" / "128倍 / 10年"）。

### 7.7 泛化用：本手册的设计参数（泛化/复刻时的默认值）

把"信贷风控手册"的判断转换成可移植的泛化参数：

| 参数 | 值 | 在新领域里的判定标准 |
|---|---|---|
| 知识主线数 | **2 条**（业务生命周期 × 方法论层次） | 新领域必须找到 2 条独立的正交主线；找不到 → 知识不适合模块化，别强做 |
| 模块数 | **7** | 有效范围 5~10，少于此 → 合并；多于此 → 分拆 |
| 一个模块的 Part 数 | **10~11** | Part 太多 → 该分拆模块；太少 → 教学密度不够，需要重新拆骨架 |
| 每模块案例数 | **1 个完整手算案例** + 1 个真实数据案例（可选） | 案例要能"被学习者自己算一遍" → 所有数字给出；真实数据只有切入口成熟时才加 |
| 跨模块叙事线数 | **1 条**（主线层面的"连续剧"） | 新领域：找到 1~2 个贯穿整个知识体系的"元问题"，让所有模块都能挂上去；没有贯通线 → 3 个模块就是 3 本孤立的手册 |
| 痛点开头位置 | **Part 1 恒为"先说痛点"** | 泛化时必须遵守；唯一例外是封面页 |
| 速查卡数 | **8~9 张** | 低于 6 → 说明该模块的"速查价值"不足，考虑缩编 |
| 自测题数 | **恰好 5 题** | 不按难度递进重写；>=6 题 → 分拆模块 |
| 坑数 | **恰好 3 个** | 坑的领域分布：一个过拟合类（数据）、一个口径类（定义）、一个监控类（实施） |

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
2. 按模板改 checklist、local-nav、各 Part；图表编号启用新前缀（如 `图G1…`，避开已用的 S/W/K/A–H、D）。
3. 案例数据优先接入 §7.3 叙事线或新开一条贯通线；示例数据全部可复算。
4. 严格遵守：三个坑恰好 3 个、自测恰好 5 题、速查卡 8~9 张、教学图表每张带脚注。
5. 完成后同步 index.html 三处状态（§2.3），并为本文件 §2.1 表格补状态。
6. 若含真实数据：执行 §6.4 全部规则（脱敏 grep、排名代码验证、tag-real 标记、来源声明）。
7. 如需衍生教学版，按 §3.7 从完整版复制后删 4 处，首 N Part 保持逐字节一致。

---

## 10. 泛化驱动器：用本 spec 生成新领域手册

本节回答一个核心问题：**如果换个 topic（比如"供应链金融""个人理财""量化交易基础"），要怎么用这份 spec 写出一本新手册？**

### 10.1 三档替换判定

换一个 topic，spec 的所有要素按可复用性分三档：

**(a) 原样复用（不改一个字）**
- style.css 全部设计 tokens（§4.2 中性色/品牌色/语义色/字体/阴影/圆角）——视觉签名就是为了跨领域复用的。
- 所有组件的 HTML 结构和 CSS 类名（§5 全表 + §4.6 微观细节）。
- Chart.js 全局 defaults（§6.2）。
- 语义色图表配色表（§6.2）——bad 红=负面、灰=基准，跨题材不变。
- 页面骨架 13 段（§3.1）、速查卡结构、pitfall 卡片结构、quiz 折叠结构。
- 双图表体系（§6.1）——教学 Chart.js + 真实数据 matplotlib 的分层逻辑不变。
- 技术栈约束（§8）——纯静态 + CDN + 无 JS 逻辑。

**(b) 换换样式就行（结构不变，内容微调）**
- 设计 tokens 的 `--brand` 色：新领域如果想换主色，改 `--brand`/`--brand-dark`/`--brand-bg` 三处即可，其余自动跟随。
- eyebrow emoji（§2.1 每模块一字中文别名 + 一个 emoji）：泛化时给新领域重新取一套（推荐选有隐喻的物件——🔍📏🏗️🛠️）。
- index 的 kicker 文案（"骨架/手艺/标尺/透视镜" → 换成新领域的隐喻词）。
- index 的 masthead sub（钩子文案）、order-strip 的学习顺序、callout 的"起点"推荐来源。
- 图表编号前缀（§6.3）——新领域启用全新字母前缀（例如"交易"用 T，避开已用的 S/W/K/A–H、D）。

**(c) 必须重写（不只是改写）**
- **§1.2 三条设计原则**——"痛点先行/凡例子必可复算/教学层与真实层分离"是这套手册的**方法论**，新领域必须重新找到自己的三条（不是直接照搬"信贷风控"的那三条）。
- **§2.1 双主线**——业务生命周期（贷前/贷中/贷后）是信贷特有的；新领域要找自己的正交主线（比如量化交易 = 数据维度 × 策略层次）。
- **§7.3 叙事线**——这是最难、也是最重要的一条。新领域必须找一条能贯穿所有模块的"连续剧"：一个特征/一个案例/一个数字在多个模块里反复出现且被重新计算。**没有这条线，新手册就变成 N 个独立文章的合集，不是一本"手册"**。
- **§9/§10 的所有"信贷"字眼**：替换成新领域的术语/案例/数据源。
- **真实数据来源**：信贷用的是静态池披露文件；新领域要找到自己的真实数据源（财报/公开 API/行业报告）。

### 10.2 新领域启动 6 步范式

1. **找双主线**：写下这个领域的两条正交组织轴（横向: 业务/对象的生命周期；纵向: 方法论/技术的层次）。如果只能找到一条轴，立即停手——这个领域还不到写手册的成熟度。
2. **拆 5~10 个模块，先行"命名"**：给每个模块取 1 字中文别名 + 1 个 emoji + 一句钩子文案。判断标准：不看正文，只看别名能不能让人猜到该模块讲什么。
3. **找一条叙事线**：确定一个具体的"元案例"——一个能在多个模块里被反复计算/引用的特征、数据集或业务事件。把它的完整数字链（样本量、关键指标值、阈值）写下来。**如果找不到这样的例子，这一步卡住了就先别往下走**。
4. **先写 index.html**：把 7 张 module-card 摆出来，用 callout 说明学习顺序和"为什么先学X"。目录结构稳定之后再动笔第一个模块。
5. **按 §3.5 骨架写第一个模块**：痛点（类比）→ 概念卡 → 手算 → 案例 → 3坑 → 速查（8~9卡）→ 5题自测。**写完后检查：这个模块里的某个具体数字，能不能在至少另一个模块里被重新提到/重新计算**——如果不能，说明叙事线断了，回头改。
6. **同步三处状态**（roadmap card / order-strip / footer），并按 §6.4 规范处理真实数据（如果有）。

### 10.3 泛化检查清单（Do-not-forget）

生成新领域手册时，下列任何一条没做到就是失败复刻：

- [ ] 找到了 2 条正交主线，不是 1 条
- [ ] 每个模块 Part 1 都是"先说痛点"
- [ ] 每个概念都有公式/例子/记忆点，凡例子必可复算
- [ ] 有 1 条跨模块的"连续剧"叙事线，数字互通
- [ ] 恰好 3 个坑、恰好 5 题自测、8~9 张速查卡
- [ ] 每个 Chart.js 图表都带"示例数据，非真实业务数据"脚注
- [ ] **每个图的 X/Y 轴单位一致**：承载百分比数值的轴刻度都带 `%`（一张图不能 Y 带 %、X 不带）；连续比例轴用 `type:'linear'` + `{x,y}` 点对，不用 `labels` 等距凑数
- [ ] 真实数据图带脱敏，`tag-real` 只配真实数据页
- [ ] strong 是荧光笔、cheat 卡是暗卡，这两个视觉签名没改
- [ ] 有复盘/纠错/口径反转的诚实披露（§7.4），不是全篇都"我很牛"
- [ ] 检查清单（checklist）里的每一条都是"动词开头、可检验"（"解释清楚…"而不是"理解…"）

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
| ⑤ 决策 | D1–D4 | 4 |

**已知遗漏（续写前必修）**：模块④的 `10.7 节` 有 6 张 `figure-pair` 图片未参与编号体系（没有"图I…"之类的续号），这是 v1.0 漏记的断裂点。续写新模块时：若模块含真实数据且有多产品/多变体对比图，**必须给它们续号**（建议模块④真实案例区改用 `图R1–R12` 或新前缀），不能让多张图处于无编号状态。

---

## 附 C：跨领域复用判定表

新领域 agent 逐行查这张表，决定每个组件"直接用/改样式/重新设计"：

| 组件 / 范式 | 复用档位 | 泛化备注 |
|---|---|---|
| style.css 全部 design tokens | ✅ 直接用 | 视觉系统就是为了跨领域 |
| 组件 HTML 结构（全部 §5 类名） | ✅ 直接用 | 结构即语义 |
| Chart.js 全局 defaults | ✅ 直接用 | 换 topic 不改 |
| 语义色图表配色（bad=负面/灰=基准） | ✅ 直接用 | 跨题材约定 |
| 页面骨架 13 段（§3.1） | ✅ 直接用 | 任何手册都是这个节奏 |
| 教学骨架（§3.5 痛点→概念→手算→案例→3坑→速查→5题） | ✅ 直接用 | 方法论核心 |
| `cheat-card` 的 `<b>用途：</b>/<b>阈值：</b>` 前缀 | ✅ 直接用 | 速查表的统一语法 |
| `tag-real` 标记 | ✅ 直接用 | 真实/教学数据分层 |
| 双图表体系（Chart.js 教学 + matplotlib 真实） | ✅ 直接用 | 分层即原则 |
| 技术栈约束（纯静态 + CDN） | ✅ 直接用 | 即"做一个能本地打开的 HTML" |
| **类比（analogy）使用法** | ⚠️ 改样式 | 新领域必须有自己的类比池（信贷的🍲👔📏 不能用在量化交易上） |
| **痛点 / 案例 / 坑 / 自测的具体内容** | ⚠️ 改内容 | 骨架照搬，内容全换 |
| **速查卡的指标/阈值** | ⚠️ 改内容 | KS/AUC/PSI 换成新领域的指标 |
| **index 的"起点" callout** | ⚠️ 改内容 | 换成新领域的种子来源 |
| **hook / kicker 文案** | ⚠️ 改内容 | 钩子文案要重写 |
| **双主线（§2.1）** | ❌ 重新设计 | 信贷的生命周期/方法论层次不能复制到新领域 |
| **三条设计原则（§1.2）** | ❌ 重新设计 | 方法论必须在新领域重新提炼 |
| **跨模块叙事线（§7.3）** | ❌ 重新设计 | 最难、最重要的一条（见 §10.1-c） |
| **真实数据来源** | ❌ 重新设计 | 找该领域自己的数据源 |
| **模块命名（kicker）** | ❌ 重新设计 | 不能用"骨架/手艺/标尺"那套隐喻 |
| **图表编号字母前缀** | ❌ 重新设计 | 避开已用的 S/W/K/A–H、D |
| **emoji / 别名** | ❌ 重新设计 | 新模块名+emoji |

---

## 附 D：模块页最小可复刻骨架（9 槽）

泛化 agent 可以直接把下面的 HTML 当作模板填空。标记 `{{...}}` 的是必须替换的槽位，`<!-- OPTIONAL -->` 是可省略的，`<!-- KEEP -->` 是泛化也不改的：

```html
<!DOCTYPE html><html lang="zh-CN">
<head>
  <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{模块N · 主题（关键词）}} | {{手册名}}</title>
  <link rel="stylesheet" href="style.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script> <!-- KEEP -->
</head>
<body>

<!-- SLOT 1: masthead -->
<header class="masthead"><div class="container">
  <div class="breadcrumb"><a href="index.html">{{手册名}}</a> › {{模块N}}</div>
  <span class="eyebrow">{{emoji}} 模块{{N}} · {{主题}}</span>
  <h1>{{问题式/断言式标题}}</h1>
  <p class="sub">{{钩子文案：用具体数字抛出一个认知冲突}}</p>
</div></header>

<!-- SLOT 2: local-nav（KEEP，只改 Part 数和文案） -->
<nav class="local-nav"><div class="container">
  <a href="#p1">① 痛点</a> <a href="#p2">② 概念</a> <a href="#p3">③ 图鉴</a>
  <a href="#p4">④ 手算</a> <a href="#p5">⑤ 案例</a> <a href="#p6">⑥ 坑</a>
  <a href="#p7">⑦ 速查</a> <a href="#p8">⑧ 自测</a>
  <!-- OPTIONAL: <a href="#p9">⑨ 真实数据</a> -->
</div></nav>

<div class="wrap">

<!-- SLOT 3: checklist（KEEP，6~9 条，动词开头） -->
<div class="checklist" style="margin-top:32px;">
  <h4>本节读完，你能做到</h4>
  <ul>
    <li>解释{{概念1}}…</li> <li>手算{{指标1}}…</li>
    <li>走一遍{{案例}}…</li> <li>避开…个坑…</li>
    <!-- OPTIONAL: <li>（进阶）…真实数据…</li> -->
  </ul>
</div>

<!-- SLOT 4: Part 1 痛点（KEEP，标题句式固定） -->
<div class="part" id="p1">
  <div class="part-head"><span class="part-num">01</span><h2>先说痛点：{{朴素做法为什么会骗人}}</h2></div>
  <p class="part-lede">{{一句导语}}</p>
  <div class="analogy"><span class="label">{{emoji}} 一个类比</span>{{生活类比}}</div>
  <p>…</p>
  <table class="tbl"><!-- 业务问题 → 该用的指标 对照表 --></table>
  <div class="callout bad"><span class="label">{{反直觉点}}</span>{{解释}}</div>
</div>

<!-- SLOT 5: Part 2..N-5（概念→图鉴→手算→案例） -->
<div class="part" id="p2">
  <div class="part-head"><span class="part-num">02</span><h2>{{核心概念}}</h2></div>
  <p class="part-lede">…</p>
  <div class="concept-grid">
    <div class="concept-card"><div class="c-name">{{中文名}}</div><div class="c-en">{{英文}}</div>
      <div class="c-def">{{定义}}</div><div class="c-formula">{{公式}}</div>
      <div class="c-mnemonic">{{记忆点}}</div></div>
    <!-- ×2~4 -->
  </div>
</div>

<div class="part" id="pN"><!-- 手算 Part -->
  <div class="part-head"><span class="part-num">0N</span><h2>手算一遍{{指标}}</h2></div>
  <div class="method-step"><div class="m-num">1</div><div class="m-body"><h4>{{步骤标题}}</h4>{{说明}}<div class="calc-box">{{代入}} <span class="eq">{{结果}}</span></div></div></div>
  <table class="tbl"><tr><th>…</th></tr><tr class="hl"><td class="num">…</td></tr></table>
  <div class="chart-card">
    <div class="chart-title">图{{前缀}}{{N}} · {{对象}}：{{发现句}}</div>
    <div class="chart-sub">{{读图提示}}</div>
    <div class="chart-wrap"><canvas id="chart{{X}}"></canvas></div>
    <div class="legend-note"><span><span class="dot" style="background:#C0433D"></span>{{系列1}}</span></div>
    <div class="chart-footnote">示例数据，用于教学演示，非真实业务数据。</div> <!-- KEEP -->
  </div>
  <div class="callout good"><span class="label">{{指标值}}，{{发现}}</span>{{解读}}</div>
</div>

<div class="part" id="pN"><!-- 案例 Part -->
  <div class="part-head"><span class="part-num">0N</span><h2>实战案例：{{故事标题}}</h2></div>
  <div class="case-step"><div class="step-badge">1</div><div class="step-body"><h4>{{第一步}}</h4>{{描述}}</div></div>
  <div class="case-step"><div class="step-body" style="margin-left:38px;"><h4>{{第二步}}</h4>{{描述}}<span class="result">→ {{结论}}</span></div></div>
  <!-- … -->
</div>

<!-- SLOT 6: 三个坑（恰好 3 个） -->
<div class="part" id="pN"><div class="part-head"><span class="part-num">0N</span><h2>三个容易踩的坑</h2></div>
  <div class="pitfall"><div class="pit-title">坑一 · {{标题}}</div>{{内容}}</div>
  <div class="pitfall"><div class="pit-title">坑二 · {{标题}}</div>{{内容}}</div>
  <div class="pitfall"><div class="pit-title">坑三 · {{标题}}</div>{{内容}}</div>
</div>

<!-- SLOT 7: 速查表（8~9 张） -->
<div class="part" id="pN"><div class="part-head"><span class="part-num">0N</span><h2>本节速查表</h2></div>
  <div class="cheat-grid">
    <div class="cheat-card"><div class="cc-name">{{指标}}</div><div class="cc-detail">{{定义}}<br><b>用途：</b>{{场景}}</div></div>
    <!-- ×8~9，最后一张恒为"三个坑"汇总 -->
    <div class="cheat-card"><div class="cc-name">三个坑</div><div class="cc-detail">{{坑1}}/{{坑2}}/{{坑3}}</div></div>
  </div>
</div>

<!-- SLOT 8: 自测（恰好 5 题，难度递进） -->
<div class="part" id="pN"><div class="part-head"><span class="part-num">0N</span><h2>自测：检验一下是不是真的懂了</h2></div>
  <div class="quiz-item"><div class="q-title">Q1. {{概念辨析题}}</div>
    <details><summary>查看解析</summary><div class="answer"><b>{{关键结论}}</b>{{解析}}</div></details></div>
  <div class="quiz-item"><div class="q-title">Q2. {{定义复述题}}</div><details><summary>查看解析</summary><div class="answer">…</div></details></div>
  <div class="quiz-item"><div class="q-title">Q3. 计算题：…（提示：ln(X)≈…）</div><details><summary>查看解析</summary><div class="answer">…<b>{{结果}}</b></div></details></div>
  <div class="quiz-item"><div class="q-title">Q4. {{信号判读题}}</div><details><summary>查看解析</summary><div class="answer">…</div></details></div>
  <div class="quiz-item"><div class="q-title">Q5. 分析题：{{开放排查题}}</div><details><summary>查看解析</summary><div class="answer">…</div></details></div>
</div>

<!-- OPTIONAL: Part 真实数据（如果含真实数据案例，参考模块④的结构） -->

<!-- SLOT 9: 收尾三件套（KEEP） -->
<div class="summary-box">
  <h3>本节小结</h3>
  <p>{{一段总结：两条本模块的"准/稳"主线}}</p>
  <div class="mnemonic-line">{{口诀}}</div>
</div>
<div class="next-card"><div><div class="n-label">下一步</div><div class="n-title">回到路线图，选择下一个模块继续学</div></div><div class="n-arrow">→</div></div>
<p style="text-align:center;"><a href="index.html">← 返回{{手册名}}总目录</a></p>
<div class="page-footer">
  <span>{{手册名}} · 模块{{N}}</span>
  <span>{{教学页："示例数据均为教学演示用途，非真实业务数据" / 真实数据页：写明来源与参考文献}}</span>
</div>

</div>

<!-- SLOT 10: Chart.js script（KEEP，逐图实例化） -->
<script>
const gridColor = '#EFE7DA';
Chart.defaults.font.family = "-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif";
Chart.defaults.font.size = 12.5; Chart.defaults.color = '#5B5147';
<!-- 逐图 new Chart(...) -->
</script>
</body></html>
```

**这个骨架覆盖了 §3.1 的完整 13 段，只多了"真实数据 Part"这个可选项——其余全部保留。拿去泛化时，把 `{{...}}` 替换掉 + 检查附 C 的判定表，就能产出一个结构正确的模块页。**
