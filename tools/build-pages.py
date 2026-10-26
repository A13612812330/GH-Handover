# -*- coding: utf-8 -*-
"""生成 GH-Handover 的 GitHub Pages 门户页（仓库根 index.html）。

用法：
    python tools/build-pages.py            # 校验仓库状态后生成
    python tools/build-pages.py --no-verify  # 跳过远端校验（离线时用）
    python tools/build-pages.py --dry-run    # 只打印，不写文件

原则：
1. **对外脱敏**：只列公开仓库与公开可访问的信息。
   内部后台地址（zx.*、coop.*、钉钉文档）一律不出现 —— 那份清单留在本机看板里。
2. **防止漂移**：生成前用 API 校验每个仓库存在且确实为 MIT，任一不符合就报错退出。
   这样仓库改名/删除/掉许可证时，构建会立刻失败，而不是页面继续撒谎。
3. **幂等**：页内不写生成时间，重跑结果一致。
"""

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

ORG = "GHZS-Project"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.html")

# (仓库名, 展示名, 一句话说明, 形态徽章, 徽章类型, 技术标签)
PROJECTS = [
    (
        "GH-NewGameWIki",
        "NewGameWiki",
        "游戏资讯、活动与排期管理。8 个平台采集 → SQLite → 后台，自带 AI_AGENT_SETUP.md，把提示词发给 Agent 就能自行复刻。",
        "需装依赖",
        "deps",
        ["Node", "SQLite", "React"],
    ),
    (
        "GH-GameNews",
        "GameNews",
        "资讯采集 → 今日简讯 → 日报/周报海报 → 飞书投递，对接 7 个平台并含定时调度。公开版已移除人工编辑器。",
        "需装依赖",
        "deps",
        ["Node", "SQLite", "React"],
    ),
    (
        "GH-Gamehub",
        "GameHub",
        "单机游戏聚合站：游戏、MOD、存档、修改器与模拟器配置，共 6 个页面。内置搜索与内容库同步。",
        "需装依赖",
        "deps",
        ["Node", "Express", "静态前端"],
    ),
    (
        "GH-GameGather-APP",
        "GameGather APP",
        "PC 与手游情报站 + 资源索引 + aria2 下载的 Electron 桌面成品。Release 提供整包，解压后双击即可运行。",
        "Release 成品",
        "ready",
        ["Electron", "Node"],
    ),
    (
        "GH-GameGather-UPSTREAM",
        "GameGather UPSTREAM",
        "上面那个 App 的配套数据服务：Express 服务 + 15 个抓取器 + 索引快照。没有它，App 只能看离线数据。",
        "需装依赖",
        "deps",
        ["Node", "Express", "抓取器"],
    ),
    (
        "GH-Game-Puton",
        "Game Puton",
        "Windows 游戏后台上架批量导入工具（Electron），含交接文档、操作手册与字段映射表。仓库只含源码，成品需自行打包。",
        "需自行打包",
        "warn",
        ["Electron", "Node"],
    ),
    (
        "GH-WeeklyReport",
        "WeeklyReport",
        "Excel 周报分析：当周、跨周汇总、收益汇总与趋势图，默认 8787 端口。零第三方依赖，克隆即跑。",
        "零依赖",
        "ready",
        ["Node", "零依赖"],
    ),
    (
        "GH-GameSearch",
        "GameSearch",
        "Android 游戏信息查询 App（Kotlin）：通过 WebView 登录后台，按账号权限读取游戏信息与详情。成品 APK 在 dist/。",
        "成品 APK",
        "ready",
        ["Kotlin", "Android"],
    ),
    (
        "GH-CloudGame",
        "CloudGame",
        "端游云游戏三源周报可复刻工程：脚本、词库、口径与 4 期产出齐全。交给 AI 读 AGENT.md，即可跑出同款 Excel 与看板。",
        "开箱即用",
        "ready",
        ["Python", "pandas", "HTML"],
    ),
    (
        "GH-KomoSkill",
        "KomoSkill",
        "AI 协作工作法技能包：六阶段门禁 + 证据纪律 + 防失忆，Codex、WorkBuddy 与 Claude 通用。不是业务工具，是方法。",
        "脚本即用",
        "ready",
        ["Python", "Markdown"],
    ),
]

GROUPS = [
    ("站点与数据", "SITES & DATA", "可独立部署的服务端与桌面端应用", 0, 5),
    ("工具与方法", "TOOLCHAIN & METHOD", "日常运营工具、数据流水线与协作方法", 5, 10),
]

TOKEN = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()


