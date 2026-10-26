# -*- coding: utf-8 -*-
"""生成 GH-Handover 的 GitHub Pages 门户页（仓库根 index.html）。

用法：
    python tools/build-pages.py              # 校验仓库状态后生成
    python tools/build-pages.py --no-verify  # 跳过远端校验（离线时用）
    python tools/build-pages.py --dry-run    # 只打印，不写文件

原则：
1. **可视化优先**：每个项目配一张真实界面截图（shots/*.webp），点开看大图。
   截图来自本机实跑或仓库自带页面，不用示意图。
2. **不脱敏（内部交接用）**：在线入口、本机端口、公司后台地址原样列出。
   这些地址仅限公司内部网络访问，公网打不开属正常。
3. **防止漂移**：生成前用 API 校验每个仓库存在且确实为 MIT，任一不符合就报错退出。
4. **幂等**：页内不写生成时间。
"""

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

ORG = "GHZS-Project"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.html")

# (仓库, 展示名, 说明, 徽章, 徽章类型, 技术标签, 截图, 截图说明, 本机端口, 线上地址)
PROJECTS = [
    (
        "GH-NewGameWIki",
        "NewGameWiki",
        "游戏资讯、活动与排期管理。8 个平台采集 → SQLite → 后台，自带 AI_AGENT_SETUP.md，把提示词发给 Agent 就能自行复刻。",
        "需装依赖",
        "deps",
        ["Node", "SQLite", "React"],
        "01-newgamewiki.webp",
        "首页：全部数据池 7,072 条 · 手机游戏 1,501 · 福利 352 · 端游资讯 5,219，右侧是游戏日历排期",
        "64111",
        "",
    ),
    (
        "GH-GameNews",
        "GameNews",
        "资讯采集 → 今日简讯 → 日报/周报海报 → 飞书投递，对接 7 个平台并含定时调度。公开版已移除人工编辑器。",
        "需装依赖",
        "deps",
        ["Node", "SQLite", "React"],
        "02-gamenews.webp",
        "今日简讯：38 条要点 · 4 款新游上线 · 20 条 Steam 信息 · 14 条版本更新，下接各平台分栏",
        "64423",
        "",
    ),
    (
        "GH-Gamehub",
        "GameHub",
        "单机游戏聚合站：游戏、MOD、存档、修改器与模拟器配置，共 6 个页面。内置搜索与内容库同步。",
        "需装依赖",
        "deps",
        ["Node", "Express", "静态前端"],
        "03-gamehub.webp",
        "线上版全站热榜 + 最新收录：机地 × XDGAME 双源 12,304 款，卡片带评分、容量、归属源",
        "8123",
        "https://gamehub-agg-v4.app.workbuddy.host/",
    ),
    (
        "GH-GameGather-APP",
        "GameGather APP",
        "PC 与手游情报站 + 资源索引 + aria2 下载的 Electron 桌面成品。Release 提供整包，解压后双击即可运行。",
        "Release 成品",
        "ready",
        ["Electron", "Node"],
        "04-gamegather-app.webp",
        "桌面客户端首页：轮播推荐、PC 新游 Top 10、评分与容量/更新时间一览",
        "",
        "",
    ),
    (
        "GH-GameGather-UPSTREAM",
        "GameGather UPSTREAM",
        "上面那个 App 的配套数据服务：Express 服务 + 15 个抓取器 + 索引快照。没有它，App 只能看离线数据。",
        "需装依赖",
        "deps",
        ["Node", "Express", "抓取器"],
        "05-gamegather-upstream.webp",
        "管理后台仪表盘：库内 19,842 · 可见 12,381 · 双源覆盖 13,448，右侧是各分项覆盖率",
        "8123",
        "",
    ),
    (
        "GH-Game-Puton",
        "Game Puton",
        "Windows 游戏后台上架批量导入工具（Electron），含交接文档、操作手册与字段映射表。仓库只含源码，成品需自行打包。",
        "需自行打包",
        "warn",
        ["Electron", "Node"],
        "06-gameputon.webp",
        "游戏导入台：4 步流程（选目录 → 登录后台 → 扫缺失 → 选策略），左侧实时状态与进度",
        "",
        "",
    ),
    (
        "GH-WeeklyReport",
        "WeeklyReport",
        "Excel 周报分析：当周、跨周汇总、收益汇总与趋势图，默认 8787 端口。零第三方依赖，克隆即跑。",
        "零依赖",
        "ready",
        ["Node", "零依赖"],
        "07-weeklyreport.webp",
        "周报分析：九游 CPS / 801 两套口径的活跃、注册、付费、ARPU、收益同屏对比",
        "8787",
        "",
    ),
    (
        "GH-GameSearch",
        "GameSearch",
        "Android 游戏信息查询 App（Kotlin）：通过 WebView 登录后台，按账号权限读取游戏信息与详情。成品 APK 在 dist/。",
        "成品 APK",
        "ready",
        ["Kotlin", "Android"],
        "08-gamesearch.webp",
        "App 查询页（390×844 手机视口）：输入游戏名后列出同名候选，带副标题、分类与游戏 ID",
        "",
        "",
    ),
    (
        "GH-CloudGame",
        "CloudGame",
        "端游云游戏三源周报可复刻工程：脚本、词库、口径与 4 期产出齐全。交给 AI 读 AGENT.md，即可跑出同款 Excel 与看板。",
        "开箱即用",
        "ready",
        ["Python", "pandas", "HTML"],
        "09-cloudgame.webp",
        "三源周报看板：搜索 3,003,769 次（+72.9%）· 鲸云下载 104,846 次（+46%）· Steam 57 款，下方是跨期对比",
        "",
        "https://cee91cf9b0ac44baa16b30868c8b4c47.app.workbuddy.link",
    ),
    (
        "GH-KomoSkill",
        "KomoSkill",
        "AI 协作工作法技能包：六阶段门禁 + 证据纪律 + 防失忆，Codex、WorkBuddy 与 Claude 通用。不是业务工具，是方法。",
        "脚本即用",
        "ready",
        ["Python", "Markdown"],
        "10-komoskill.webp",
        "doctor.py 自检：9 项全 OK（Python 版本 / 安装位置 / references / templates / scripts / 可执行 / UTF-8）",
        "",
        "",
    ),
]

