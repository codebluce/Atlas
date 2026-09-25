#!/usr/bin/env python3
"""
Atlas 手册结构校验器 —— 把 DESIGN-SPEC 的硬性约定变成可执行检查。

设计原则：
  1. 唯一事实来源是 style.css 与 DESIGN-SPEC.md，不是脚本作者的假设。
  2. 报告要能解释成因（例如"内联样式覆盖"），而不是只丢一个红叉。
  3. 零依赖（仅标准库），可在 CI 或本地秒级运行。

用法：
    python3 tools/check_handbook.py                    # 校验全部 topic
    python3 tools/check_handbook.py topics/credit-risk # 只校验一个 topic
退出码：有 FAIL 时为 1，仅 WARN 时为 0。
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}

# §7.7「泛化用：本手册的设计参数」——硬性数值约定
PARAMS = {
    "quiz": (5, 5),          # 自测题：恰好 5
    "pitfall": (3, 3),       # 坑：恰好 3
    "cheat_card": (8, 9),    # 速查卡：8~9
}

# §3.1 / 附 D 的必备槽位
REQUIRED_SLOTS = {
    "masthead": "页眉（breadcrumb + eyebrow + h1 + sub）",
    "local-nav": "局部导航",
    "checklist": "学习清单",
    "summary-box": "本节小结",
    "next-card": "下一步卡片",
    "page-footer": "页脚（左右双栏声明）",
}

# 已知的"另一套词汇"——用于把 FAIL 直接翻译成改法
KNOWN_ALIASES = {
    "quiz": "quiz-item", "quiz-q": "q-title", "quiz-a": "answer",
    "quiz-list": "(容器，删除，改用 .part 下并列的 .quiz-item)",
    "compare-card": "concept-card", "compare-cards": "concept-grid",
    "compare-hd": "c-name", "compare-ft": "c-mnemonic",
    "def-list": "concept-grid", "def": "concept-card", "def-term": "c-name",
    "chip": "c-en（.chip 只在 .order-strip 下定义，别处用不了）",
    "calc-steps": "(容器，删除，改用并列的 .method-step)",
    "calc-step": "method-step", "calc-step-num": "m-num", "calc-step-body": "m-body",
    "figure-note": "chart-footnote", "figure": "chart-card",
    "trap": "pitfall", "trap-num": "(并入 .pit-title 文案)", "trap-body": "(展开，无对应容器)",
    "row-hl": "hl",
    "formula": "calc-box", "formula-main": "calc-box 内的 .eq",
    "cheat-tag": "cc-name（正文改 .cc-detail）",
}


# ---------------------------------------------------------------- DOM

class Node:
    __slots__ = ("tag", "attrs", "children", "parent", "_text")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.children = []
        self.parent = parent
        self._text = []

    @property
    def classes(self) -> set[str]:
        return set((self.attrs.get("class") or "").split())

    @property
    def style(self) -> str:
        return self.attrs.get("style") or ""

    def text(self) -> str:
        out = list(self._text)
        for c in self.children:
            out.append(c.text())
        return re.sub(r"\s+", " ", "".join(out)).strip()

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()

    def find_all(self, cls: str):
        return [n for n in self.walk() if cls in n.classes]

    def find(self, cls: str):
        hits = self.find_all(cls)
        return hits[0] if hits else None

    def find_all_tag(self, tag: str):
        return [n for n in self.walk() if n.tag == tag]

    def find_tag(self, tag: str):
        hits = self.find_all_tag(tag)
        return hits[0] if hits else None


class Dom(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs), self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, dict(attrs), self.stack[-1]))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1]._text.append(data)


def parse(path: Path) -> Node:
    dom = Dom()
    dom.feed(path.read_text(encoding="utf-8"))
    return dom.root


# ---------------------------------------------------------------- 报告

class Report:
    def __init__(self):
        self.rows: list[tuple[str, str, str, str]] = []

    def add(self, level, scope, check, detail=""):
        self.rows.append((level, scope, check, detail))

    def count(self, level):
        return sum(1 for r in self.rows if r[0] == level)


# ---------------------------------------------------------------- 检查项

def parse_css(css_text: str) -> tuple[set[str], dict[str, set[tuple[frozenset, ...]]]]:
    """从 style.css 抽出 (全部类名, {类名: {允许的祖先链…}})。

    祖先链是"由外到内"的类集合序列，用于识别"语境类"：
    像 .chip 只写成 `.order-strip .chip`，单独用 .chip 就没有样式。
    某类只要有一条独立可用的规则，就不算语境类。
    """
    text = re.sub(r"/\*.*?\*/", "", css_text, flags=re.S)
    text = re.sub(r"@media[^{]*\{", "", text)

    defined: set[str] = set()
    standalone: set[str] = set()
    requires: dict[str, set[tuple]] = {}

    for block in re.finditer(r"([^{}]+)\{", text):
        for sel in block.group(1).split(","):
            sel = sel.strip().lstrip("}").strip()
            if not sel or sel.startswith("@"):
                continue
            parts = [set(re.findall(r"\.([a-zA-Z][\w-]*)", p)) for p in sel.split()]
            for cls in parts:
                defined |= cls
            # 最后一个带类的部分 = 规则的"主语"
            idx = max((i for i, c in enumerate(parts) if c), default=None)
            if idx is None:
                continue
            chain = tuple(frozenset(c) for c in parts[:idx] if c)
            for cls in parts[idx]:
                if chain:
                    requires.setdefault(cls, set()).add(chain)
                else:
                    standalone.add(cls)

    contextual = {c: s for c, s in requires.items() if c not in standalone}
    return defined, contextual


def has_ancestor_chain(node: Node, chain: tuple) -> bool:
    """祖先链由外到内匹配——链上的每一节可以由不同的祖先元素承担。"""
    need = list(reversed(chain))
    i = 0
    p = node.parent
    while p is not None and i < len(need):
        if need[i] <= p.classes:
            i += 1
        p = p.parent
    return i == len(need)


def check_rendering(page: Path, root: Node, defined: set[str],
                    contextual: dict[str, set[frozenset]], rep: Report):
    """A. 渲染完整性：用到的类必须真的能出样式。

    两类问题分开报：
      1. 悬空类——style.css 里根本没有这个类名。
      2. 语境类——类名存在，但只写成"祖先 .类"的复合选择器（如 .order-strip .chip）。
         这类类名换个祖先放就同样裸奔，必须逐处核对祖先。
    """
    used: dict[str, int] = {}
    for n in root.walk():
        for c in n.classes:
            used[c] = used.get(c, 0) + 1

    orphans = {c: n for c, n in used.items() if c not in defined}
    for cls, n in sorted(orphans.items(), key=lambda kv: -kv[1]):
        hint = KNOWN_ALIASES.get(cls)
        fix = f" → 应改用 .{hint}" if hint else ""
        rep.add("FAIL", page.name, f"渲染完整性 · .{cls}",
                f"{n} 处无样式定义（style.css 中不存在）{fix}")

    stray: list[tuple[str, bool]] = []
    for n in root.walk():
        for c in n.classes:
            allowed = contextual.get(c)
            if allowed and not any(has_ancestor_chain(n, chain) for chain in allowed):
                want = " 或 ".join(
                    " > ".join("." + "+.".join(sorted(seg)) for seg in chain)
                    for chain in sorted(allowed, key=len))
                # 作者写了内联样式 → 说明是"借名字当语义标签"，不是漏了样式，降级为 WARN
                stray.append((f".{c}（需祖先 {want}）", bool(n.style)))
    if stray:
        uniq: dict[tuple[str, bool], int] = {}
        for s in stray:
            uniq[s] = uniq.get(s, 0) + 1
        for (s, has_inline), n in uniq.items():
            level = "WARN" if has_inline else "FAIL"
            tail = "（该处有内联样式，属命名问题而非渲染缺失）" if has_inline else ""
            rep.add(level, page.name, "渲染完整性 · 语境类",
                    f"{n} 处用错祖先——{s}{tail}")

    if not orphans and not stray:
        rep.add("PASS", page.name, "渲染完整性", "所有 class 均有样式定义且在正确语境")


def check_params(page: Path, root: Node, rep: Report, *, allow_absent_pitfall: bool = False):
    """B. §7.7 硬参数：恰好 5 题 / 默认恰好 3 坑 / 8~9 速查卡。"""
    # 坑只数「三个坑」那一 Part 里的——否则会把别处复用 .pitfall 的中性卡片算进来
    pitfall_part = next((p for p in root.find_all("part")
                         if (h := p.find_tag("h2")) and "坑" in h.text()), None)
    n_pitfall = len(pitfall_part.find_all("pitfall")) if pitfall_part else 0
    n_total_pitfall = len(root.find_all("pitfall"))

    actual = {
        "quiz": len(root.find_all("quiz-item")) or len(root.find_all("quiz")),
        "pitfall": n_pitfall,
        "cheat_card": len(root.find_all("cheat-card")),
    }
    label = {"quiz": "自测题", "pitfall": "坑", "cheat_card": "速查卡"}

    for key, (lo, hi) in PARAMS.items():
        got, name = actual[key], label[key]
        if key == "pitfall" and got == 0 and allow_absent_pitfall:
            rep.add("PASS", page.name, "§7.7 坑", "本事件课题明确省略重复的坑卡")
            continue
        if lo <= got <= hi:
            detail = f"{got}（要求 {lo}~{hi}）"
            if key == "pitfall" and n_total_pitfall != n_pitfall:
                detail += f"；另有 {n_total_pitfall - n_pitfall} 处 .pitfall 在其它 Part（疑似中性卡片复用）"
            rep.add("PASS", page.name, f"§7.7 {name}", detail)
        elif got == 0:
            rep.add("FAIL", page.name, f"§7.7 {name}", f"0 个——完全缺失（要求 {lo}~{hi}）")
        else:
            rep.add("FAIL", page.name, f"§7.7 {name}", f"{got} 个，要求 {lo}~{hi}")



def check_skeleton(page: Path, root: Node, rep: Report):
    """C. §3.1 骨架：必备槽位 + Part1 痛点先行 + 口诀。"""
    missing = [f"{c}（{desc}）" for c, desc in REQUIRED_SLOTS.items()
               if not root.find(c)]
    if missing:
        for m in missing:
            rep.add("FAIL", page.name, "§3.1 骨架", f"缺少 {m}")
    else:
        rep.add("PASS", page.name, "§3.1 骨架", "13 段槽位齐全")

    parts = root.find_all("part")
    if parts:
        h2 = parts[0].find_tag("h2")
        head = h2.text() if h2 else ""
        if "痛点" in head:
            rep.add("PASS", page.name, "§7.6-iii 痛点先行", f"Part1 =「{head[:24]}」")
        else:
            rep.add("FAIL", page.name, "§7.6-iii 痛点先行",
                    f"Part1 不是痛点：「{head[:30] or '(无 h2)'}」")
    else:
        rep.add("FAIL", page.name, "§3.1 骨架", "没有任何 .part（正文未按 Part 组织）")

    if not root.find("mnemonic-line"):
        rep.add("WARN", page.name, "§7.1 记忆点", "小结缺 .mnemonic-line 口诀")
    else:
        rep.add("PASS", page.name, "§7.1 记忆点", "口诀存在")


def check_data_disclosure(page: Path, root: Node, rep: Report, source_driven: bool = False):
    """D. §7.4 / §6.1：真正的图表（含 chart-title）必须带脚注；
    教学页的脚注还须含"非真实业务数据"声明。

    注意：.chart-card 在本库中兼作非图表的图示容器（如 .mob-timeline），
    因此只把含 .chart-title 的卡片算作图表。
    """
    charts = [c for c in root.find_all("chart-card") if c.find("chart-title")]
    if not charts:
        rep.add("PASS" if source_driven else "WARN", page.name, "§6 图表",
                "事件驱动章节按需使用图表" if source_driven else "无教学图表（若本模块确实不含图表可忽略）")
        return

    is_real = root.find("tag-real") is not None
    footer = root.find("page-footer")
    footer_says = footer is not None and ("教学" in footer.text() or "非真实" in footer.text())

    no_note, no_disclaimer = [], []
    for i, c in enumerate(charts, 1):
        title = c.find("chart-title")
        label = (title.text() if title else "?")[:22]
        fn = c.find("chart-footnote")
        if fn is None:
            no_note.append(f"#{i}「{label}」")
        elif "非真实业务数据" not in fn.text() and not is_real:
            no_disclaimer.append(f"#{i}「{label}」")

    if no_note:
        rep.add("FAIL", page.name, "§7.4 图表脚注",
                f"{len(no_note)}/{len(charts)} 张图完全无脚注：{'、'.join(no_note)}")
    else:
        rep.add("PASS", page.name, "§7.4 图表脚注", f"{len(charts)} 张图均有脚注")

    if no_disclaimer:
        # §7.4 要求「图表脚注 + 页脚」双重声明；页脚已声明时降级为 WARN
        level = "WARN" if footer_says else "FAIL"
        tail = "（页脚已有声明，但 §7.4 要求双重声明）" if footer_says else ""
        rep.add(level, page.name, "§7.4 数据声明",
                f"{len(no_disclaimer)} 张教学图脚注未含「非真实业务数据」{tail}")
    elif not is_real:
        rep.add("PASS", page.name, "§7.4 数据声明", "教学图均声明了非真实业务数据")



def check_chart_numbering(page: Path, root: Node, rep: Report):
    """E. §6.3 / 附 B：图表标题须按「图X#」编号，同页不得混用编号体系。

    本库存在两种合法体系：
      · 前缀+序号（图K1、图 L1、图S1）——同页前缀必须唯一
      · 字母编号（图A、图B）——模块④教学版专用，字母本身即编号
    混用两种体系，或前缀+序号体系混用多个前缀，都判 FAIL。
    """
    titles = [t.text() for t in root.find_all("chart-title")]
    if not titles:
        return

    numbered, lettered, unnumbered = {}, [], []
    for t in titles:
        m = re.match(r"^图\s*([A-Z]+)\s*(\d*)", t)
        if not m:
            unnumbered.append(t[:26])
        elif m.group(2):
            numbered.setdefault(m.group(1), []).append(t[:20])
        else:
            lettered.append(m.group(1))

    for t in unnumbered:
        rep.add("WARN", page.name, "§6.3 图表编号", f"标题未按「图X#」编号：「{t}」")

    conventions = [c for c, v in (("前缀+序号", numbered), ("字母编号", lettered)) if v]
    if len(conventions) > 1:
        rep.add("FAIL", page.name, "§6.3 图表编号",
                f"同页混用编号体系：{conventions}")
    elif numbered and len(numbered) > 1:
        rep.add("FAIL", page.name, "§6.3 图表编号",
                f"前缀+序号体系混用多个前缀 {sorted(numbered)}")
    elif numbered:
        p = next(iter(numbered))
        rep.add("PASS", page.name, "§6.3 图表编号", f"前缀 {p}，共 {len(numbered[p])} 张")
    elif lettered:
        rep.add("PASS", page.name, "§6.3 图表编号",
                f"字母编号体系 {sorted(lettered)}，共 {len(lettered)} 张（模块④教学版特例）")


def check_narrative(topic_dir: Path, rep: Report, source_driven: bool = False):
    """G. §7.3 叙事线数字互通：跨模块共享的权威数字，任何模块引用都必须一致。

    登记表在 topics/<topic>/narrative.json。只查"数字 + 锚定词"这一对，
    不做全文数值扫描——这样既抓得住"450 基准分"这类错误引用，
    又不会把无关的巧合数字算进来。
    """
    reg_path = topic_dir / "narrative.json"
    if not reg_path.exists():
        rep.add("PASS" if source_driven else "WARN", "narrative.json", "§7.3 叙事线",
                "事件时间线与主体关系贯穿，无须虚构数字登记" if source_driven else "本 topic 未建立数字登记表")
        return

    try:
        entries = json.loads(reg_path.read_text(encoding="utf-8"))["narrative"]
    except (json.JSONDecodeError, KeyError) as e:
        rep.add("FAIL", "narrative.json", "§7.3 叙事线", f"登记表解析失败：{e}")
        return

    manual = topic_dir / "manual"
    bodies = {}
    for p in sorted(manual.glob("*.html")):
        t = p.read_text(encoding="utf-8")
        bodies[p.stem[:2]] = (p.name, re.sub(r"<script.*?</script>", "", t, flags=re.S))

    if not bodies:
        rep.add("WARN", "narrative.json", "§7.3 叙事线", "本课题暂无正文，跳过叙事线校验（正文成文后重新运行）")
        return

    def num(s):
        try:
            return float(s.replace(",", "").replace("，", ""))
        except ValueError:
            return None

    NUM = r"([0-9][0-9,，]*(?:\.[0-9]+)?)"

    def scan(entry, text, fname):
        """返回 (命中数, 不符列表)。两种模式：term=唯一术语；anchor+metric=实体锚定。"""
        want, accept = entry["value"], set(entry.get("accept", []))
        win = entry.get("window", 60)
        found = []

        if "term" in entry:
            t = re.escape(entry["term"])
            pats = [re.compile(rf"{t}\s*(?:[=＝:：]|\s)*{NUM}"),
                    re.compile(rf"{NUM}\s*(?:个|人)?\s*{t}")]
            for pat in pats:
                for m in pat.finditer(text):
                    found.append((num(m.group(1)), m))
        else:
            # 只查「锚点在前、指标在后」这个方向：中文叙述里"X 的 IV=0.563"是常态，
            # 反向匹配会把"复核线（IV=0.5）…本例中只有 X 落在该区域"这类误判成引用。
            a, k = entry["anchor"], entry["metric"]  # 两者都是正则，不要转义
            pats = [re.compile(rf"(?:{a})[\s\S]{{0,{win}}}?(?:{k})\s*(?:[=＝:：]|\s)*{NUM}")]
            for pat in pats:
                for m in pat.finditer(text):
                    found.append((num(m.group(1)), m))

        bad = []
        for got, m in found:
            if got is None or got == want or got in accept:
                continue
            ctx = re.sub(r"\s+", " ", text[max(0, m.start() - 34):m.end() + 16]).strip()
            bad.append(f"{fname}：「…{ctx}…」（读到 {got}）")
        return len(found), bad

    for e in entries:
        key = e.get("term") or f"{e['anchor']} 附近的 {e['metric']}"
        want = e["value"]
        offenders, checked = [], 0
        for mod, (fname, text) in bodies.items():
            if mod not in e.get("scope", list(bodies)):
                continue
            n, bad = scan(e, text, fname)
            checked += n
            offenders += bad

        label = f"§7.3 叙事线 · {e.get('term') or e['metric']}"
        if offenders:
            rep.add("FAIL", "narrative", label,
                    f"权威值 {want}，以下引用不符：" + "；".join(offenders))
        elif checked:
            extra = f"，另接受 {sorted(e['accept'])}" if e.get("accept") else ""
            rep.add("PASS", "narrative", label, f"{checked} 处引用均为 {want}{extra}")
        else:
            rep.add("WARN", "narrative", label, f"未匹配到「{key}」（scope {e.get('scope')}）")



def check_index(topic_dir: Path, rep: Report):
    """F. §2.3：index.html 与手册目录的双向引用必须同步。"""
    index = topic_dir / "index.html"
    manual = topic_dir / "manual"
    if not index.exists() or not manual.exists():
        rep.add("WARN", "index.html", "§2.3 状态同步", "缺 index.html 或 manual/ 目录")
        return

    root = parse(index)
    linked = {m.group(1) for n in root.walk()
              for m in [re.search(r"([\w-]+\.html)", n.attrs.get("href", ""))] if m}
    on_disk = {p.name for p in manual.glob("*.html")}
    on_disk.discard("index.html")

    dead = sorted(h for h in linked if h not in on_disk and re.match(r"\d{2}-", h))
    orphan = sorted(f for f in on_disk if f not in linked)

    if dead:
        rep.add("FAIL", "index.html", "§2.3 状态同步", f"链接指向不存在的文件：{dead}")
    if orphan:
        rep.add("FAIL", "index.html", "§2.3 状态同步", f"已成文但 index 未收录：{orphan}")
    if not dead and not orphan:
        rep.add("PASS", "index.html", "§2.3 状态同步", f"{len(on_disk)} 个模块双向一致")


def check_state_sync(topic_dir: Path, repo: Path, rep: Report):
    """H. 状态一致性：topic.json 是唯一事实源，四处必须对得上：
      1. topic.json 声明的文件 ↔ manual/ 实际存在的文件
      2. 课题 index.html 卡片状态 ↔ topic.json state
      3. 课题 index.html order-strip ↔ topic.json state
      4. 根 index.html 的进度数字 ↔ topic.json 统计
    """
    tj = topic_dir / "topic.json"
    if not tj.exists():
        rep.add("WARN", "topic.json", "状态一致性", "本课题无 topic.json，跳过状态一致性校验")
        return
    try:
        meta = json.loads(tj.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, KeyError) as e:
        rep.add("FAIL", "topic.json", "状态一致性", f"topic.json 解析失败：{e}")
        return

    # todo 是学习路线中的计划章节：可以登记文件名，但尚不应产生失效链接。
    # 一旦写出正文，需将其状态改成 current/done 并加入目录。
    required = {m["file"] for m in meta["modules"] if m["state"] != "todo"}
    on_disk = {f"manual/{p.name}" for p in (topic_dir / "manual").glob("*.html")}
    for f in sorted(required - on_disk):
        rep.add("FAIL", "topic.json", "状态一致性 · 磁盘", f"已上线模块文件不存在：{f}")
    for f in sorted(on_disk - required):
        rep.add("FAIL", "topic.json", "状态一致性 · 磁盘", f"正文已存在但未标记上线：{f}")
    if required == on_disk:
        rep.add("PASS", "topic.json", "状态一致性 · 磁盘", f"{len(on_disk)} 个已上线模块声明与实际相符")

    done = sum(1 for m in meta["modules"] if m["state"] in ("done", "current"))
    total = len(meta["modules"])

    root_index = repo / "index.html"
    if root_index.exists():
        rtxt = root_index.read_text(encoding="utf-8")
        pos = rtxt.find(f'topics/{meta["slug"]}/index.html')
        m2 = re.search(r"进行中 · (\d+) / (\d+)", rtxt[pos:pos + 900]) if pos >= 0 else None
        if not m2:
            rep.add("WARN", "index.html", "状态一致性 · 根目录进度", "根 index 中未找到该课题的进度数字")
        elif (int(m2.group(1)), int(m2.group(2))) != (done, total):
            rep.add("FAIL", "index.html", "状态一致性 · 根目录进度",
                    f"根 index 写的是 {m2.group(1)}/{m2.group(2)}，topic.json 是 {done}/{total}")
        else:
            rep.add("PASS", "index.html", "状态一致性 · 根目录进度", f"{done} / {total} 与 topic.json 一致")

    # 课题 index.html：每张模块卡的状态徽标与 topic.json state 一致
    t_index = topic_dir / "index.html"
    if t_index.exists():
        i_text = t_index.read_text(encoding="utf-8")
        seen_any = False
        for m in meta["modules"]:
            name = Path(m["file"]).name
            pos = i_text.find(name)
            if pos < 0:
                rep.add("FAIL", "index.html", "状态一致性 · 课题目录",
                        f"{name} 在 topic.json 声明但课题 index 没有对应卡片")
                continue
            seen_any = True
            seg = i_text[pos:pos + 600]  # 卡片结构：href 在前、card-top 的 tag 在后
            tag_m = re.search(r'<span class="tag[^"]*">([^<]+)</span>', seg)
            tag = tag_m.group(1) if tag_m else ""
            want_tag = {"done": "已完成", "current": "当前在学", "todo": "待更新"}.get(m["state"], "?")
            if want_tag not in tag:
                rep.add("FAIL", "index.html", "状态一致性 · 课题目录",
                        f"{name} 卡片未见「{want_tag}」徽标（读到「{tag[:24]}」；topic.json state={m['state']}）")
        if seen_any and not any(r[0] == "FAIL" and r[2].endswith("课题目录") for r in rep.rows):
            rep.add("PASS", "index.html", "状态一致性 · 课题目录", "所有卡片徽标与 topic.json state 一致")


# ---------------------------------------------------------------- 主流程

def main(argv: list[str]) -> int:
    verbose = "-v" in argv
    args = [a for a in argv[1:] if not a.startswith("-")]
    topics_root = REPO / "topics"
    targets = [Path(a) if Path(a).is_absolute() else REPO / a for a in args]
    if not targets:
        targets = sorted(p for p in topics_root.iterdir() if p.is_dir())

    css = REPO / "design-system" / "style.css"
    if not css.exists():
        print(f"找不到 {css}", file=sys.stderr)
        return 2
    defined, contextual = parse_css(css.read_text(encoding="utf-8"))

    rep = Report()
    for topic in targets:
        manual = topic / "manual"
        if not manual.is_dir():
            continue
        meta_path = topic / "topic.json"
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
        except json.JSONDecodeError:
            meta = {}  # check_state_sync reports malformed metadata below
        source_driven = meta.get("source_driven", False)
        allow_absent_pitfall = source_driven and "pitfall" in meta.get("optional_sections", [])
        for page in sorted(manual.glob("*.html")):
            root = parse(page)
            check_rendering(page, root, defined, contextual, rep)
            check_params(page, root, rep, allow_absent_pitfall=allow_absent_pitfall)
            check_skeleton(page, root, rep)
            check_data_disclosure(page, root, rep, source_driven)
            if source_driven:
                text = root.text()
                banned = [word for word in ("原文", "原笔记", "虚构演练", "海岸品牌", "澄芯", "星环", "榕城家庭", "松河基金", "青屿月调用")
                          if word in text]
                tables = root.find_all_tag("table")
                if banned or tables:
                    rep.add("FAIL", page.name, "事件驱动页", f"剩余来源转述/演练词：{banned}，宽表：{len(tables)}")
                else:
                    rep.add("PASS", page.name, "事件驱动页", "无虚构案例、来源转述词或宽表")
            check_chart_numbering(page, root, rep)
        check_index(topic, rep)
        check_narrative(topic, rep, source_driven)
        check_state_sync(topic, REPO, rep)

    icon = {"PASS": "  ok ", "WARN": " warn", "FAIL": " FAIL"}
    scope_w = max(len(r[1]) for r in rep.rows) if rep.rows else 10
    for level, scope, check, detail in rep.rows:
        if level == "PASS" and not verbose:
            continue
        print(f"[{icon[level]}] {scope:<{scope_w}}  {check:<22} {detail}")

    print()
    print(f"通过 {rep.count('PASS')} · 警告 {rep.count('WARN')} · 失败 {rep.count('FAIL')}")
    if rep.count("FAIL"):
        print("\nFAIL 项见上。加 -v 可同时打印通过项。")
    return 1 if rep.count("FAIL") else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
