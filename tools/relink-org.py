# -*- coding: utf-8 -*-
"""仓库转移到组织后，把所有文档里的旧归属链接改成新的。

替换规则（精确，不做模糊匹配）：
    A13612812330/GH  ->  <org>/GH

覆盖范围：
  1. 本仓库（GH-Handover）内的 .md / .py
  2. 其余 10 个仓库的 README.md（走 Contents API，不 clone）
  3. 本地 git remote URL

跳过：tools/migrate-to-org.py（它的 SOURCE 常量必须保留原账号，否则无法再跑）

用法：
    python tools/relink-org.py --org GHZS              # 干跑，只报告
    python tools/relink-org.py --org GHZS --local      # 只改本地
    python tools/relink-org.py --org GHZS --remote     # 只改 10 个远端 README
    python tools/relink-org.py --org GHZS --remote --apply
"""
import base64
import io
import json
import os
import subprocess
import sys

OLD = "A13612812330/GH"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_FILES = {"migrate-to-org.py", "relink-org.py"}

PEERS = [
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


def arg(name, default=None):
    if name in sys.argv:
        i = sys.argv.index(name)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


def gh(args, stdin=None):
    p = subprocess.run(
        ["gh"] + args, capture_output=True, text=True, encoding="utf-8", input=stdin
    )
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def do_local(org, apply):
    new = "%s/GH" % org
    changed = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for fn in files:
            if not fn.endswith((".md", ".py")):
                continue
            if fn in SKIP_FILES:
                continue
            path = os.path.join(root, fn)
            with io.open(path, encoding="utf-8") as fh:
                text = fh.read()
            n = text.count(OLD)
            if n == 0:
                continue
            rel = os.path.relpath(path, BASE).replace("\\", "/")
            print("  [LOCAL] %-32s 替换 %d 处" % (rel, n))
            changed.append(rel)
            if apply:
                with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(text.replace(OLD, new))

    # git remote
    rc, cur, _ = gh(["config", "--get", "remote.origin.url"]) if False else (0, "", "")
    p = subprocess.run(
        ["git", "-C", BASE, "remote", "get-url", "origin"],
        capture_output=True, text=True, encoding="utf-8",
    )
    old_url = p.stdout.strip()
    new_url = old_url.replace("A13612812330/", "%s/" % org)
    if old_url and old_url != new_url:
        print("  [REMOTE] %s\n        -> %s" % (old_url, new_url))
        if apply:
            subprocess.run(
                ["git", "-C", BASE, "remote", "set-url", "origin", new_url], check=False
            )
    return changed


def do_remote(org, apply):
    new = "%s/GH" % org
    ok = skip = fail = 0
    for repo in PEERS:
        full = "%s/%s" % (org, repo)
        rc, out, err = gh(["api", "repos/%s/contents/README.md" % full])
        if rc != 0:
            print("  [FAIL] %-26s 读取失败: %s" % (repo, err[:90]))
            fail += 1
            continue
        d = json.loads(out)
        text = base64.b64decode(d["content"]).decode("utf-8")
        n = text.count(OLD)
        if n == 0:
            print("  [SKIP] %-26s 已是新链接" % repo)
            skip += 1
            continue
        print("  [UPDATE] %-26s 替换 %d 处" % (repo, n))
        if not apply:
            ok += 1
            continue
        payload = json.dumps({
            "message": "docs: 仓库已迁移到 %s，同步链接" % org,
            "content": base64.b64encode(
                text.replace(OLD, new).encode("utf-8")).decode("ascii"),
            "sha": d["sha"],
        }, ensure_ascii=False)
        rc2, out2, err2 = gh(
            ["api", "-X", "PUT", "repos/%s/contents/README.md" % full, "--input", "-"],
            stdin=payload,
        )
        if rc2 == 0:
            c = json.loads(out2)["commit"]["sha"][:7]
            print("           → 提交 %s" % c)
            ok += 1
        else:
            print("           → 失败 %s" % (err2 or out2)[:100])
            fail += 1
    print("\n远端 README：更新 %d / 跳过 %d / 失败 %d" % (ok, skip, fail))
    return fail


def main():
    org = arg("--org", "GHZS")
    apply = "--apply" in sys.argv
    only_local = "--local" in sys.argv
    only_remote = "--remote" in sys.argv

    print("旧归属：%s…    新归属：%s/GH…\n" % (OLD, org))

    if not only_remote:
        print("=== 本地文档 ===")
        ch = do_local(org, apply)
        print("本地改动文件 %d 个%s\n" % (len(ch), "" if apply else "（干跑，未写入）"))

    if not only_local:
        print("=== 远端 README（10 个）===")
        fail = do_remote(org, apply)

    if apply and not only_remote:
        print("\n下一步：cd %s && git add -A && git commit && git push" % BASE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
