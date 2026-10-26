# -*- coding: utf-8 -*-
"""生成一个本地预览页（不进仓库，避免与 md 双份维护）。

用法：python tools/make-preview.py
产物：../../GH-Handover-预览.html
"""
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDIR = os.path.join(BASE, "prompts")
OUT = os.path.join(os.path.dirname(BASE), "GH-Handover-预览.html")

PROJECTS = [
    ("GH-Gamehub", "单机游戏聚合站", "机地 + XDGAME 的游戏 / MOD / 存档 / 修改器 / 模拟器配置，6 页 + 管理后台", "⚠️ 装一次依赖", "https://github.com/GHZS-Project/GH-Gamehub", "04-Gamehub.md"),
    ("GH-GameGather-APP", "游戏情报桌面成品", "PC/手游情报站 + 资源索引 + aria2 下载，Electron 成品（Release v28 262MB）", "✅ 开箱即用", "https://github.com/GHZS-Project/GH-GameGather-APP", "05-GameGather.md"),
    ("GH-GameGather-UPSTREAM", "配套数据服务", "Express + 15 个抓取器 + 93.6MB JSON 索引快照，APP 的后端", "⚠️ 装一次依赖", "https://github.com/GHZS-Project/GH-GameGather-UPSTREAM", "05-GameGather.md"),
    ("GH-GameNews", "资讯采集与日报周报", "7 平台采集 → 今日简讯 → 日报/周报海报 → 飞书投递，含定时调度", "⚠️ 装一次依赖", "https://github.com/GHZS-Project/GH-GameNews", "07-GameNews.md"),
    ("GH-NewGameWIki", "新游资讯与排期管理", "8 平台采集 → SQLite → 后台，重点管排期", "⚠️ 装一次依赖", "https://github.com/GHZS-Project/GH-NewGameWIki", "08-NewGameWIki.md"),
    ("GH-GameSearch", "Android 查询 App", "内部游戏信息查询，按后台账号权限读数据（Kotlin）", "✅ 开箱即用", "https://github.com/GHZS-Project/GH-GameSearch", "06-GameSearch.md"),
    ("GH-Game-Puton", "后台上架批量导入", "Windows 桌面工具，批量往 and-admin.ghzs.com 填上架信息", "🔶 需自己打包", "https://github.com/GHZS-Project/GH-Game-Puton", "09-Game-Puton.md"),
    ("GH-CloudGame", "端游三源周报", "神策搜索 / 鲸云下载 / SteamDB 销量 → Excel 五表 + HTML 看板，实测 104 秒跑通", "✅ 开箱即用", "https://github.com/GHZS-Project/GH-CloudGame", "01-CloudGame.md"),
    ("GH-WeeklyReport", "Excel 周报分析", "当周 / 跨周汇总 / 收益汇总 / 趋势图，零依赖", "✅ 开箱即用", "https://github.com/GHZS-Project/GH-WeeklyReport", "02-WeeklyReport.md"),
    ("GH-KomoSkill", "AI 协作工作法", "六阶段门禁 + 证据纪律 + 防失忆，Codex / WorkBuddy / Claude 通用", "✅ 开箱即用", "https://github.com/GHZS-Project/GH-KomoSkill", "03-KomoSkill.md"),
]


def extract_prompt(fname):
    """从 prompts/xx.md 里取出第一个 ```text 代码块的内容。"""
    path = os.path.join(PDIR, fname)
    if not os.path.exists(path):
        return None
    with io.open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"```text\n(.*?)\n```", text, re.S)
    return m.group(1) if m else None


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


