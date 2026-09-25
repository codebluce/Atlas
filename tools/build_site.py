#!/usr/bin/env python3
"""把 Atlas 仓库构建成可发布的静态站点（GitHub Pages）。

用法：
    python3 tools/build_site.py            # 输出到 _site/
    python3 tools/build_site.py --out dir  # 指定输出目录

做三件事：
  1. 复制可发布内容（根目录首页、design-system、topics、reviews）。
  2. 生成全站索引 catalog.html：课题 → 模块、状态、最近更新、全文搜索、文档。
     课题信息以 topics/<slug>/topic.json 为唯一事实源；没有 topic.json 的课题
     退化为读取课题 index.html 的标题。
  3. 生成 search-index.json 与 md.html（Markdown 在线阅读器），并把站内
     指向 .md 的链接改写到阅读器，避免浏览器直接下载原始文本。
"""
from __future__ import annotations

import html
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PUBLISH = ["index.html", "design-system", "topics", "reviews"]
IGNORE = shutil.ignore_patterns("__pycache__", ".DS_Store", ".gitkeep", "*.pyc")
STATE_TAG = {
    "done": ("已完成", "tag-good"),
    "current": ("当前在学", "tag-current"),
    "todo": ("待更新", "tag-todo"),
}


# ---------------------------------------------------------------- 工具函数

def git_date(path: Path) -> str:
    """文件最近一次提交的日期（YYYY-MM-DD）；不在 git 中则用修改时间。"""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path)],
            cwd=REPO, capture_output=True, text=True, check=True).stdout.strip()
        if out:
            return out
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")


def page_title(path: Path) -> str:
    m = re.search(r"<title>(.*?)</title>", path.read_text(encoding="utf-8"), re.S)
    return html.unescape(m.group(1)).strip() if m else path.stem


def plain_text(src: str) -> str:
    src = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", src, flags=re.S)
    src = re.sub(r"<[^>]+>", " ", src)
    return re.sub(r"\s+", " ", html.unescape(src)).strip()


def headings(src: str) -> list[str]:
    return [plain_text(h) for h in re.findall(r"<h2[^>]*>(.*?)</h2>", src, re.S)]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- 数据收集

def collect_topics() -> list[dict]:
    topics = []
    for d in sorted(p for p in (REPO / "topics").iterdir() if p.is_dir()):
        index = d / "index.html"
        if not index.exists():
            continue
        tj = d / "topic.json"
        meta = json.loads(tj.read_text(encoding="utf-8")) if tj.exists() else {}
        title = meta.get("title") or page_title(index).split("·")[0].strip()
        modules = []
        for m in sorted(meta.get("modules", []), key=lambda m: m.get("order", 0)):
            f = d / m["file"]
            live = m.get("state") != "todo" and f.exists()
            modules.append({
                **m,
                "href": f"topics/{d.name}/{m['file']}",
                "live": live,
                "updated": git_date(f) if f.exists() else "",
            })
        extras = [p for p in sorted(d.glob("*.html")) if p.name != "index.html"]
        done = sum(1 for m in modules if m.get("state") in ("done", "current"))
        topics.append({
            "slug": d.name,
            "title": title,
            "status": meta.get("status", "planning" if not modules else "active"),
            "href": f"topics/{d.name}/index.html",
            "modules": modules,
            "extras": [{"title": page_title(p), "href": f"topics/{d.name}/{p.name}",
                        "updated": git_date(p)} for p in extras],
            "progress": f"{done} / {len(modules)}" if modules else "尚无正文",
            "updated": max([m["updated"] for m in modules if m["updated"]] +
                           [git_date(index)]),
        })
    return topics


def collect_docs() -> list[dict]:
    docs = []
    for p in sorted(REPO.glob("design-system/*.md")) + sorted(REPO.glob("topics/*/*.md")) \
            + sorted(REPO.glob("reviews/*.md")):
        rel = p.relative_to(REPO).as_posix()
        first = next((l.lstrip("# ").strip() for l in p.read_text(encoding="utf-8").splitlines()
                      if l.startswith("#")), p.stem)
        docs.append({"title": first, "path": rel, "updated": git_date(p)})
    return docs