GROUPS = [
    ("站点与数据", "SITES & DATA", "可独立部署的服务端与桌面端应用", 0, 5),
    ("工具与方法", "TOOLCHAIN & METHOD", "日常运营工具、数据流水线与协作方法", 5, 10),
]

# 竖屏截图（手机 UI）：缩略图用 contain，别横向裁掉
PORTRAIT = {"08-gamesearch.webp"}

# 在线入口一览（内部使用，不脱敏）：(用途, 地址, 说明)
LINKS = [
    ("GameHub 线上站", "https://gamehub-agg-v4.app.workbuddy.host/", "公网可访问，当前 prod 版本"),
    ("端游周报看板", "https://cee91cf9b0ac44baa16b30868c8b4c47.app.workbuddy.link", "CloudGame 最新一期产出"),
    ("GameHub 本机", "http://127.0.0.1:8123/", "npm install && npm start 后打开"),
    ("GameHub 管理后台", "http://127.0.0.1:8123/admin.html", "库构成 / 缺口 / 数据源健康"),
    ("NewGameWiki", "http://127.0.0.1:64111/", "前后端一起起，端口见 .env"),
    ("GameNews 工作台", "http://127.0.0.1:64423/", "需同时起 64424 后端"),
    ("WeeklyReport", "http://127.0.0.1:8787/", "零依赖，node server/server.mjs"),
    ("游戏后台上架", "https://and-admin.ghzs.com/", "需要公司后台账号，Puton / GameSearch 共用"),
    ("鲸云数据", "http://coop.jingyungame.com/#/login", "需要公司账号，CloudGame 下载数据来源"),
    ("数据平台（神策）", "https://zx.20130123.com/light_gm/login.html", "需要公司账号，CloudGame 搜索数据来源"),
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
        repo, name, desc, badge, btype, tags, shot, cap, port, live = PROJECTS[i]
        tag_html = "".join('<span class="tag">%s</span>' % esc(t) for t in tags)
        chips = [
            '<a class="chip" href="https://github.com/%s/%s" target="_blank" rel="noopener">'
            '<span>打开仓库</span><span class="arw">&#8599;</span></a>' % (ORG, repo)
        ]
        if live:
            chips.append(
                '<a class="chip live" href="%s" target="_blank" rel="noopener">'
                '<span>在线访问</span><span class="arw">&#8599;</span></a>' % esc(live)
            )
        if port:
            chips.append(
                '<button class="chip mono" data-copy="http://127.0.0.1:%s/" title="点击复制本机地址">'
                '<span class="dot-live"></span><span class="pt">:%s</span></button>' % (port, port)
            )
        out.append(
            '<article class="card" data-idx="%02d">'
            '<button class="thumb%s" data-i="%d" aria-label="查看 %s 截图">'
            '<img src="shots/%s" alt="%s 界面截图" loading="lazy" width="1400" height="875">'
            '<span class="zoom">&#9974; 看大图</span>'
            "</button>"
            '<div class="cbody">'
            '<div class="card-top"><span class="num">%02d</span><h3>%s</h3>'
            '<span class="badge b-%s">%s</span></div>'
            '<p class="shotcap"><span class="cam">&#9635;</span>%s</p>'
            '<p class="desc">%s</p>'
            '<div class="tags">%s<span class="tag lic">MIT</span></div>'
            '<div class="links">%s</div>'
            "</div>"
            "</article>"
            % (
                i + 1,
                " portrait" if shot in PORTRAIT else "",
                i,
                esc(name),
                shot,
                esc(name),
                i + 1,
                esc(name),
                btype,
                esc(badge),
                esc(cap),
                esc(desc),
                tag_html,
                "".join(chips),
            )
        )
    return "".join(out)


def link_rows():
    rows = []
    for use, url, note in LINKS:
        rows.append(
            '<tr><td class="u">%s</td>'
            '<td><a href="%s" target="_blank" rel="noopener">%s</a></td>'
            '<td class="n">%s</td></tr>' % (esc(use), esc(url), esc(url), esc(note))
        )
    return "".join(rows)


def shots_json():
    data = [
        {
            "src": "shots/" + p[6],
            "title": p[1],
            "cap": p[7],
            "repo": "https://github.com/%s/%s" % (ORG, p[0]),
        }
        for p in PROJECTS
    ]
    return json.dumps(data, ensure_ascii=False)


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

    html = TEMPLATE
    for k, v in (
        ("@@NAV@@", nav),
        ("@@SECTIONS@@", "".join(sections)),
        ("@@LINKS@@", link_rows()),
        ("@@N_REPO@@", str(len(PROJECTS))),
        ("@@N_GROUP@@", str(len(GROUPS))),
        ("@@N_SHOT@@", str(len(PROJECTS))),
        ("@@SHOTS@@", shots_json()),
    ):
        html = html.replace(k, v)
    return html


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="GHZS-Project 交接总览：10 个可独立运行的项目，全部 MIT，含真实界面截图与在线入口。">
<title>GHZS-Project · 项目交接总览</title>
<style>
:root{
  --bg:#f5f6f8;--panel:#fff;--line:#e4e6ea;--line-2:#eff1f4;
  --ink:#15181d;--ink-2:#5b6472;--ink-3:#8a93a1;
  --blue:#2563eb;--teal:#0f766e;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-size:14px;line-height:1.65;
  font-family:"Segoe UI","PingFang SC","Microsoft YaHei",system-ui,-apple-system,sans-serif;
  -webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding:0 28px 72px}
.wrap-top{padding-bottom:0}

.hero{padding:52px 0 24px;border-bottom:1px solid var(--line)}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ink-3);font-weight:600;margin-bottom:14px}
.eyebrow::before{content:"";width:22px;height:2px;background:var(--blue);display:block}
h1{font-size:34px;line-height:1.25;letter-spacing:-.02em;font-weight:700}
h1 em{font-style:normal;color:var(--blue)}
.sub{margin-top:11px;color:var(--ink-2);font-size:14.5px;max-width:720px}
.stats{display:flex;gap:34px;margin-top:24px;flex-wrap:wrap}
.stat b{display:block;font-size:24px;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.stat span{font-size:12px;color:var(--ink-3)}
.stat+.stat{border-left:1px solid var(--line);padding-left:34px}

.bar{position:sticky;top:0;z-index:20;background:rgba(245,246,248,.94);backdrop-filter:blur(10px);
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

.group{padding-top:38px}
.group-h{margin-bottom:16px}
.group-h h2{font-size:16.5px;font-weight:700;letter-spacing:-.01em;display:flex;align-items:baseline;gap:10px}
.group-en{font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}
.group-d{color:var(--ink-2);font-size:13px;margin-top:4px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:16px}

.card{background:var(--panel);border:1px solid var(--line);border-radius:13px;overflow:hidden;
  display:flex;flex-direction:column;
  transition:border-color .16s,box-shadow .16s,transform .16s}
.card:hover{border-color:#cdd3db;box-shadow:0 6px 22px rgba(16,24,40,.09);transform:translateY(-1px)}
.thumb{position:relative;display:block;width:100%;padding:0;border:0;border-bottom:1px solid var(--line-2);
  background:#eef1f5;cursor:zoom-in;overflow:hidden;aspect-ratio:16/10}
.thumb img{display:block;width:100%;height:100%;object-fit:cover;object-position:top center;
  transition:transform .35s ease,filter .2s}
.thumb:hover img{transform:scale(1.015)}
.zoom{position:absolute;right:9px;bottom:9px;background:rgba(17,22,31,.78);color:#fff;
  font-size:11px;padding:3px 8px;border-radius:6px;opacity:0;transition:opacity .18s;letter-spacing:.02em}
.thumb:hover .zoom{opacity:1}
.thumb.portrait{background:#dde4ee;padding:16px 0}
.thumb.portrait img{width:auto;height:100%;margin:0 auto;object-fit:contain;
  border-radius:9px;box-shadow:0 6px 22px rgba(16,24,40,.2)}

.cbody{padding:14px 16px 15px;display:flex;flex-direction:column;gap:9px;flex:1}
.shotcap{font-size:11.5px;line-height:1.55;color:var(--ink-3);background:#f7f8fa;
  border:1px solid var(--line-2);border-radius:7px;padding:6px 9px;display:flex;gap:6px}
.cam{color:#b9c1cd;flex:none;font-size:10px;line-height:1.7}
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
.links{display:flex;gap:7px;margin-top:2px;flex-wrap:wrap}
.chip{display:inline-flex;align-items:center;gap:6px;padding:5px 11px;border-radius:7px;
  background:#f7f8fa;border:1px solid var(--line);color:var(--ink);text-decoration:none;
  font-size:12.5px;transition:.15s;font-family:inherit;cursor:pointer}
.chip:hover{background:#eef3fd;border-color:#cfdcfb;color:var(--blue)}
.chip.live{background:#f0f9f6;border-color:#d5ece5;color:#0b6b5c}
.chip.live:hover{background:#e3f4ee;color:#0b6b5c}
.chip.mono{font-family:Consolas,"Cascadia Mono",monospace;font-size:11.5px;color:var(--ink-2);gap:5px}
.chip.mono.done{background:#e8f6f2;border-color:#c8e9e1;color:#0b6b5c}
.dot-live{width:6px;height:6px;border-radius:50%;background:#22c55e;display:inline-block}
.arw{font-size:11px;color:var(--ink-3);line-height:1}
.chip:hover .arw{color:var(--blue)}

.sec{border:1px solid var(--line);background:var(--panel);border-radius:13px;padding:20px 22px;margin-top:34px}
.sec h2{font-size:15.5px;font-weight:700;margin-bottom:4px}
.sec .hint{color:var(--ink-3);font-size:12.5px;margin-bottom:14px}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line-2);vertical-align:top}
th{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);font-weight:600;
  background:#fafbfc}
tr:last-child td{border-bottom:0}
td.u{white-space:nowrap;font-weight:600}
td a{color:var(--blue);text-decoration:none;word-break:break-all}
td a:hover{text-decoration:underline}
td.n{color:var(--ink-2)}
.mono-t{font-family:Consolas,"Cascadia Mono",monospace}

.how ol{display:grid;gap:9px;padding-left:22px;list-style:decimal;margin-top:10px}
.how li{color:var(--ink-2);font-size:13px;padding-left:2px}
.how li::marker{color:var(--ink-3);font-weight:700;font-size:12px}
.how code{background:#eef0f3;border-radius:4px;padding:1px 5px;font-size:12px;color:var(--ink-2)}

.empty{display:none;padding:70px 0;text-align:center;color:var(--ink-3)}
body.filtering .empty{display:block}
body.filtering .group{display:none}
body.filtering .group.has-hit{display:block}

.foot{margin-top:40px;padding-top:20px;border-top:1px solid var(--line);color:var(--ink-3);font-size:12px;line-height:1.9}
.foot code{background:#eef0f3;border-radius:4px;padding:1px 5px;font-size:11.5px;color:var(--ink-2)}
.foot a{color:var(--ink-2)}

/* 灯箱 */
.lb{position:fixed;inset:0;z-index:100;background:rgba(12,16,23,.9);display:none;
  flex-direction:column;padding:16px;backdrop-filter:blur(3px)}
.lb.on{display:flex}
.lb-top{display:flex;align-items:center;gap:14px;color:#e9eef6;padding:2px 6px 10px}
.lb-cap{font-size:13px;line-height:1.5;flex:1}
.lb-cap b{font-weight:700;color:#fff}
.lb-x{margin-left:auto;background:rgba(255,255,255,.12);border:0;color:#fff;width:32px;height:32px;
  border-radius:8px;font-size:15px;cursor:pointer;flex:none}
.lb-x:hover{background:rgba(255,255,255,.22)}
.lb-stage{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
.lb-img{max-width:100%;max-height:100%;border-radius:8px;box-shadow:0 20px 60px rgba(0,0,0,.5);
  background:#fff;cursor:zoom-out}
.lb-bar{display:flex;align-items:center;justify-content:center;gap:12px;padding-top:12px;color:#c2ccd9;font-size:12px}
.lb-bar button{background:rgba(255,255,255,.12);border:0;color:#e9eef6;padding:6px 14px;border-radius:7px;
  font-size:12.5px;cursor:pointer;font-family:inherit}
.lb-bar button:hover{background:rgba(255,255,255,.22)}
.lb-bar button:disabled{opacity:.35;cursor:default}
.lb-n{font-variant-numeric:tabular-nums;color:#8b98a9;min-width:52px;text-align:center}

@media (max-width:900px){.grid{grid-template-columns:1fr}}
@media (max-width:640px){
  .wrap,.bar-in{padding-left:16px;padding-right:16px}
  h1{font-size:26px}.stats{gap:20px}.stat+.stat{padding-left:20px}
  .sec{padding:16px}
  table{font-size:11.5px}th,td{padding:6px 6px}
}
@media print{body{background:#fff}.bar{position:static}.card{break-inside:avoid;box-shadow:none}.lb{display:none!important}}
</style>
</head>
<body>

<div class="wrap wrap-top">
  <header class="hero">
    <div class="eyebrow">GHZS-Project &middot; Handover / Open Source</div>
    <h1>项目交接总览<em>.</em></h1>
    <p class="sub"><strong>@@N_REPO@@ 个可独立运行的项目</strong>，覆盖游戏资讯站、运营工具、数据流水线与协作方法。每个项目配一张真实界面截图，点开看大图；全部 <strong>MIT</strong> 许可，clone 下来就能改、能再分发。</p>
    <div class="stats">
      <div class="stat"><b>@@N_REPO@@</b><span>开源仓库</span></div>
      <div class="stat"><b>@@N_SHOT@@</b><span>真实界面截图</span></div>
      <div class="stat"><b>5</b><span>开箱即用</span></div>
      <div class="stat"><b>MIT</b><span>统一许可证</span></div>
    </div>
  </header>
</div>

<div class="bar">
  <div class="bar-in">
    <label class="search">
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-3.5-3.5"></path></svg>
      <input id="q" type="search" placeholder="搜索项目、技术栈或端口…" autocomplete="off">
    </label>
    @@NAV@@
    <a class="navbtn" href="#links">在线入口<span class="navn">@@N_REPO@@</span></a>
    <a class="navbtn" href="PROMPTS.md">AI 提示词</a>
  </div>
</div>

<div class="wrap">
  @@SECTIONS@@
  <div class="empty">没有匹配的项目</div>

  <section class="sec" id="links">
    <h2>在线入口一览</h2>
    <p class="hint">内部交接用，地址原样保留。带 <span class="mono-t">127.0.0.1</span> 的需先把对应服务跑起来；公司后台类地址要在公司网络内、并用公司账号登录。</p>
    <table>
      <thead><tr><th>用途</th><th>地址</th><th>说明</th></tr></thead>
      <tbody>@@LINKS@@</tbody>
    </table>
  </section>

  <section class="sec how">
    <h2>怎么用</h2>
    <ol>
      <li>点任意截图看大图，右键可另存；每张图下方都写清了它展示的是什么数据。</li>
      <li>挑一个仓库，点「打开仓库」；每个仓库的 README 都写了它自己怎么跑。需要依赖的先 <code>npm install</code> 或 <code>pip install -r requirements.txt</code>。</li>
      <li>涉及第三方登录的（飞书推送、公司后台），仓库内<strong>不含任何凭据</strong>，由使用者在界面内自行登录。</li>
      <li>想让 AI 接手，把 <a href="PROMPTS.md">PROMPTS.md</a> 里对应段落整段复制给它。</li>
    </ol>
  </section>

  <footer class="foot">
    完整交接说明、可用性实测与 AI Agent 提示词：<a href="https://github.com/@ORG@/GH-Handover">GH-Handover</a> &middot;
    <a href="https://github.com/@ORG@/GH-Handover/blob/main/PROMPTS.md">PROMPTS.md</a><br>
    截图全部来自本机实跑或仓库自带页面（非示意图），文件在 <code>shots/</code>，可直接用于 PPT。<br>
    本页由 <code>tools/build-pages.py</code> 生成；构建时会校验每个仓库仍公开且为 MIT。
  </footer>
</div>

<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="项目截图">
  <div class="lb-top">
    <div class="lb-cap" id="lbCap"></div>
    <button class="lb-x" id="lbX" aria-label="关闭">&#10005;</button>
  </div>
  <div class="lb-stage"><img class="lb-img" id="lbImg" alt=""></div>
  <div class="lb-bar">
    <button id="lbPrev">&#8249; 上一个</button>
    <span class="lb-n" id="lbN"></span>
    <button id="lbNext">下一个 &#8250;</button>
  </div>
</div>

<script>
(function () {
  var DATA = @@SHOTS@@;

  /* 搜索过滤 */
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

  /* 本机端口点击复制 */
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function (ev) {
      ev.preventDefault();
      var txt = b.getAttribute('data-copy');
      var lbl = b.querySelector('.pt');
      var done = function () {
        var old = lbl.textContent;
        b.classList.add('done');
        lbl.textContent = ' 已复制';
        setTimeout(function () {
          b.classList.remove('done');
          lbl.textContent = old;
        }, 1400);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(txt).then(done, done);
      } else { done(); }
    });
  });

  /* 灯箱 */
  var lb = document.getElementById('lb'), lbImg = document.getElementById('lbImg'),
      lbCap = document.getElementById('lbCap'), lbN = document.getElementById('lbN'),
      lbPrev = document.getElementById('lbPrev'), lbNext = document.getElementById('lbNext');
  var cur = -1;

  function render() {
    var d = DATA[cur];
    lbImg.src = d.src;
    lbImg.alt = d.title + ' 界面截图';
    lbCap.innerHTML = '<b>' + d.title + '</b> · ' + d.cap;
    lbN.textContent = (cur + 1) + ' / ' + DATA.length;
    lbPrev.disabled = cur <= 0;
    lbNext.disabled = cur >= DATA.length - 1;
  }
  function open(i) {
    cur = i; render();
    lb.classList.add('on');
    document.body.style.overflow = 'hidden';
  }
  function close() {
    lb.classList.remove('on');
    document.body.style.overflow = '';
    lbImg.src = '';
  }
  function step(n) {
    var i = cur + n;
    if (i < 0 || i >= DATA.length) return;
    cur = i; render();
  }
  document.querySelectorAll('.thumb').forEach(function (t) {
    t.addEventListener('click', function () { open(parseInt(t.getAttribute('data-i'), 10)); });
  });
  document.getElementById('lbX').addEventListener('click', close);
  lbPrev.addEventListener('click', function () { step(-1); });
  lbNext.addEventListener('click', function () { step(1); });
  lbImg.addEventListener('click', close);
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('on')) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowLeft') step(-1);
    else if (e.key === 'ArrowRight') step(1);
  });
})();
</script>
</body>
</html>
""".replace("@@ORG@@", ORG)


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