cards = []
modal = []
for i, (name, title, desc, level, url, pf) in enumerate(PROJECTS, 1):
    badge = "ok" if level.startswith("✅") else ("warn" if level.startswith("⚠️") else "hard")
    cards.append(
        """<div class="card">
  <div class="c-head"><span class="idx">%02d</span><a class="c-name" href="%s" target="_blank">%s</a>
  <span class="badge %s">%s</span></div>
  <div class="c-title">%s</div>
  <div class="c-desc">%s</div>
  <button class="copy" data-t="%d">复制对应 Prompt</button>
</div>""" % (i, url, name, badge, level, title, desc, i - 1))

    p = extract_prompt(pf)
    if p:
        modal.append(
            """<div class="prompt" id="p%d">
  <div class="p-head"><strong>%s · %s</strong>
    <span class="p-actions">
      <a href="prompts/%s" target="_blank">单独打开</a>
      <button class="copy2" data-i="%d">复制</button>
    </span>
  </div>
  <pre id="t%d">%s</pre>
</div>""" % (i - 1, name, title, pf, i - 1, i - 1, esc(p)))

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GH 系列交接总览</title>
<style>
:root{
  --bg:#f6f7f9; --panel:#ffffff; --line:#e5e7eb; --ink:#1f2328; --sub:#57606a;
  --ok:#1a7f37; --okbg:#e8f5ec; --warn:#9a6700; --warnbg:#fff4d6; --hard:#a40e26; --hardbg:#ffe9ec;
  --acc:#2f6feb; --code:#f3f5f7;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:-apple-system,"Segoe UI","Microsoft YaHei",system-ui,sans-serif;line-height:1.6}
.wrap{max-width:1080px;margin:0 auto;padding:32px 20px 72px}
h1{font-size:26px;margin:0 0 8px}
.lead{color:var(--sub);font-size:14px;margin-bottom:22px}
.lead a{color:var(--acc);text-decoration:none}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:26px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.stat b{display:block;font-size:22px;letter-spacing:-.5px}
.stat span{font-size:12px;color:var(--sub)}
h2{font-size:16px;margin:30px 0 12px;padding-left:10px;border-left:3px solid var(--acc)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px}
.c-head{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.idx{font-size:11px;color:#8b949e;font-variant-numeric:tabular-nums}
.c-name{font-weight:600;font-size:14px;color:var(--ink);text-decoration:none;border-bottom:1px dashed #c8ccd1}
.c-name:hover{color:var(--acc);border-color:var(--acc)}
.c-title{font-size:13px;color:var(--acc);margin:6px 0 4px}
.c-desc{font-size:12.5px;color:var(--sub);min-height:38px}
.badge{font-size:11px;padding:2px 8px;border-radius:20px;margin-left:auto;white-space:nowrap}
.badge.ok{color:var(--ok);background:var(--okbg)}
.badge.warn{color:var(--warn);background:var(--warnbg)}
.badge.hard{color:var(--hard);background:var(--hardbg)}
.copy{margin-top:12px;width:100%;padding:7px;font-size:12.5px;cursor:pointer;
  background:#f6f8fa;border:1px solid var(--line);border-radius:7px;color:var(--ink);
  font-family:inherit;transition:.15s}
.copy:hover{background:#eef1f4;border-color:#d0d7de}
.copy.done{background:var(--okbg);border-color:#a7d8b5;color:var(--ok)}
.prompt{background:var(--panel);border:1px solid var(--line);border-radius:10px;margin-bottom:12px;overflow:hidden}
.prompt.flash{box-shadow:0 0 0 3px #cfe0ff}
.p-head{display:flex;align-items:center;justify-content:space-between;gap:10px;
  padding:11px 14px;background:#fafbfc;border-bottom:1px solid var(--line);font-size:13px}
.p-actions{display:flex;align-items:center;gap:12px;font-size:12px}
.p-actions a{color:var(--acc);text-decoration:none}
.copy2{padding:4px 12px;font-size:12px;cursor:pointer;background:#fff;
  border:1px solid var(--line);border-radius:6px;font-family:inherit}
.copy2:hover{background:#f0f3f6}
pre{margin:0;padding:14px;background:var(--code);font-size:12px;line-height:1.65;
  white-space:pre-wrap;word-break:break-word;max-height:340px;overflow:auto;
  font-family:Consolas,"Courier New",monospace;color:#24292f}
.note{background:#fff8e6;border:1px solid #f0dfae;border-radius:9px;padding:14px 16px;
  font-size:13px;margin-bottom:8px}
.note b{color:#7d4e00}
ol.cmd{background:var(--panel);border:1px solid var(--line);border-radius:10px;
  padding:14px 14px 14px 34px;margin:0;font-size:12.5px}
ol.cmd li{margin:5px 0}
code{background:#eef1f4;padding:1px 5px;border-radius:4px;font-size:12px;
  font-family:Consolas,monospace}
footer{margin-top:36px;font-size:12px;color:#8b949e;text-align:center}
</style>
</head>
<body>
<div class="wrap">
  <h1>GH 系列 · 交接总览</h1>
  <div class="lead">10 个仓库已全部公开并整理到一处 ·
    总入口 <a href="https://github.com/GHZS-Project/GH-Handover" target="_blank">github.com/GHZS-Project/GH-Handover</a>
  </div>

  <div class="stats">
    <div class="stat"><b>10</b><span>交接仓库</span></div>
    <div class="stat"><b>5</b><span>开箱即用</span></div>
    <div class="stat"><b>0</b><span>真实密钥泄露</span></div>
    <div class="stat"><b>10</b><span>可复制 Prompt</span></div>
  </div>

  <div class="note"><b>仓库里没有凭据。</b>账号、密码、飞书密钥、后台登录态全部按设计排除，
  <code>.gitignore</code> 明确拦截，历史提交也已核查干净。用到时由使用者自己登录或初始化。</div>

  <h2>项目一览</h2>
  <div class="grid">
__CARDS__
  </div>

  <h2>最快上手三条</h2>
  <ol class="cmd">
    <li><code>git clone https://github.com/GHZS-Project/GH-CloudGame.git</code> → <code>pip install -r requirements.txt</code> + <code>npm i jsdom</code> → <code>cd pipeline &amp;&amp; python 09_run_all.py</code>（约 104 秒出看板 + Excel）</li>
    <li><code>git clone https://github.com/GHZS-Project/GH-WeeklyReport.git</code> → <code>node server/server.mjs</code>（零依赖，开 8787）</li>
    <li><code>git clone https://github.com/GHZS-Project/GH-KomoSkill.git</code> → <code>python scripts/doctor.py</code>（8 项自检）</li>
  </ol>

  <h2>可直接复制的 AI Agent Prompt</h2>
  <div class="lead" style="margin-bottom:14px">
    每段都是完整指令。点「复制」后直接粘给任意 AI 即可，不用再补充背景。
  </div>
__PROMPTS__
  <footer>核对时间 2026-10-26 · 内容与 GitHub 上的 PROMPTS.md 同源</footer>
</div>
<script>
function flash(btn){
  var old = btn.textContent;
  btn.textContent = '已复制 ✓';
  btn.classList.add('done');
  setTimeout(function(){ btn.textContent = old; btn.classList.remove('done'); }, 1600);
}
function doCopy(text, btn){
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(function(){ flash(btn); }, function(){ fallback(text, btn); });
  } else { fallback(text, btn); }
}
function fallback(text, btn){
  var ta = document.createElement('textarea');
  ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
  document.body.appendChild(ta); ta.select();
  try { document.execCommand('copy'); flash(btn); } catch(e) { alert('复制失败，请手动选择文本'); }
  document.body.removeChild(ta);
}
document.querySelectorAll('.copy').forEach(function(b){
  b.addEventListener('click', function(){
    var i = b.dataset.t, pre = document.getElementById('t' + i);
    if (!pre) return;
    var box = document.getElementById('p' + i);
    box.classList.add('flash');
    box.scrollIntoView({behavior:'smooth', block:'center'});
    setTimeout(function(){ box.classList.remove('flash'); }, 1200);
    doCopy(pre.textContent, b);
  });
});
document.querySelectorAll('.copy2').forEach(function(b){
  b.addEventListener('click', function(){
    var pre = document.getElementById('t' + b.dataset.i);
    if (pre) doCopy(pre.textContent, b);
  });
});
</script>
</body>
</html>
"""

html = html.replace("__CARDS__", "\n".join(cards)).replace("__PROMPTS__", "\n".join(modal))

with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(html)

print("预览页已生成：%s" % OUT)
print("卡片 %d 个 / prompt 块 %d 个 / %.1f KB" % (len(cards), len(modal), len(html) / 1024.0))