def collect_search(topics: list[dict]) -> list[dict]:
    pages = []
    for t in topics:
        targets = [(t["href"], t["title"] + " · 目录")]
        targets += [(m["href"], None) for m in t["modules"] if m["live"]]
        targets += [(e["href"], None) for e in t["extras"]]
        for href, forced in targets:
            src = (REPO / href).read_text(encoding="utf-8")
            pages.append({
                "topic": t["title"],
                "title": forced or page_title(REPO / href),
                "href": href,
                "headings": headings(src),
                "text": plain_text(src),
            })
    return pages


# ---------------------------------------------------------------- 页面生成

CATALOG_CSS = """
.search-box{width:100%;padding:14px 18px;font-size:16px;border:1.5px solid var(--line);
  border-radius:12px;background:var(--paper);color:var(--ink);font-family:inherit;
  box-shadow:var(--shadow);outline:none;box-sizing:border-box}
.search-box:focus{border-color:var(--brand)}
.hits{margin-top:14px}
.hit{display:block;background:var(--paper);border:1px solid var(--line);border-radius:12px;
  padding:12px 16px;margin-bottom:10px;border-bottom:1px solid var(--line)}
.hit .h-meta{font-size:12px;color:var(--ink-faint)}
.hit .h-title{font-weight:600;color:var(--ink);margin:2px 0}
.hit .h-snip{font-size:14px;color:var(--ink-soft)}
.hit mark{background:var(--brand-bg);color:var(--ink);padding:0 1px}
.stat-row{display:flex;flex-wrap:wrap;gap:12px;margin:18px 0 6px}
.stat{flex:1 1 120px;background:var(--paper);border:1px solid var(--line);border-radius:12px;
  padding:12px 16px}
.stat b{display:block;font-size:24px;color:var(--brand-dark)}
.stat span{font-size:13px;color:var(--ink-faint)}
.tbl td.muted{color:var(--ink-faint)}
.topbar{display:flex;gap:18px;flex-wrap:wrap;font-size:14px;margin-top:10px}
"""


def render_catalog(topics: list[dict], docs: list[dict], built: str) -> str:
    n_live = sum(1 for t in topics for m in t["modules"] if m["live"])
    recent = sorted(
        [(m["updated"], t["title"], m["title"], m["href"]) for t in topics
         for m in t["modules"] if m["live"]] +
        [(e["updated"], t["title"], e["title"].split("|")[0].strip(), e["href"])
         for t in topics for e in t["extras"]],
        reverse=True)[:8]

    sections = []
    for t in topics:
        rows = []
        for m in t["modules"]:
            label, cls = STATE_TAG.get(m.get("state"), ("?", "tag-info"))
            name = f"{m.get('emoji', '')} {esc(m['title'])}"
            if m.get("note"):
                name += f" <span class=\"tag tag-info\">{esc(m['note'])}</span>"
            link = f"<a href=\"{m['href']}\">{name}</a>" if m["live"] else name
            rows.append(f"<tr><td>{esc(m.get('id', ''))}</td><td>{link}</td>"
                        f"<td><span class=\"tag {cls}\">{label}</span></td>"
                        f"<td class=\"muted\">{m['updated'] or '—'}</td></tr>")
        for e in t["extras"]:
            rows.append(f"<tr><td>附</td><td><a href=\"{e['href']}\">📎 "
                        f"{esc(e['title'].split('|')[0].strip())}</a></td>"
                        f"<td><span class=\"tag tag-info\">伴读</span></td>"
                        f"<td class=\"muted\">{e['updated']}</td></tr>")
        body = (f"<div class=\"table-scroll\"><table class=\"tbl\"><thead><tr><th>#</th>"
                f"<th>模块</th><th>状态</th><th>更新</th></tr></thead><tbody>"
                f"{''.join(rows)}</tbody></table></div>") if rows else \
            "<p class=\"part-lede\">课题入口已创建，章节尚在规划。</p>"
        sections.append(
            f"<div class=\"part\" id=\"t-{t['slug']}\"><div class=\"part-head\">"
            f"<span class=\"part-num\">{esc(t['progress'])}</span>"
            f"<h2><a href=\"{t['href']}\">{esc(t['title'])} →</a></h2></div>"
            f"<p class=\"part-lede\">最近更新 {t['updated']} · "
            f"<a href=\"{t['href']}\">进入课题目录</a></p>{body}</div>")

    recent_html = "".join(
        f"<tr><td class=\"muted\">{d}</td><td>{esc(tt)}</td><td><a href=\"{h}\">{esc(mt)}</a></td></tr>"
        for d, tt, mt, h in recent)
    docs_html = "".join(
        f"<tr><td><a href=\"md.html?f={esc(d['path'])}\">{esc(d['title'])}</a></td>"
        f"<td class=\"muted\">{esc(d['path'])}</td><td class=\"muted\">{d['updated']}</td></tr>"
        for d in docs)
    toc = " · ".join(f"<a href=\"#t-{t['slug']}\">{esc(t['title'])}</a>" for t in topics)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Atlas 全站索引</title>
