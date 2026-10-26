# -*- coding: utf-8 -*-
"""给 GHZS-Project 下的仓库统一补 MIT LICENSE。

用法：
    python tools/add-license.py --dry-run   # 只看每个仓库会做什么
    python tools/add-license.py --apply     # 真正写入

原则：
1. 幂等 —— 内容已一致就 SKIP，不产生空提交。
2. LICENSE 必须是 21 行标准 MIT 原文，**不能追加任何中文说明**，
   否则 GitHub 的识别引擎会判 NOASSERTION（GH-Gamehub 就是这么坏掉的）。
   附加声明单独放 NOTICE.md。
3. 署名统一为 `GHZS-Project`（仓库归属组织，交接后不随个人账号变化）。
"""

import base64
import json
import subprocess
import sys
import urllib.error
import urllib.request

ORG = "GHZS-Project"
HOLDER = "GHZS-Project"
YEAR = "2026"

MIT = """MIT License

Copyright (c) {year} {holder}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""".format(year=YEAR, holder=HOLDER)

# GH-Gamehub 原先塞在 LICENSE 末尾的中文声明，移到 NOTICE.md
GAMEHUB_NOTICE = """# 内容来源声明

本仓库的 MIT 许可证（见 [LICENSE](LICENSE)）覆盖仓库内的**代码**。

关于游戏内容：本仓库只包含「标题 / 封面地址 / 分类 / 体积 / 热度」等索引信息与指向源站的链接，
不包含任何游戏本体、破解文件或安装包。所有内容的版权归各自权利人与原站
（jidiyouxi.com / xdgame.com）所有。

如需删除某条记录，请在 Issues 中提出，维护者会从 `data/*.json` 中移除。
"""

# 全部 11 个仓库：是否需要写 LICENSE、是否需要写 NOTICE
REPOS = [
    "GH-Handover",
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

TOKEN = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()
if not TOKEN:
    sys.exit("拿不到 gh token，先 gh auth login")


def api(path, method="GET", payload=None):
    url = "https://api.github.com" + path
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "license-sync")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            body = r.read().decode()
            return r.status, (json.loads(body) if body.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, {"message": e.read().decode()[:200]}


def get_file(repo, name):
    code, d = api("/repos/%s/%s/contents/%s" % (ORG, repo, name))
    if code != 200:
        return None, None
    return base64.b64decode(d["content"]).decode("utf-8", "replace"), d["sha"]


def put_file(repo, name, text, sha, msg):
    payload = {
        "message": msg,
        "content": base64.b64encode(text.encode()).decode(),
    }
    if sha:
        payload["sha"] = sha
    return api("/repos/%s/%s/contents/%s" % (ORG, repo, name), "PUT", payload)


def norm(s):
    return (s or "").replace("\r\n", "\n").strip()


def main():
    apply = "--apply" in sys.argv
    ok = skip = fail = 0
    for repo in REPOS:
        cur, sha = get_file(repo, "LICENSE")
        action = "CREATE"
        if cur is not None:
            if norm(cur) == norm(MIT):
                action = "SKIP"
            elif repo == "GH-Gamehub":
                action = "FIX-APPENDIX"  # 拆出中文附录
            else:
                action = "RESIGN"  # 旧署名换掉

        line = "%-26s %-13s" % (repo, action)
        if action == "SKIP":
            skip += 1
            print(line + "已一致")
            continue
        if not apply:
            print(line + "（待写入）")
            ok += 1
            continue

        msg = "docs: 采用 MIT 许可证" if action == "CREATE" else "docs: LICENSE 规范为标准 MIT（署名统一 GHZS-Project）"
        code, res = put_file(repo, "LICENSE", MIT, sha, msg)
        if code in (200, 201):
            ok += 1
            print(line + "OK commit " + res.get("commit", {}).get("sha", "")[:7])
        else:
            fail += 1
            print(line + "FAIL %s %s" % (code, res.get("message", "")[:100]))

        # Gamehub：把中文声明搬到 NOTICE.md
        if repo == "GH-Gamehub":
            ncur, nsha = get_file(repo, "NOTICE.md")
            if ncur and norm(ncur) == norm(GAMEHUB_NOTICE):
                print("%-26s %-13s已一致" % ("  └ NOTICE.md", "SKIP"))
            else:
                c2, r2 = put_file(
                    repo, "NOTICE.md", GAMEHUB_NOTICE, nsha, "docs: 内容来源声明从 LICENSE 拆到 NOTICE"
                )
                print("%-26s %-13s%s" % ("  └ NOTICE.md", "OK" if c2 in (200, 201) else "FAIL", c2))

    print()
    print("%s：写入 %d / 跳过 %d / 失败 %d" % ("已应用" if apply else "预演", ok, skip, fail))


if __name__ == "__main__":
    main()