def api(path):
    req = urllib.request.Request("https://api.github.com" + path)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "build-pages")
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode())


def verify():
    """任何仓库缺失或不再是 MIT，直接失败 —— 避免页面与事实脱节。"""
    bad = []
    for repo, name, *_ in PROJECTS:
        try:
            d = api("/repos/%s/%s" % (ORG, repo))
        except urllib.error.HTTPError as e:
            bad.append("%s: HTTP %s" % (repo, e.code))
            continue
        if d.get("private"):
            bad.append("%s: 变成私有" % repo)
        lic = (d.get("license") or {}).get("spdx_id")
        if lic != "MIT":
            bad.append("%s: license=%s" % (repo, lic))
        print("  %-26s %-6s %-10s %s KB" % (repo, "OK", lic, d.get("size")))
    if bad:
        print("\n校验失败：")
        for b in bad:
            print("  -", b)
        sys.exit(1)
    print("  校验通过：%d 个仓库均公开且为 MIT\n" % len(PROJECTS))


def esc(s):
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )


def cards(start, end):
    out = []
    for i in range(start, end):
        repo, name, desc, badge, btype, tags = PROJECTS[i]
        tag_html = "".join('<span class="tag">%s</span>' % esc(t) for t in tags)
        out.append(
            '<article class="card" data-idx="%02d">'
            '<div class="card-top">'
            '<span class="num">%02d</span>'
            '<h3>%s</h3>'
            '<span class="badge b-%s">%s</span>'
            "</div>"
            '<p class="desc">%s</p>'
            '<div class="tags">%s<span class="tag lic">MIT</span></div>'
            '<div class="links">'
            '<a class="chip" href="https://github.com/%s/%s" target="_blank" rel="noopener">'
            "<span>打开仓库</span><span class=\"arw\">&#8599;</span></a>"
            "</div>"
            "</article>"
            % (i + 1, i + 1, esc(name), btype, esc(badge), esc(desc), tag_html, ORG, repo)
        )
    return "".join(out)


def build():
    sections = []
    for gi, (label, en, desc, s, e) in enumerate(GROUPS):
        sections.append(
            '<section class="group" id="g%d">'
            '<div class="group-h">'
            '<h2>%s<span class="group-en">%s</span></h2>'
            '<p class="group-d" data-total="%d"><span class="gd-text">%s · %d 个</span></p>'
            "</div>"
            '<div class="grid">%s</div>'
            "</section>" % (gi, esc(label), esc(en), e - s, esc(desc), e - s, cards(s, e))
        )

    nav = "".join(
        '<a class="navbtn" href="#g%d">%s<span class="navn">%d</span></a>' % (i, esc(g[0]), g[4] - g[3])
        for i, g in enumerate(GROUPS)
    )

    return TEMPLATE.replace("@@NAV@@", nav).replace("@@SECTIONS@@", "".join(sections)).replace(
        "@@N_REPO@@", str(len(PROJECTS))
    ).replace("@@N_GROUP@@", str(len(GROUPS)))


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="GHZS-Project 开源仓库总览：11 个可独立运行的项目，全部 MIT 许可。">
<title>GHZS-Project · 开源项目总览</title>
<style>
:root{
  --bg:#f5f6f8;--panel:#fff;--line:#e4e6ea;--line-2:#eff1f4;
  --ink:#15181d;--ink-2:#5b6472;--ink-3:#8a93a1;
  --blue:#2563eb;--teal:#0f766e;--violet:#7c3aed;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-size:14px;line-height:1.65;
  font-family:"Segoe UI","PingFang SC","Microsoft YaHei",system-ui,-apple-system,sans-serif;
  -webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding:0 28px 72px}
.wrap-top{padding-bottom:0}