<link rel="stylesheet" href="design-system/style.css">
<style>{CATALOG_CSS}</style>
</head>
<body>
<header class="masthead"><div class="container">
  <nav class="breadcrumb" aria-label="当前位置"><ol><li><a href="index.html">Atlas</a></li><li aria-current="page">全站索引</li></ol></nav>
  <span class="eyebrow">🔎 所有课题 · 所有模块 · 一处检索</span>
  <h1>全站索引</h1>
  <p class="sub">按课题列出每个模块的状态与更新时间；上方搜索框可检索全部正文。</p>
  <div class="topbar">{toc} · <a href="#recent">最近更新</a> · <a href="#docs">文档</a></div>
</div></header>
<div class="wrap">
  <div class="stat-row">
    <div class="stat"><b>{len(topics)}</b><span>课题</span></div>
    <div class="stat"><b>{n_live}</b><span>已上线模块</span></div>
    <div class="stat"><b>{len(docs)}</b><span>规范与报告</span></div>
    <div class="stat"><b>{built[:10]}</b><span>站点构建日期</span></div>
  </div>
  <div class="part" style="margin-top:24px"><div class="part-head"><span class="part-num">搜索</span><h2>全文检索</h2></div>
    <input id="q" class="search-box" type="search" placeholder="输入关键词，如 VIE、37 号文、Vintage、WOE…" autocomplete="off">
    <div id="hits" class="hits"></div>
  </div>
  {''.join(sections)}
  <div class="part" id="recent"><div class="part-head"><span class="part-num">NEW</span><h2>最近更新</h2></div>
    <div class="table-scroll"><table class="tbl"><thead><tr><th>日期</th><th>课题</th><th>页面</th></tr></thead><tbody>{recent_html}</tbody></table></div>
  </div>
  <div class="part" id="docs"><div class="part-head"><span class="part-num">DOCS</span><h2>规范、课题说明与分析报告</h2></div>
    <div class="table-scroll"><table class="tbl"><thead><tr><th>文档</th><th>路径</th><th>更新</th></tr></thead><tbody>{docs_html}</tbody></table></div>
  </div>
  <div class="page-footer"><span>Atlas · 全站索引由 tools/build_site.py 自动生成</span><span>构建于 {built} · <a href="index.html">返回首页</a></span></div>
