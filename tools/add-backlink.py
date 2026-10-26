# -*- coding: utf-8 -*-
"""给 10 个 GH 仓库的 README 顶部插入「总入口」反向链接。

走 GitHub Contents API 直接提交，不 clone，避免大仓库网络问题。
脚本幂等：README 里已有总入口链接则跳过。

用法：
    python tools/add-backlink.py --dry-run    # 只看会改哪些
    python tools/add-backlink.py --apply      # 真正提交
"""
import base64
import json
import subprocess
import sys

OWNER = "A13612812330"
HANDOVER = "GH-Handover"
MARK = "GH-Handover"

REPOS = [
    "GH-Gamehub",
    "GH-GameGather-APP",
    "GH-GameGather-UPSTREAM",
    "GH-GameNews",
    "GH-NewGameWIki",
    "GH-GameSearch",
    "GH-Game-Puton",
    "GH-CloudGame",
    "GH-WeeklyReport",
    "GH-KomoSkill",
]

BLOCK = (
    "> 📚 **本文档属于 GH 系列交接项目。** 总入口（全部 10 个仓库索引、"
    "可用性实测、可复制的 AI Agent prompt）："
    "https://github.com/%s/%s\n" % (OWNER, HANDOVER)
)


def gh(args, stdin=None):
    p = subprocess.run(
        ["gh"] + args, capture_output=True, text=True, encoding="utf-8", input=stdin
    )
    return p.returncode, p.stdout, p.stderr


def get_readme(repo):
    rc, out, err = gh(["api", "repos/%s/%s/contents/README.md" % (OWNER, repo)])
    if rc != 0:
        return None, None, err.strip()[:120]
    d = json.loads(out)
    content = base64.b64decode(d["content"]).decode("utf-8")
    return content, d["sha"], None


def insert_block(text):
    """在第一个 '# ' 标题行之后（含其后紧跟的空行之前）插入引用块。"""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            # 跳过标题后已有的空行，插在标题行下方空一行处
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            new = lines[:i + 1] + ["", BLOCK.rstrip("\n"), ""] + lines[j:]
            return "\n".join(new)
    # 没有一级标题：放最前面
    return BLOCK + "\n" + text


def main():
    apply = "--apply" in sys.argv
    results = []
    for repo in REPOS:
        content, sha, err = get_readme(repo)
        if content is None:
            results.append((repo, "SKIP", "读取失败: %s" % err))
            print("[SKIP] %-26s 读取失败: %s" % (repo, err))
            continue
        if MARK in content:
            results.append((repo, "SKIP", "已含总入口链接"))
            print("[SKIP] %-26s 已含总入口链接，跳过" % repo)
            continue

        new = insert_block(content)
        if not apply:
            results.append((repo, "DRY", "将插入 %d 字符" % len(BLOCK)))
            print("[DRY ] %-26s 将插入反向链接（当前 %d 字节）" % (repo, len(content)))
            continue

        payload = json.dumps({
            "message": "docs: 顶部加 GH 系列交接总入口链接",
            "content": base64.b64encode(new.encode("utf-8")).decode("ascii"),
            "sha": sha,
        }, ensure_ascii=False)
        rc, out, err2 = gh(
            ["api", "-X", "PUT", "repos/%s/%s/contents/README.md" % (OWNER, repo),
             "--input", "-"],
            stdin=payload,
        )
        if rc == 0:
            d = json.loads(out)
            c = d["commit"]["sha"][:7]
            results.append((repo, "OK", c))
            print("[ OK ] %-26s 提交 %s" % (repo, c))
        else:
            msg = (err2 or out).strip().replace("\n", " ")[:110]
            results.append((repo, "FAIL", msg))
            print("[FAIL] %-26s %s" % (repo, msg))

    print("\n=== 汇总 ===")
    for kind in ("OK", "DRY", "SKIP", "FAIL"):
        n = sum(1 for r in results if r[1] == kind)
        if n:
            print("%s: %d" % (kind, n))
    return 0 if not any(r[1] == "FAIL" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
