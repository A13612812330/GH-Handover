# -*- coding: utf-8 -*-
"""把 11 个 GH 仓库从个人账号转移到组织（默认 GHZS）。

转移是异步的（API 返回 202），脚本会轮询直到目标位置可读。
commit sha 不变 —— 转移不改内容，只在仓库归属层面换位置。

用法：
    python tools/migrate-to-org.py --org GHZS --dry-run
    python tools/migrate-to-org.py --org GHZS --apply
"""
import json
import subprocess
import sys
import time

SOURCE = "A13612812330"
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


def gh(args, stdin=None):
    p = subprocess.run(
        ["gh"] + args, capture_output=True, text=True, encoding="utf-8", input=stdin
    )
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def arg(name, default=None):
    if name in sys.argv:
        i = sys.argv.index(name)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


def repo_exists(full):
    rc, out, _ = gh(["api", "repos/" + full, "--jq", ".full_name"])
    return rc == 0 and out


def main():
    org = arg("--org", "GHZS")
    apply = "--apply" in sys.argv

    # 前置：目标组织必须已存在
    rc, out, err = gh(["api", "orgs/" + org, "--jq", ".login"])
    if rc != 0:
        print("[中止] 组织 %s 不存在或无权读取：%s" % (org, err[:160]))
        print("       请先在 https://github.com/account/organizations/new?plan=free 创建")
        return 2
    print("目标组织：%s ✓\n" % out)

    ok, skip, fail = [], [], []
    for repo in REPOS:
        src = "%s/%s" % (SOURCE, repo)
        dst = "%s/%s" % (org, repo)

        if repo_exists(dst):
            print("[SKIP] %-26s 已在 %s" % (repo, org))
            skip.append(repo)
            continue
        if not repo_exists(src):
            print("[FAIL] %-26s 源仓库不存在" % repo)
            fail.append((repo, "源仓库不存在"))
            continue

        if not apply:
            print("[DRY ] %-26s 将转移到 %s" % (repo, org))
            ok.append(repo)
            continue

        payload = json.dumps({"new_owner": org})
        rc, out, err = gh(
            ["api", "-X", "POST", "repos/%s/transfer" % src, "--input", "-"],
            stdin=payload,
        )
        if rc != 0:
            print("[FAIL] %-26s %s" % (repo, (err or out)[:130]))
            fail.append((repo, (err or out)[:130]))
            continue

        # 轮询：目标位置可读即视为完成（最多等 60 秒）
        done = False
        for _ in range(20):
            if repo_exists(dst):
                done = True
                break
            time.sleep(3)
        if done:
            print("[ OK ] %-26s → %s" % (repo, dst))
            ok.append(repo)
        else:
            print("[WAIT] %-26s 已提交转移，但 60 秒内未在目标可见，稍后复查" % repo)
            ok.append(repo)

    print("\n=== 汇总 ===")
    print("成功/已提交: %d   跳过: %d   失败: %d" % (len(ok), len(skip), len(fail)))
    for r, m in fail:
        print("  失败 %s: %s" % (r, m))
    print("\n下一步：跑 tools/relink-org.py --org %s --apply 更新所有文档链接" % org)
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