</div>
<script>
(function(){{
  var box=document.getElementById('q'), out=document.getElementById('hits'), data=null;
  function esc(s){{return s.replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}});}}
  function load(cb){{ if(data) return cb();
    fetch('search-index.json').then(function(r){{return r.json();}}).then(function(j){{data=j;cb();}})
      .catch(function(){{out.innerHTML='<p class="part-lede">索引加载失败，请刷新重试。</p>';}}); }}
  function run(){{
    var q=box.value.trim(); if(!q){{out.innerHTML='';return;}}
    load(function(){{
      var terms=q.toLowerCase().split(/\\s+/), res=[];
      data.forEach(function(p){{
        var hay=(p.title+' '+p.headings.join(' ')+' '+p.text).toLowerCase(), score=0, ok=true;
        terms.forEach(function(t){{ var i=hay.indexOf(t); if(i<0) ok=false;
          score+=(p.title.toLowerCase().indexOf(t)>=0?10:0)+(p.headings.join(' ').toLowerCase().indexOf(t)>=0?4:0)+hay.split(t).length-1; }});
        if(!ok) return;
        var i=p.text.toLowerCase().indexOf(terms[0]), s=Math.max(0,i-40);
        var snip=(s>0?'…':'')+p.text.slice(s,s+120)+'…';
        var h=esc(snip); terms.forEach(function(t){{ if(!t) return;
          h=h.replace(new RegExp(t.replace(/[.*+?^${{}}()|[\\]\\\\]/g,'\\\\$&'),'gi'),function(m){{return '<mark>'+m+'</mark>';}}); }});
        res.push({{p:p,score:score,snip:h}});
      }});
      res.sort(function(a,b){{return b.score-a.score;}});
      out.innerHTML=res.length?res.slice(0,20).map(function(r){{
        return '<a class="hit" href="'+r.p.href+'"><div class="h-meta">'+esc(r.p.topic)+'</div><div class="h-title">'+esc(r.p.title)+'</div><div class="h-snip">'+r.snip+'</div></a>';
      }}).join(''):'<p class="part-lede">没有找到包含“'+esc(q)+'”的页面。</p>';
    }});
  }}
  var timer; box.addEventListener('input',function(){{clearTimeout(timer);timer=setTimeout(run,150);}});
  var qs=new URLSearchParams(location.search).get('q'); if(qs){{box.value=qs;run();}}
}})();
</script>
</body>
</html>
"""


MD_VIEWER = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Atlas 文档阅读</title>
<link rel="stylesheet" href="design-system/style.css">
<style>
.md-body{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);
  padding:24px 28px;margin-top:28px;box-shadow:var(--shadow);overflow-wrap:anywhere}
.md-body img{max-width:100%}
.md-body table{border-collapse:collapse;display:block;overflow-x:auto}
.md-body th,.md-body td{border:1px solid var(--line);padding:6px 10px}
.md-body pre{background:var(--line-soft);padding:12px;border-radius:8px;overflow-x:auto}
@media (max-width:600px){.md-body{padding:16px}}
</style>
</head>
<body>
<header class="masthead"><div class="container">
  <nav class="breadcrumb" aria-label="当前位置"><ol><li><a href="index.html">Atlas</a></li><li><a href="catalog.html#docs">文档目录</a></li><li id="doc-topic" hidden></li><li id="crumb" aria-current="page">文档</li></ol></nav>
  <h1 id="title">文档</h1>
</div></header>
<div class="wrap"><div id="doc" class="md-body">加载中…</div>
<div class="page-footer"><span>Atlas · Markdown 文档阅读器</span><span><a id="raw" href="#">查看原文</a> · <a href="catalog.html">全站索引</a></span></div></div>
<script src="design-system/vendor/marked.min.js"></script>
<script src="design-system/vendor/purify.min.js"></script>
<script>
(function(){
  /* DOC_BREADCRUMB_METADATA */
  var f=new URLSearchParams(location.search).get('f')||'';
  var doc=document.getElementById('doc');
  if(!/^[\\w\\-\\/\\u4e00-\\u9fa5.]+\\.md$/.test(f)||f.indexOf('..')>=0){doc.textContent='无效的文档路径。';return;}
  var entry=docsMeta[f], crumb=document.getElementById('crumb');
  crumb.textContent=entry?entry.title:f;
  if(entry&&entry.topic&&topicsMeta[entry.topic]){
    var parent=document.getElementById('doc-topic'), link=document.createElement('a');
    link.href='topics/'+entry.topic+'/index.html';
    link.textContent=topicsMeta[entry.topic]; parent.appendChild(link); parent.hidden=false;
  }
  document.getElementById('raw').href=f;
  var base=f.replace(/[^\\/]*$/,'');
  fetch(f).then(function(r){if(!r.ok)throw 0;return r.text();}).then(function(t){
    doc.innerHTML=DOMPurify.sanitize(marked.parse(t));
    var h=doc.querySelector('h1'); if(h){document.getElementById('title').textContent=h.textContent;document.title=h.textContent+' | Atlas';crumb.textContent=h.textContent;h.remove();}
    doc.querySelectorAll('a[href],img[src]').forEach(function(el){
      var attr=el.tagName==='A'?'href':'src', v=el.getAttribute(attr);
      if(/^(https?:|#|mailto:|\\/)/.test(v)) return;
      var p=base+v;
      if(el.tagName==='A'&&/\\.md(#.*)?$/.test(v)) el.setAttribute(attr,'md.html?f='+p.replace(/#.*$/,''));
      else el.setAttribute(attr,p);
    });
  }).catch(function(){doc.textContent='文档加载失败：'+f;});
})();
</script>
</body>
</html>
"""


