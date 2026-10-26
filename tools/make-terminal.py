# -*- coding: utf-8 -*-
"""把 KomoSkill 的 doctor.py 真实输出渲染成一张终端窗口页，供 capture-shots.py 截图。

用法：
    cd GH-KomoSkill && python scripts/doctor.py > doctor.txt
    python tools/make-terminal.py doctor.txt
    SET GH_KOMOSKILL_TERM=<本目录>   # 指向生成 komoskill-terminal.html 的目录
    python tools/capture-shots.py 10
"""
import html
import pathlib
import sys

SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "doctor.txt")
OUT = SRC.parent / "komoskill-terminal.html"

rows = []
for ln in SRC.read_text(encoding="utf-8").splitlines():
    e = html.escape(ln)
    if "[OK" in ln:
        e = e.replace("[OK  ]", '<span class="ok">[OK]</span>')
        cls = "row okrow"
    elif ln.strip().startswith("===") or ln.strip().startswith("---"):
        cls = "row dim"
    elif "合计" in ln or "结论" in ln:
        cls = "row hi"
    elif ln.startswith("GH-KomoSkill"):
        cls = "row title"
    else:
        cls = "row"
    rows.append('<div class="%s">%s</div>' % (cls, e or "&nbsp;"))

page = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>KomoSkill · doctor</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#eef1f6;font-family:"Segoe UI","Microsoft YaHei",system-ui,sans-serif;
  display:flex;align-items:center;justify-content:center;min-height:100vh;padding:20px}
.term{width:100%;max-width:1080px;background:#11161f;border-radius:12px;overflow:hidden;
  box-shadow:0 24px 60px rgba(16,24,40,.28),0 0 0 1px rgba(15,23,42,.5)}
.bar{display:flex;align-items:center;gap:8px;padding:11px 14px;background:#1a2029;border-bottom:1px solid #262e3a}
.dot{width:11px;height:11px;border-radius:50%}
.d1{background:#ff5f57}.d2{background:#febc2e}.d3{background:#28c840}
.ttl{margin-left:8px;color:#9aa7b8;font-size:12px}
.body{padding:14px 20px 16px;font-family:"Cascadia Mono","JetBrains Mono",Consolas,monospace;
  font-size:11.8px;line-height:1.52;color:#c8d3e2;white-space:pre-wrap;word-break:break-all}
.title{color:#e8f0fb;font-weight:700;font-size:13.5px;margin-bottom:2px}
.dim{color:#4d5a6c}
.hi{color:#7dd3fc;font-weight:600}
.okrow .ok{color:#4ade80;font-weight:700}
.cmd{color:#94a3b8;padding-bottom:4px}
.cmd b{color:#e2e8f0}
.caret{display:inline-block;width:7px;height:14px;background:#4ade80;vertical-align:-2px}
</style></head><body>
<div class="term">
  <div class="bar"><span class="dot d1"></span><span class="dot d2"></span><span class="dot d3"></span>
    <span class="ttl">GH-KomoSkill &mdash; python scripts/doctor.py</span></div>
  <div class="body"><div class="row cmd"><b>&gt;</b> python scripts/doctor.py</div>@@ROWS@@
<div class="row cmd" style="margin-top:6px"><b>&gt;</b> <span class="caret"></span></div></div>
</div>
</body></html>
"""
OUT.write_text(page.replace("@@ROWS@@", "\n".join(rows)), encoding="utf-8")
print("写出", OUT)
