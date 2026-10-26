# -*- coding: utf-8 -*-
"""把 prompts/*.md 拼成 PROMPTS.md 合集。

处理要点：
1. 每个单文件的 `# 标题` 降为 `## `，`## ` 降为 `### `，保持合集层级正确
2. 目录里用相对路径链到单文件（GitHub 锚点对中文/符号不稳定，文件链接更可靠）
"""
import io
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDIR = os.path.join(BASE, "prompts")

files = sorted(f for f in os.listdir(PDIR) if f.endswith(".md"))


def demote(body):
    """标题降一级：'# ' -> '## '，'## ' -> '### '（只处理行首）。"""
    out = []
    for line in body.split("\n"):
        if line.startswith("### "):
            out.append("#### " + line[4:])
        elif line.startswith("## "):
            out.append("### " + line[3:])
        elif line.startswith("# "):
            out.append("## " + line[2:])
        else:
            out.append(line)
    return "\n".join(out)


out = []
out.append("# GH 系列 · AI Agent Prompt 合集\n")
out.append("> 每一节都是一段**完整可复制**的 prompt。复制代码块里的整段文字发给任意 AI 即可。\n")
out.append("> 想单独拿某一个项目的链接：点下表右列。总览与可用性判定见 [README.md](README.md)。\n")

out.append("\n## 三条通用红线（每段 prompt 里都已复述）\n")
out.append("1. **不许猜凭据** —— 找不到就停下问人，不编造 Token / 密码 / Key，不硬编码进代码。")
out.append("2. **先自检再动手** —— 有 `doctor` / `setup-check` / `09_run_all` 的，先跑它们，通过后再改代码。")
out.append("3. **改动前先备份、先说明** —— 不 `rm -rf`、不 `git push --force`、不改无关仓库。\n")

out.append("\n## 索引\n")
out.append("| 段 | 适用场景 | 单独链接 |")
out.append("|---|---|---|")
desc = {
    "00-总览": "刚接手 / 不知道从哪开始",
    "01-CloudGame": "跑通三源周报流水线",
    "02-WeeklyReport": "分析自己的周报 Excel",
    "03-KomoSkill": "装 AI 协作规范",
    "04-Gamehub": "起游戏聚合站",
    "05-GameGather": "用桌面成品 / 起数据服务",
    "06-GameSearch": "看懂或重编 Android App",
    "07-GameNews": "配资讯采集与日报",
    "08-NewGameWIki": "起排期管理后台",
    "09-Game-Puton": "打包后台上架工具",
}
for f in files:
    name = f[:-3]
    out.append("| `%s` | %s | [打开](prompts/%s) |" % (name, desc.get(name, ""), f))
out.append("\n---\n")

for f in files:
    with io.open(os.path.join(PDIR, f), encoding="utf-8") as fh:
        body = fh.read().strip()
    out.append(demote(body))
    out.append("\n---\n")

text = "\n".join(out).rstrip()
if text.endswith("---"):
    text = text[:-3].rstrip()

with io.open(os.path.join(BASE, "PROMPTS.md"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(text + "\n")

print("PROMPTS.md 生成完成：%d 节，%d 字符" % (len(files), len(text)))