def render_md_viewer(topics: list[dict], docs: list[dict]) -> str:
    """在静态阅读器中登记文档标题与所属课题，不通过路径猜页面层级。"""
    index = {d["path"]: {
        "title": d["title"],
        "topic": d["path"].split("/")[1] if d["path"].startswith("topics/") else None,
    } for d in docs}
    titles = {t["slug"]: t["title"] for t in topics}
    # JSON is embedded into a <script> tag, so escape '<' to avoid closing the tag.
    metadata = ("var docsMeta=" + json.dumps(index, ensure_ascii=False) + ";\n"
                "  var topicsMeta=" + json.dumps(titles, ensure_ascii=False) + ";")
    return MD_VIEWER.replace("/* DOC_BREADCRUMB_METADATA */", metadata.replace("<", "\\u003c"))


def rewrite_md_links(site: Path) -> int:
    """站内 <a href="xxx.md"> → md.html?f=<站点根相对路径>。"""
    n = 0
    for page in site.rglob("*.html"):
        if page.name == "md.html":
            continue
        src = page.read_text(encoding="utf-8")
        rel_dir = page.parent.relative_to(site)
        up = "../" * len(rel_dir.parts)

        def sub(m: re.Match) -> str:
            nonlocal n
            target = m.group(2)
            if re.match(r"^(https?:|/|#)", target):
                return m.group(0)
            resolved = os.path.normpath((rel_dir / target).as_posix()).replace(os.sep, "/")
            if resolved.startswith(".."):
                return m.group(0)
            n += 1
            return f'{m.group(1)}{up}md.html?f={resolved}"'

        new = re.sub(r'(href=["\'])([^"\'#?]+\.md)["\']', sub, src)
        if new != src:
            page.write_text(new, encoding="utf-8")
    return n


def inject_catalog_link(site: Path) -> None:
    """在首页 masthead 下加入全站索引入口（只改构建产物，不改源文件）。"""
    idx = site / "index.html"
    src = idx.read_text(encoding="utf-8")
    link = ('<p class="sub" style="margin-top:10px"><a href="catalog.html">🔎 全站索引与全文搜索 →</a></p>')
    src = src.replace("</p>\n  </div>\n</header>", "</p>\n    " + link + "\n  </div>\n</header>", 1)
    idx.write_text(src, encoding="utf-8")


def adapt_published_template(site: Path) -> None:
    """模板源文件按 topics/<slug>/manual/ 写；发布目录位于 design-system/。"""
    page = site / "design-system" / "page-template.html"
    src = page.read_text(encoding="utf-8")
    src = src.replace('href="../../../design-system/style.css"', 'href="style.css"')
    src = src.replace('src="../../../design-system/vendor/chart.umd.min.js"',
                      'src="vendor/chart.umd.min.js"')
    src = src.replace(
        '<nav class="breadcrumb" aria-label="当前位置"><ol><li><a href="../../../index.html">Atlas</a></li><li><a href="../index.html">{{课题名}}</a></li><li aria-current="page">模块N · {{主题}}</li></ol></nav>',
        '<nav class="breadcrumb" aria-label="当前位置"><ol><li><a href="../index.html">Atlas</a></li><li><a href="../catalog.html#docs">文档目录</a></li><li aria-current="page">章节页面模板</li></ol></nav>',
    )
    page.write_text(src, encoding="utf-8")


# ---------------------------------------------------------------- 主流程

def main(argv: list[str]) -> int:
    out = REPO / "_site"
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1]).resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    for item in PUBLISH:
        src = REPO / item
        if src.is_dir():
            shutil.copytree(src, out / item, ignore=IGNORE)
        elif src.exists():
            shutil.copy2(src, out / item)

    topics = collect_topics()
    docs = collect_docs()
    built = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    (out / "catalog.html").write_text(render_catalog(topics, docs, built), encoding="utf-8")
    (out / "md.html").write_text(render_md_viewer(topics, docs), encoding="utf-8")
    (out / "search-index.json").write_text(
        json.dumps(collect_search(topics), ensure_ascii=False), encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    n_md = rewrite_md_links(out)
    inject_catalog_link(out)
    adapt_published_template(out)

    n_pages = sum(1 for _ in out.rglob("*.html"))
    print(f"已构建 {out.relative_to(REPO) if out.is_relative_to(REPO) else out}："
          f"{len(topics)} 个课题 · {n_pages} 个页面 · {len(docs)} 份文档 · 改写 {n_md} 处 .md 链接")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
