#!/usr/bin/env python3
"""开新课题脚手架。

用法：
    python3 tools/new_topic.py <slug> [显示名]
    例：python3 tools/new_topic.py quant-trading "量化交易基础"

干四件事：
  1. 建目录 topics/<slug>/{manual, figures, data, reports}
  2. 生成 topics/<slug>/index.html（课题 hub 页骨架）
  3. 生成 topics/<slug>/narrative.json（叙事线登记表空壳）
  4. 把课题卡片注册到根 index.html

slug 规则：小写字母、数字、连字符（a-z0-9-），建议两段式如 quant-trading。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MARKER = "<!-- <new-topic-marker> -->"

TOPIC_INDEX = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{display} · 路线图</title>
<link rel="stylesheet" href="../../design-system/style.css">
</head>
<body>

<header class="masthead">
  <div class="container">
    <nav class="breadcrumb" aria-label="当前位置"><ol><li><a href="../../index.html">Atlas</a></li><li aria-current="page">{display}</li></ol></nav>
    <span class="eyebrow">🗂️ 课题目录 · 学习路线</span>
    <h1>{display}</h1>
    <p class="sub">{{用一句话写清这本手册的知识主线和学习方式}}</p>
  </div>
</header>

<div class="wrap">

  <div class="part" style="margin-top:36px;">
    <div class="part-head"><span class="part-num">MAP</span><h2>怎么用这本手册</h2></div>
    <p class="part-lede">本手册围绕 {{两条正交主线}} 组织。下面 {{N}} 个模块是知识地图的划分方式；点开的卡片是已经写好的正文。</p>
  </div>

  <div class="roadmap-grid">
    <!-- 模块卡片：写好的模块用 <a class="module-card linked" href="manual/NN-xxx.html">，待写用 <div class="module-card"> -->
  </div>

  <div class="order-strip">
    <strong style="margin-right:4px;">推荐学习顺序：</strong>
    <!-- 写好的 chip：<a class="chip done-chip" href="manual/NN-xxx.html">✓ N 主题</a>；待写：<span class="chip">N 主题</span> -->
  </div>

  <div class="callout info">
    <span class="label">从哪个模块切进去</span>
    {{写一句：为什么推荐先学模块X而不是第一个}}
  </div>

  <div class="callout warn">
    <span class="label">起点</span>
    {{这本手册的种子来源：文章/数据/报告的链接和致谢}}
  </div>

  <div class="page-footer">
    <span>{display} · 个人笔记，非机构内部资料</span>
    <span>已完成 → <!-- 写好的模块往这里加链接 --></span>
  </div>

</div>
</body>
</html>
"""

NARRATIVE_STUB = {
    "_about": "本课题的叙事线权威数字。改这里=改全库口径。",
    "_how": [
        "术语模式（term）：全库只有它指这个量（如「基准分」），数字与词相邻即校验。",
        "锚定模式（anchor + metric）：锚点在 metric 数字前后 window 字符内才算引用。",
        "只有跨模块反复引用、必须一致的数字才进登记表；一次性计算不写。",
    ],
    "narrative": [],
}

TOPIC_MD = """# {display} · 课题规格

> 层级：**课题级**。只属于 `{slug}`。全站视觉/工程见 [/design-system/DESIGN-SYSTEM.md](../../design-system/DESIGN-SYSTEM.md)；教学方法论见 [/design-system/PEDAGOGY.md](../../design-system/PEDAGOGY.md)。
> 状态的唯一事实来源是 [topic.json](topic.json)；叙事线权威数值在 [narrative.json](narrative.json)；可复算原始数据在 [data/](data/)。

## 1. 定位

- slug：`{slug}` · 原型：{{选 compute-model / law-rule / process-ops / concept-frame 之一，见 PEDAGOGY §4}}
- 种子：{{初始触发源：文章/数据/问题}}

## 2. 主线

{{至少 1 条、建议 2 条正交：横向对象生命周期 × 纵向方法论层次；找不到 2 条就先用 1 条}}

## 3. 模块表

{{4~10 个：# | 文件 | 主题 | 别名 | emoji | 状态}}

## 4. 叙事线

{{一句话写清元案例：哪个特征/数据/数字会被多个模块反复引用、反复重算；权威值落进 narrative.json}}

## 5. 数据源

{{教学构造数字 + 真实数据（若有）：来源格式、口径、脱敏方式}}

## 6. 类比池

{{新课题自己的物件隐喻，不抄别的课题的}}
"""

TOPIC_JSON = {
    "slug": None,
    "title": None,
    "prototype": "compute-model",
    "status": "active",
    "root_index_card": {"progress": "0 / ?", "tag": "tag-todo"},
    "modules": [],
}


def fail(msg: str) -> None:
    print(f"错误：{msg}", file=sys.stderr)
    sys.exit(2)


def register_root_index(slug: str, display: str, dry_run: bool) -> None:
    index = REPO / "index.html"
    text = index.read_text(encoding="utf-8")
    if MARKER not in text:
        fail(f"根 index.html 里找不到注册锚点：{MARKER}")
    card = (
        f'\n    <a class="module-card linked" href="topics/{slug}/index.html">\n'
        f'      <div class="card-top"><span class="kicker">{slug}</span>'
        f'<span class="tag tag-todo">进行中 · 0 / ? 模块</span></div>\n'
        f"      <h3>{display} →</h3>\n"
        f"      <p>{{一句钩子：这本手册从哪儿来、讲什么}}</p>\n    </a>\n"
    )
    text = text.replace(MARKER, card + "    " + MARKER, 1)
    if not dry_run:
        index.write_text(text, encoding="utf-8")


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    slug, display = argv[1], argv[2] if len(argv) > 2 else argv[1]
    dry_run = "--dry-run" in argv

    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        fail(f"slug 非法：{slug!r}。规则：小写的 a-z0-9 和连字符。")
    topic = REPO / "topics" / slug
    if topic.exists():
        fail(f"目录已存在：{topic}")

    print(f"创建课题 {slug}（{display}）{'【预演，不写盘】' if dry_run else ''}")

    if not dry_run:
        for d in ("manual", "figures", "data", "reports"):
            (topic / d).mkdir(parents=True)
            (topic / d / ".gitkeep").touch()
        (topic / "index.html").write_text(
            TOPIC_INDEX.format(slug=slug, display=display), encoding="utf-8")
        (topic / "narrative.json").write_text(
            json.dumps(NARRATIVE_STUB, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        topic_json = dict(TOPIC_JSON, slug=slug, title=display)
        (topic / "topic.json").write_text(
            json.dumps(topic_json, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        (topic / "TOPIC.md").write_text(
            TOPIC_MD.format(slug=slug, display=display), encoding="utf-8")
        register_root_index(slug, display, dry_run)

    print("  ✓ 目录 manual/ figures/ data/ reports/（含 .gitkeep）")
    print("  ✓ index.html（课题 hub 页骨架）")
    print("  ✓ topic.json（状态唯一事实源）")
    print("  ✓ TOPIC.md（课题规格：主线/模块表/叙事线/类比池）")
    print("  ✓ narrative.json（空壳）")
    print("  ✓ 根 index.html 注册卡片")
    print()
    print("下一步：")
    print("  1. 先写 topics/{}/TOPIC.md 定主线+模块表，再动正文".format(slug))
    print(f"  2. 照着 design-system/page-template.html 写第一个模块：")
    print(f"     cp design-system/page-template.html topics/{slug}/manual/01-xxx.html")
    print(f"  3. 写完按 spec-patch.md 走一遍")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