.hero{padding:52px 0 22px;border-bottom:1px solid var(--line)}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ink-3);font-weight:600;margin-bottom:14px}
.eyebrow::before{content:"";width:22px;height:2px;background:var(--blue);display:block}
h1{font-size:34px;line-height:1.25;letter-spacing:-.02em;font-weight:700}
h1 em{font-style:normal;color:var(--blue)}
.sub{margin-top:11px;color:var(--ink-2);font-size:14.5px;max-width:660px}
.stats{display:flex;gap:38px;margin-top:24px;flex-wrap:wrap}
.stat b{display:block;font-size:25px;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.stat span{font-size:12px;color:var(--ink-3)}
.stat+.stat{border-left:1px solid var(--line);padding-left:38px}

.bar{position:sticky;top:0;z-index:20;background:rgba(245,246,248,.93);backdrop-filter:blur(10px);
  border-bottom:1px solid var(--line);padding:13px 0;margin-bottom:4px}
.bar-in{max-width:1180px;margin:0 auto;padding:0 28px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.search{position:relative;flex:1;min-width:210px;max-width:330px}
.search input{width:100%;height:37px;border:1px solid var(--line);border-radius:9px;background:var(--panel);
  padding:0 12px 0 35px;font-size:13.5px;font-family:inherit;color:var(--ink);outline:none;
  transition:border-color .15s,box-shadow .15s}
.search input:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(37,99,235,.1)}
.search svg{position:absolute;left:12px;top:11px;width:15px;height:15px;stroke:var(--ink-3);fill:none;stroke-width:1.8}
.navbtn{display:inline-flex;align-items:center;gap:7px;height:33px;padding:0 11px;border:1px solid var(--line);
  border-radius:9px;background:var(--panel);color:var(--ink-2);text-decoration:none;font-size:12.5px;transition:.15s}
.navbtn:hover{border-color:#c9ced6;color:var(--ink)}
.navn{color:var(--ink-3);font-variant-numeric:tabular-nums}

.group{padding-top:36px}
.group-h{margin-bottom:16px}
.group-h h2{font-size:16.5px;font-weight:700;letter-spacing:-.01em;display:flex;align-items:baseline;gap:10px}
.group-en{font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}
.group-d{color:var(--ink-2);font-size:13px;margin-top:4px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:14px}

.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:17px 18px 15px;
  display:flex;flex-direction:column;gap:9px;min-height:168px;
  transition:border-color .16s,box-shadow .16s,transform .16s}
.card:hover{border-color:#cdd3db;box-shadow:0 4px 16px rgba(16,24,40,.07);transform:translateY(-1px)}
.card-top{display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.num{font-size:11px;font-weight:700;color:var(--ink-3);background:var(--line-2);border-radius:5px;
  padding:1px 6px;line-height:1.7;font-variant-numeric:tabular-nums}
.card h3{font-size:15px;font-weight:650;letter-spacing:-.01em}
.badge{font-size:10.5px;font-weight:600;padding:2px 7px;border-radius:20px;border:1px solid transparent;
  white-space:nowrap;margin-left:auto}
.b-ready{color:#0b6b5c;background:#e8f6f2;border-color:#c8e9e1}
.b-deps{color:#1d4ed8;background:#eaf0fe;border-color:#cfdcfb}
.b-warn{color:#92400e;background:#fdf3e3;border-color:#f4dfbc}
.desc{color:var(--ink-2);font-size:13px;flex:1}
.tags{display:flex;flex-wrap:wrap;gap:6px}
.tag{font-size:11px;color:var(--ink-3);background:#f5f6f8;border:1px solid var(--line-2);
  border-radius:5px;padding:1px 6px;line-height:1.7}
.tag.lic{color:#0b6b5c;background:#f0f9f6;border-color:#d5ece5;font-weight:600}
.links{display:flex;gap:7px;margin-top:2px}
.chip{display:inline-flex;align-items:center;gap:6px;padding:5px 11px;border-radius:7px;
  background:#f7f8fa;border:1px solid var(--line);color:var(--ink);text-decoration:none;
  font-size:12.5px;transition:.15s}
.chip:hover{background:#eef3fd;border-color:#cfdcfb;color:var(--blue)}
.arw{font-size:11px;color:var(--ink-3);line-height:1}
.chip:hover .arw{color:var(--blue)}

.how{margin-top:46px;border:1px solid var(--line);background:var(--panel);border-radius:12px;padding:20px 22px}
.how h2{font-size:15px;font-weight:700;margin-bottom:12px}
.how ol{display:grid;gap:9px;padding-left:22px;list-style:decimal}
.how li{color:var(--ink-2);font-size:13px;padding-left:2px}
.how li::marker{color:var(--ink-3);font-weight:700;font-size:12px}
.how code{background:#eef0f3;border-radius:4px;padding:1px 5px;font-size:12px;color:var(--ink-2)}

.empty{display:none;padding:70px 0;text-align:center;color:var(--ink-3)}
body.filtering .empty{display:block}
body.filtering .group{display:none}
body.filtering .group.has-hit{display:block}

.foot{margin-top:44px;padding-top:20px;border-top:1px solid var(--line);color:var(--ink-3);font-size:12px;line-height:1.9}
.foot code{background:#eef0f3;border-radius:4px;padding:1px 5px;font-size:11.5px;color:var(--ink-2)}
.foot a{color:var(--ink-2)}

@media (max-width:640px){
  .wrap,.bar-in{padding-left:16px;padding-right:16px}
  h1{font-size:26px}.stats{gap:22px}.stat+.stat{padding-left:22px}
  .grid{grid-template-columns:1fr}
}
@media print{body{background:#fff}.bar{position:static}.card{break-inside:avoid;box-shadow:none}}
</style>
</head>
<body>

<div class="wrap wrap-top">
  <header class="hero">
    <div class="eyebrow">GHZS-Project &middot; Open Source</div>
    <h1>开源项目总览<em>.</em></h1>
    <p class="sub">10 个可独立运行的项目，覆盖游戏资讯站、运营工具、数据流水线与协作方法。全部 <strong>MIT</strong> 许可，可自由使用、修改与再分发。</p>
    <div class="stats">
      <div class="stat"><b>@@N_REPO@@</b><span>开源仓库</span></div>
      <div class="stat"><b>@@N_GROUP@@</b><span>分类</span></div>
      <div class="stat"><b>MIT</b><span>统一许可证</span></div>
    </div>
  </header>
</div>

<div class="bar">
  <div class="bar-in">
    <label class="search">
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-3.5-3.5"></path></svg>
      <input id="q" type="search" placeholder="搜索项目或技术栈…" autocomplete="off">
    </label>
    @@NAV@@
  </div>
</div>

<div class="wrap">
  @@SECTIONS@@
  <div class="empty">没有匹配的项目</div>

  <section class="how">
    <h2>怎么用</h2>
    <ol>
      <li>挑一个仓库，点「打开仓库」；每个仓库的 README 都写了它自己怎么跑。</li>
      <li>需要依赖的，先在该目录执行 <code>npm install</code> 或 <code>pip install -r requirements.txt</code>。</li>
      <li>涉及第三方登录的（推送通道、后台账号），仓库内<strong>不含任何凭据</strong>，请由使用者在界面内自行登录。</li>
    </ol>
  </section>

  <footer class="foot">
    完整交接说明、可用性实测与 AI Agent 提示词：<a href="https://github.com/GHZS-Project/GH-Handover">GH-Handover</a> &middot; <a href="https://github.com/GHZS-Project/GH-Handover/blob/main/PROMPTS.md">PROMPTS.md</a><br>
    本页即组织下第 11 个仓库，作为其余项目的总入口。<br>
    本页由 <code>tools/build-pages.py</code> 生成，构建时会校验每个仓库仍公开且为 MIT。
  </footer>
</div>

<script>
(function () {
  var q = document.getElementById('q');
  var cards = [].slice.call(document.querySelectorAll('.card'));
  var groups = [].slice.call(document.querySelectorAll('.group'));
  var empty = document.querySelector('.empty');
  function norm(s) { return (s || '').toLowerCase(); }
  function setText(g, kw) {
    var p = g.querySelector('.group-d'), t = p.querySelector('.gd-text');
    var vis = 0;
    g.querySelectorAll('.card').forEach(function (c) { if (c.style.display !== 'none') vis++; });
    g.classList.toggle('has-hit', vis > 0);
    if (!p.dataset.orig) p.dataset.orig = t.textContent;
    t.textContent = kw ? ('匹配 ' + vis + ' / 共 ' + p.dataset.total) : p.dataset.orig;
  }
  function apply() {
    var kw = norm(q.value.trim()), any = false;
    if (!kw) {
      document.body.classList.remove('filtering');
      cards.forEach(function (c) { c.style.display = ''; });
      groups.forEach(function (g) { setText(g, ''); });
      empty.style.display = 'none';
      return;
    }
    document.body.classList.add('filtering');
    cards.forEach(function (c) {
      var hit = norm(c.textContent).indexOf(kw) >= 0;
      c.style.display = hit ? '' : 'none';
      if (hit) any = true;
    });
    groups.forEach(function (g) { setText(g, kw); });
    empty.style.display = any ? 'none' : 'block';
  }
  q.addEventListener('input', apply);
  q.addEventListener('keydown', function (e) { if (e.key === 'Escape') { q.value = ''; apply(); } });
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== q) { e.preventDefault(); q.focus(); }
  });
})();
</script>
</body>
</html>
"""


def main():
    dry = "--dry-run" in sys.argv
    if "--no-verify" not in sys.argv:
        print("校验远端仓库状态：")
        verify()
    html_out = build()
    if dry:
        print("将写入:", OUT, "|", len(html_out), "字节")
        return
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html_out)
    print("写出:", OUT)
    print("字节:", os.path.getsize(OUT), "| 卡片:", html_out.count('class="card"'))


if __name__ == "__main__":
    main()
