# -*- coding: utf-8 -*-
"""逐个文件比对本地 blob sha 与 GitHub 远端 blob sha，验证推送完整性。"""
import json
import subprocess
import sys

REPO = "A13612812330/GH-Handover"
CWD = r"C:\Users\komo\WorkBuddy\本机\GH-Handover"

# 本地：git ls-tree -r HEAD
# 必须关掉 core.quotepath，否则中文路径会被转义成 "\346\200\273..." 导致误判缺失
local = {}
out = subprocess.run(
    ["git", "-C", CWD, "-c", "core.quotepath=false", "ls-tree", "-r", "HEAD"],
    capture_output=True, text=True, encoding="utf-8"
).stdout
for line in out.splitlines():
    meta, path = line.split("\t", 1)
    local[path] = meta.split()[2]

# 远端：GitHub tree API（含 blob sha）
remote_raw = subprocess.run(
    ["gh", "api", "repos/%s/git/trees/main?recursive=1" % REPO],
    capture_output=True, text=True, encoding="utf-8"
).stdout
tree = json.loads(remote_raw)
remote = {n["path"]: n["sha"] for n in tree.get("tree", []) if n["type"] == "blob"}

ok = diff = missing = 0
for path in sorted(set(local) | set(remote)):
    l, r = local.get(path), remote.get(path)
    if l is None:
        print("EXTRA-REMOTE %s" % path)
        diff += 1
    elif r is None:
        print("MISSING-REMOTE %s" % path)
        missing += 1
    elif l != r:
        print("SHA-DIFF %s local=%s remote=%s" % (path, l[:10], r[:10]))
        diff += 1
    else:
        ok += 1

print("\n本地文件 %d 个 / 远端 blob %d 个" % (len(local), len(remote)))
print("一致 %d / 不一致 %d / 远端缺失 %d" % (ok, diff, missing))
sys.exit(0 if diff == 0 and missing == 0 else 1)
