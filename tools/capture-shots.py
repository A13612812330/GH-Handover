# -*- coding: utf-8 -*-
"""重新抓取门户页用的项目截图（截图会写进 shots/*.webp）。

依赖：pip install playwright pillow  &&  playwright install chromium

用法：
    python tools/capture-shots.py              # 全部重抓
    python tools/capture-shots.py 01 09        # 只抓编号匹配的
    python tools/capture-shots.py --list       # 看清单和前置条件

前置条件分三种（脚本会跳过跑不起来的，并打印原因）：
  A. 本机要先把服务跑起来：8123 GameHub / 64111 NewGameWiki / 64423 GameNews / 8787 WeeklyReport
  B. 仓库内的静态页：需要先把对应仓库 clone 到本地，用环境变量指向它
       SET GH_GAMEGATHER_APP=D:\\path\\GH-GameGather-APP
       SET GH_GAMEGATHER_UPSTREAM=D:\\path\\GH-GameGather-UPSTREAM
       SET GH_GAME_PUTON=D:\\path\\GH-Game-Puton
       SET GH_CLOUDGAME=D:\\path\\GH-CloudGame
     （GameGather-APP / Game-Puton 的页面用绝对路径引用 /style.css 之类，脚本会自动起一个临时静态服务）
  C. GameSearch 的截图来自 App 原型页 prototype.html，放 GH_GAMESEARCH_PROTO 指向它；
     KomoSkill 的截图是 doctor.py 真实输出的终端卡片，先跑 tools/make-terminal.py 生成页面再用 GH_KOMOSKILL_TERM 指向它。

截图规格：桌面 1440x900（少数 1320x860），手机 390x844；导出 WebP 宽度上限 1400、质量 88。
"""
import http.server
import os
import pathlib
import socketserver
import sys
import threading

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
DST = ROOT / "shots"
RAW = ROOT / "_shots_raw"
RAW.mkdir(exist_ok=True)
DST.mkdir(exist_ok=True)

ENV = os.environ


def dir_of(var):
    v = ENV.get(var)
    if not v:
        return None
    p = pathlib.Path(v)
    return p if p.exists() else None


def serve(directory, port):
    """给引用绝对路径(/style.css)的页面起个临时静态服务。"""
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(  # noqa: E731
        *a, directory=str(directory), **kw
    )
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def file_uri(p):
    return pathlib.Path(p).resolve().as_uri()


def build_targets():
    app = dir_of("GH_GAMEGATHER_APP")
    up = dir_of("GH_GAMEGATHER_UPSTREAM")
    puton = dir_of("GH_GAME_PUTON")
    cloud = dir_of("GH_CLOUDGAME")
    proto = dir_of("GH_GAMESEARCH_PROTO")
    term = dir_of("GH_KOMOSKILL_TERM")

    t = [
        # name, url, w, h, wait_ms, click, 前置说明
        ("01-newgamewiki", "http://127.0.0.1:64111/", 1440, 900, 2500, None, "NewGameWiki 服务 :64111"),
        ("02-gamenews", "http://127.0.0.1:64423/", 1440, 900, 12000, None, "GameNews 前端 :64423 + 后端 :64424"),
        ("03-gamehub", "https://gamehub-agg-v4.app.workbuddy.host/", 1440, 900, 12000, None, "GameHub 线上站"),
        ("04-gamegather-app", file_uri(app / "demo/index.html") if app else "", 1320, 860, 2000, None, "GH_GAMEGATHER_APP/demo/index.html"),
        ("05-gamegather-upstream", "http://127.0.0.1:8123/admin.html", 1440, 900, 6000, None, "GameHub 服务 :8123（同端口提供 admin.html）"),
        ("06-gameputon", "http://127.0.0.1:18803/", 1320, 860, 2500, None, "GH_GAME_PUTON/页面（临时静态服务 18803）"),
        ("07-weeklyreport", "http://127.0.0.1:8787/", 1440, 900, 2500, None, "WeeklyReport 服务 :8787"),
        ("08-gamesearch", file_uri(proto / "prototype.html") if proto else "", 390, 844, 1200, "模拟已登录", "GH_GAMESEARCH_PROTO/prototype.html"),
        ("09-cloudgame", file_uri(cloud / "outputs/2026-10-12/端游三源周报看板_9.28-10.11.html") if cloud else "", 1440, 900, 2500, None, "GH_CLOUDGAME 里任一期看板 HTML"),
        ("10-komoskill", file_uri(term / "komoskill-terminal.html") if term else "", 1180, 880, 900, None, "tools/make-terminal.py 生成的终端卡片"),
    ]
    return t


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    targets = build_targets()
    if "--list" in sys.argv:
        for n, _u, w, h, _w2, _c, note in targets:
            print("%-24s %-28s %s" % (n, "%dx%d" % (w, h), note))
        return

    if any(n[0].startswith("06") for n in targets):
        puton = dir_of("GH_GAME_PUTON")
        if puton:
            serve(puton / "页面", 18803)

    done = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, url, w, h, wait, click, note in targets:
            if args and not any(a in name for a in args):
                continue
            if not url:
                print("[SKIP] %-24s 缺少路径：%s" % (name, note))
                continue
            ctx = b.new_context(viewport={"width": w, "height": h}, locale="zh-CN", ignore_https_errors=True)
            pg = ctx.new_page()
            try:
                pg.goto(url, wait_until="load", timeout=45000)
                pg.wait_for_timeout(wait)
                if click:
                    pg.get_by_text(click, exact=False).first.click(timeout=5000)
                    pg.wait_for_timeout(1200)
            except Exception as e:  # noqa: BLE001
                print("[SKIP] %-24s %s（%s）" % (name, str(e)[:90], note))
                ctx.close()
                continue
            png = RAW / (name + ".png")
            pg.screenshot(path=str(png))
            im = Image.open(png).convert("RGB")
            if im.width > 1400:
                im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
            out = DST / (name + ".webp")
            im.save(out, "WEBP", quality=88, method=6)
            done += 1
            print("[OK]   %-24s -> shots/%s  %.0f KB" % (name, out.name, out.stat().st_size / 1024))
            ctx.close()
        b.close()
    print("完成 %d 张。原图（PNG）在 _shots_raw/，只提交 shots/*.webp。" % done)


if __name__ == "__main__":
    main()
