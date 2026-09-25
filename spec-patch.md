# 写完一个模块之后，按这个顺序过一遍

有原始素材时先做「零读前知识测试」：逐段列出原文的时间线、主要参与者、数字口径与反证，写进按章连贯的正文；找没有读过原文的人只读手册，看是否能重述原文章的来龙去脉。卡片/算例/目录不能替代正文。检查每个解释性段落是否先交代一句总结，再展开材料并只划出少量关键事实或口径；手机窄屏不能为了排版牺牲原有信息。完成这一步后再运行下述工程清单。

每写完一个模块，做这五件事。前三步是改单一事实源，第 4 步让校验器反过来验前三步，第 5 步验收。

## 1. 改 `topics/<课题>/topic.json`（单一事实源）

- [ ] 把新模块加进 `modules`（`id` 两位数字、`file`、`title`、`alias`、`emoji`、`state`）
- [ ] `state` 取值：`done` / `current`（当前在学）/ `todo`
- [ ] 根 index 进度数字对应关系：`done`+`current`/`total`，先记一下

## 2. 同步课题 `topics/<课题>/index.html` 三处

- [ ] **roadmap 卡片**：待写 → 可点链接 `<a class="module-card linked">`，徽标 `tag-todo`/`tag-good`/`tag-current` 与 topic.json state 一致，标题末尾加 `→`
- [ ] **order-strip**：对应 chip 改 `<a class="chip done-chip" href="...">✓ N 主题</a>`（"当前在学"是 `<span class="chip current-chip">`）
- [ ] **页脚**：「已完成」列表追加链接

## 3. 同步根目录 `index.html` 的进度数字

- [ ] 该课题卡片「进行中 · 已写 / 总 模块」改成新数字

## 4. 检查叙事线

- [ ] 新模块引用了哪些已有数字？是不是都还是权威值？
- [ ] 新引入的数字，若会被以后模块反复引用，登记到 `topics/<课题>/narrative.json`（锚定词 + 值 + scope）

## 5. 跑校验

```bash
python3 tools/check_handbook.py
python3 tools/recompute_strategy.py   # 若本模块的表结构数字来自 data/*.csv
```

- [ ] 两条命令都通过才算写完这个模块
- [ ] 数据口径有变：先改 `topics/<课题>/data/*.csv` 和 `narrative.json`，再排 HTML
- [ ] 有 FAIL 先修 FAIL，再进入下一个模块

---

## 开新课题

1. `python3 tools/new_topic.py <slug> [显示名]`（例：`python3 tools/new_topic.py quant-trading "量化交易基础"`）
2. 先填 `topics/<slug>/TOPIC.md`：原型选型（计算/法规/流程/概念 4 型）+ 主线 + 模块表
3. 照 `design-system/page-template.html` 写第一个模块：`cp design-system/page-template.html topics/<slug>/manual/01-xxx.html`
4. 写完按上面 1~5 走一遍
