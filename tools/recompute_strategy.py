#!/usr/bin/env python3
"""⑤ Part 4 放款决策表——从叙事线原始数据重算并对账。

数据流：
  data/deciles.csv  （③ 十分位表，叙事线的原始数据）
  data/strategy-params.json  （⑤ 的业务参数）
        ↓ 重算从低风险端逐档放款的"10 档面值账"
  05-strategy.html Part 4 表格
        ↓ 逐格比对

差一项就退出码 1。跑在 check_handbook.py 之外，
因为它针对的是"内容数字"而不是"结构"。

用法：python3 tools/recompute_strategy.py [--topic topics/credit-risk]
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def load_table(topic: Path) -> list[dict]:
    rows = []
    with open(topic / "data" / "deciles.csv", encoding="utf-8") as f:
        for r in csv.reader(f):
            if not r or r[0].startswith(("#", "decile")):
                continue
            rows.append({"decile": int(r[0]), "good": int(r[1]), "bad": int(r[2])})
    return rows


def recompute(deciles: list[dict], p: dict) -> list[dict]:
    """从低风险端放款：⑤ 第 k 档 = deciles 里的低 k 档（decile 10, 9, …）累计。"""
    out = []
    # 按低风险端排序：decile 10 最先放
    by_low = sorted(deciles, key=lambda d: -d["decile"])
    cum_bad, cum_n = 0, 0
    for k in range(1, 11):
        d = by_low[k - 1]
        cum_bad += d["bad"]
        cum_n += d["good"] + d["bad"]
        interest = cum_n * p["EAD_yuan"] * p["rate_annual"] / 10000
        ecl = cum_bad * p["EAD_yuan"] * p["LGD"] / 10000
        fixed = cum_n * p["fixed_cost_per_capita_yuan"] / 10000
        out.append({
            "k": k, "n": cum_n, "bad": cum_bad, "pd": cum_bad / cum_n,
            "interest": interest, "ecl": ecl, "fixed": fixed,
            "net": interest - ecl - fixed,
        })
    return out


def page_rows(page: Path) -> dict[int, dict]:
    text = page.read_text(encoding="utf-8")
    pat = re.compile(
        r'<tr[^>]*><td class="num"[^>]*>第 (\d+) 档[^<]*</td>'
        r'<td class="num"[^>]*>([0-9,]+)</td>'
        r'<td class="num"[^>]*>([0-9,]+)</td>'
        r'<td class="num"[^>]*>([0-9.]+)%</td>'
        r'<td class="num"[^>]*>([0-9,]+)</td>'
        r'<td class="num"[^>]*>([0-9,.]+)</td>'
        r'<td class="num"[^>]*>([0-9,.]+)</td>'
        r'<td class="num"[^>]*><strong>\+?([0-9,]+)</strong></td>')
    found = {}
    for m in pat.finditer(text):
        k, n, bad, pd_, inte, ecl, fx, net = m.groups()
        found[int(k)] = {
            "n": int(n.replace(",", "")),
            "bad": int(bad.replace(",", "")),
            "pd": float(pd_) / 100,
            "interest": float(inte.replace(",", "")),
            "ecl": float(ecl.replace(",", "")),
            "fixed": float(fx.replace(",", "")),
            "net": float(net.replace(",", "")),
        }
    return found


def close(a: float, b: float, *, pct=0.005, abs_=0.51) -> bool:
    return abs(a - b) <= max(abs_, abs(b) * pct)


def main(argv: list[str]) -> int:
    topic = REPO / "topics" / "credit-risk"
    for i, a in enumerate(argv):
        if a == "--topic" and i + 1 < len(argv):
            topic = Path(argv[i + 1])
            if not topic.is_absolute():
                topic = REPO / topic

    deciles = load_table(topic)
    params = json.loads((topic / "data" / "strategy-params.json").read_text(encoding="utf-8"))
    expect = recompute(deciles, params)
    html = topic / "manual" / "05-strategy.html"
    page = page_rows(html)

    n_fail = 0
    for e in expect:
        got = page.get(e["k"])
        if got is None:
            print(f"  ✗ 第 {e['k']} 档：05-strategy.html 里找不到这一行")
            n_fail += 1
            continue
        checks = [
            ("通过人数", e["n"], got["n"]),
            ("累计坏客户", e["bad"], got["bad"]),
            ("PD", e["pd"] * 100, got["pd"] * 100),
            ("利息", e["interest"], got["interest"]),
            ("ECL", e["ecl"], got["ecl"]),
            ("固定成本", e["fixed"], got["fixed"]),
            ("净利润", e["net"], got["net"]),
        ]
        for label, want, have in checks:
            if not close(have, want):
                unit = {"PD": "%", "通过人数": " 人", "累计坏客户": " 人"}.get(label, " 万")
                print(f"  ✗ 第 {e['k']} 档 {label}：页面 {have}{unit}，重算 {want:.2f}{unit}")
                n_fail += 1

    if n_fail:
        print(f"\n{n_fail} 处与重算不符——先改 data/*.csv（若有口径修正）或改 05 Part 4 表格")
        return 1

    zone = [r for r in expect if 1 <= r["k"] <= 10]
    limits = params["red_lines"]
    feasible = [r for r in expect
                if r["k"] >= limits["business_min_cutoff_decile"]
                and r["pd"] <= limits["pd_cap"]
                and limits["existing_balance_yi_yuan"]
                    + r["n"] * params["EAD_yuan"] / 1e8 <= limits["balance_cap_yi_yuan"]]
    if not feasible:
        print("  ✗ 教学约束没有留下可选档位")
        return 1
    fpk = max(feasible, key=lambda r: r["net"])
    kspk = 6
    print(f"✓ 10 档共 70 格全部与 data/deciles.csv + strategy-params.json 重算结果吻合")
    print(f"  教学约束内（第 {feasible[0]['k']}~{feasible[-1]['k']} 档）净利润峰值 = 第 {fpk['k']} 档 +{fpk['net']:.0f} 万")
    print(f"  KS 峰值切点 = 第 {kspk} 档 +{zone[kspk-1]['net']:.0f} 万（差 {fpk['net']-zone[kspk-1]['net']:.0f} 万）")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
