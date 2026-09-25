# Atlas · 全站设计系统

> 层级：**全局**。所有课题共用，改这里会影响全站。
> 单字数定位：**视觉 + 工程**（不含教学方法论，见 [PEDAGOGY.md](PEDAGOGY.md)；不含课题专属参数，见各课题 `TOPIC.md`）。
> 事实来源约定：本文件是规范；`style.css` 是代码实现。两者不符时，校验器以代码为准并回报差异。

## 1. 设计原则

- 纯静态、零构建：HTML + 单一共享 CSS + CDN/本地 vendor 的 Chart.js；除图表外无 JS 逻辑。
- 风格：暖色手写笔记感（米白底 + 赭橙主色 + 衬线标题），与"仪表盘/深度报告"风刻意区分。
- 教学层与真实层分离：教学图 = Chart.js + 教学脚注；真实数据图 = 静态 PNG（figures/）+ `tag-real`。

## 2. Design tokens（`style.css:6-30`）

```
底色    --bg #FBF8F3   纸面 --paper #FFFFFF
墨色    --ink #2B2622  --ink-soft #5B5147  --ink-faint #8C8177
线条    --line #E9E1D6  --line-soft #F1EBE1
品牌    --brand #D9764A  --brand-dark #B85A34  --brand-bg #FCEBD9
语义    good #3E8362/#E7F2EB  bad #C0433D/#FBEAE8
        info #3E7E96/#E8F1F5  warn #C1892A/#FBF1DE
圆角    --radius 16px    阴影 --shadow（双层浅影）
断点    760 / 640 / 520 px      内容列宽 900px      图表高 320 / 230px
```

字体：正文 `-apple-system, PingFang SC… sans`；标题 `Songti SC, Georgia… serif`；数字 `Menlo/Consolas`。

**visual signature（改了就等于破坏了手册的脸）**：
- `strong` = 赭橙荧光笔（`linear-gradient(transparent 60%, brand-bg 60%)`）；一段只强调少量关键词/数字/边界，避免整段高亮。
- `.source-driven .para-lead` = 段首总结句（写在段落内的 `<strong class="para-lead">`）：单独成行、不铺整行荧光底；后面的普通 `<strong>` 仍可高亮关键事实。桌面和手机保持相同阅读顺序，无需横向排版。
- `cheat-card` = 暗卡（墨底 #2B2622），内部 `<b>` 用 brand 赭橙，**不要用 `<strong>`**（荧光笔压在暗底上不可读）
- `tag-real` 只配真实数据

## 3. 组件库（全站通用）

声明式表格，详见 `style.css`。骨架层级：

```
masthead(breadcrumb+eyebrow+h1+sub) → local-nav → wrap
  ├─ checklist（学习目标）
  ├─ part × N（part-head/part-num/part-lede + 各组件）
  ├─ summary-box（含 mnemonic-line）
  ├─ next-card → 返回链接 → page-footer
```

| 组件 | 类名 | 用场景 |
|---|---|---|
| 类比框 | `.analogy` | 新概念首次出现前的生活类比 |
| 提示框 | `.callout.good/bad/warn/info` | 反直觉点、落地方案、案例备注 |
| 坑卡 | `.pitfall` > `.pit-title` | 「三个坑」part |
| 概念卡 | `.concept-grid` > `.concept-card` > `.c-name/.c-en/.c-def/.c-formula/.c-mnemonic` | 名词速览、双方案对比 |
| 手算步骤 | `.method-step` > `.m-num/.m-body`（可含 `.calc-box > .eq`） | 手算案例 |
| 案例步骤 | `.case-step` > `.step-badge/.step-body`（`.result` 为结果行） | 实战案例流水 |
| 图表卡 | `.chart-card` > `.chart-title/.chart-sub/.chart-wrap/.legend-note/.chart-footnote` | 所有 Chart.js 图 |
| 自测卡 | `.quiz-item` > `.q-title` + details/summary + `.answer` | 自测 |
| 速查卡 | `.cheat-grid` > `.cheat-card` > `.cc-name/.cc-detail` | 速查表 |
| 表格 | `table.tbl`（`td.num` 数字右对齐；`tr.hl` 高亮行；`.table-scroll` 包裹） | 数据表 |
| 时间轴 | `.mob-timeline` > `.mob-step`（账龄/阶段示意） | MOB 型图示 |
| 真实数据图 | `.figure`（`.fig-cap`）/`.figure-pair` | 静态 PNG |

**语境类规则**：`.dot/.arrow/.chip/.cc-name/.cc-detail/.c-name/.c-en/.c-*/.m-*/.step-*/.q-title/.answer/.pit-title/.eq` 只在其父容器内有样式。校验器对这些做祖先链校验（`tools/check_handbook.py` 渲染完整性检查）。

## 4. 图表规范

### 4.1 Chart.js 全局 defaults（每页 script 开头必需）

```js
const gridColor = '#EFE7DA';
Chart.defaults.font.family = "-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif";
Chart.defaults.font.size = 12.5;
Chart.defaults.color = '#5B5147';
```

- 实例约定：`responsive:true, maintainAspectRatio:false`；`legend:{position:'top',align:'end',boxWidth:10,usePointStyle:true}`（常配 `display:false` 改用 `.legend-note` 手写图例）；柱图 `borderRadius:4~6`；折线 `borderWidth:2.5, pointRadius:2~3, tension:0.25~0.3`；参考线一律虚线；X 轴不画网格。
- **坐标轴单位一致性（硬规则）**：承载百分比的轴刻度一律带 `%`（`ticks:{callback:v=>v+'%'}`）；一图两制禁止。
- 连续比例轴用 `type:'linear'` + `{x,y}` 点对，不用 `labels` 等距凑数。

### 4.2 配图色语义表

`#C0433D`=坏问题/恶化；`#3E8362`=好/最优；`#3E7E96`=对照序列；`#C1892A`=警戒；`#C9BFB2`=基准灰。跨题材不变。

### 4.3 图表编号

规范 = "图 + 课题内模块专属字母前缀 + 序号"（如 `图K1`）。同页不得混用两种体系；全局字母占用由各课题 `TOPIC.md` 的图号表管理。字母稀缺方案（选修约定）：改用「图 模块号.序号」（图 5.2），课题间天然隔离——新课题默认采用这个方案。

### 4.4 教学脚注（硬规则）

每张教学图 `.chart-footnote` 必须含「示例数据，用于教学演示，非真实业务数据」；真实数据页用 `tag-real` + 来源声明。`.chart-card` 兼作非图表图示容器（mob-timeline 等），只有含 `.chart-title` 的才计为图表。

## 5. 工程约束

| 项 | 约定 |
|---|---|
| 技术栈 | 纯 HTML + `style.css` + vendor Chart.js（本地优先）：`design-system/vendor/chart.umd.min.js` + CDN fallback |
| 构建 | 无 |
| 交互 | 除 Chart.js 外零 JS；折叠只用原生 `details/summary` |
| 兼容 | Chrome/Safari 桌面 + 移动 |
| 预览 | `.claude/launch.json`：`python3 -m http.server 8844` |
| 校验 | `python3 tools/check_handbook.py`（0 FAIL 才能交付） |

## 6. 改此层的规则

- 新增组件：先进 `style.css` 并更新本表；
- 改类名/上下文：更新 `tools/check_handbook.py` 会被自动校验，不用再手动同步清单；
- 只引入新设计颜色不允许：全局 tokens 不改，课题强调色用 `<body data-topic>` 覆写 `--brand` 三值（选修）。
