# GH 系列项目 · 交接总入口

> 账号：`A13612812330`　·　共 **10 个** `GH-` 前缀仓库　·　全部已公开
> 本页是所有 GH 项目的唯一入口。想快速上手，看[第 2 节](#2-拿到就跑最快的三个)；想让 AI Agent 干活，复制 [PROMPTS.md](PROMPTS.md) 里的段落。
>
> 🔗 **双向可达**：10 个仓库的 README 顶部都已挂上回到本页的链接，从任何一个仓库都能找回总目录。

---

## 1. 十个项目一览

### A. 游戏内容与聚合（6 个）

| # | 项目 | 是什么 | 形态 | 上手难度 |
|---|---|---|---|---|
| 1 | [`GH-Gamehub`](https://github.com/A13612812330/GH-Gamehub) | 单机游戏聚合站：机地 + XDGAME 的游戏、MOD、存档、修改器、模拟器配置，共 6 页，带管理后台 | Node 服务（8123） | ⚠️ 装一次依赖 |
| 2 | [`GH-GameGather-APP`](https://github.com/A13612812330/GH-GameGather-APP) | PC/手游情报站 + 资源索引 + aria2 下载的 **Electron 桌面成品** | 桌面 App | ✅ 开箱即用 |
| 3 | [`GH-GameGather-UPSTREAM`](https://github.com/A13612812330/GH-GameGather-UPSTREAM) | 第 2 项的**配套数据服务**：Express + 15 个抓取器 + 93.6 MB JSON 索引快照 | Node 服务 | ⚠️ 装一次依赖 |
| 4 | [`GH-GameNews`](https://github.com/A13612812330/GH-GameNews) | 资讯采集 → 今日简讯 → 日报/周报海报 → 飞书投递，对接 7 个平台，含定时调度 | React + Express | ⚠️ 装一次依赖 |
| 5 | [`GH-NewGameWIki`](https://github.com/A13612812330/GH-NewGameWIki) | 游戏资讯 / 活动 / **排期**管理，8 个平台采集 → SQLite → 后台 | React + Vite + Express（64111） | ⚠️ 装一次依赖 |
| 6 | [`GH-GameSearch`](https://github.com/A13612812330/GH-GameSearch) | 内部 Android 游戏信息查询 App，按后台账号权限读数据 | Android APK | ✅ 开箱即用 |

### B. 运营与数据工具（3 个）

| # | 项目 | 是什么 | 形态 | 上手难度 |
|---|---|---|---|---|
| 7 | [`GH-Game-Puton`](https://github.com/A13612812330/GH-Game-Puton) | Windows **游戏后台上架批量导入**工具（Electron），填 `and-admin.ghzs.com` 已授权后台 | 桌面 App | 🔶 需自己打包 |
| 8 | [`GH-CloudGame`](https://github.com/A13612812330/GH-CloudGame) | 端游云游戏**三源周报**可复刻工程（神策搜索 / 鲸云下载 / SteamDB 销量），含脚本、词库、口径与 4 期产出 | Python 流水线 | ✅ 开箱即用 |
| 9 | [`GH-WeeklyReport`](https://github.com/A13612812330/GH-WeeklyReport) | Excel 周报分析：当周 / 跨周汇总 / 收益汇总 / 趋势图 | 零依赖 Node（8787） | ✅ 开箱即用 |

### C. 通用方法论（1 个）

| # | 项目 | 是什么 | 形态 | 上手难度 |
|---|---|---|---|---|
| 10 | [`GH-KomoSkill`](https://github.com/A13612812330/GH-KomoSkill) | **AI 协作工作法技能包**（非业务工具）：六阶段门禁 + 证据纪律 + 防失忆，Codex / WorkBuddy / Claude 通用 | Python 脚本 | ✅ 开箱即用 |

---

## 2. 拿到就跑：最快的三个

如果你只有 10 分钟，先跑这三个，能立刻看到东西：

```bash
# 1. 云端三源周报 —— 不需要任何密钥，仓库自带两期真实样例
git clone https://github.com/A13612812330/GH-CloudGame.git && cd GH-CloudGame
pip install -r requirements.txt && npm i jsdom
cd pipeline && python 09_run_all.py        # 约 104 秒，产出看板 + Excel

# 2. 周报分析工具 —— 零依赖
git clone https://github.com/A13612812330/GH-WeeklyReport.git && cd GH-WeeklyReport
node server/server.mjs                      # 打开 http://127.0.0.1:8787

# 3. 技能包自检 —— 零依赖
git clone https://github.com/A13612812330/GH-KomoSkill.git && cd GH-KomoSkill
python scripts/doctor.py                    # 8 项检查
```

> 已有在线可看：**Gamehub** https://gamehub-agg-v4.app.workbuddy.host/ ｜ **GameGather-APP** 装 Release 包

---

## 3. 可用性总表（实测，非根据文档推断）

| 级别 | 项目 | 实测证据 | 你需要自备 |
|---|---|---|---|
| ✅ | **GH-CloudGame** | `09_run_all.py` 9 步 **104.2s** 跑完，`08` 门禁 `ERROR 0 · WARN 0 → PASS` | 无（自带样例数据） |
| ✅ | **GH-WeeklyReport** | `PORT=18787 node server/server.mjs` → `200`，**零依赖** | 自己的周报 Excel |
| ✅ | **GH-KomoSkill** | `doctor.py` 8 项全 `OK` | 无 |
| ✅ | **GH-GameSearch** | `dist/GH-GameSearch.apk`（890,470 B）可直接安装 | 后台账号（App 内登录） |
| ✅ | **GH-GameGather-APP** | Release `v28`（262 MB）；`demo/index.html` 双击即看 | 无 |
| ⚠️ | **GH-Gamehub** | 依赖仅 **3 个**，带 `npm run doctor` 自检 | `npm i` + 自行初始化管理员 |
| ⚠️ | **GH-GameGather-UPSTREAM** | 依赖 **3 个**，`npm start` | `npm i` |
| ⚠️ | **GH-NewGameWIki** | 有 `.env.example`，**无必填密钥** | `npm i`（Firecrawl key 可选） |
| ⚠️ | **GH-GameNews** | 9 个依赖 + `.env.example` | `npm i`（飞书密钥仅推送功能需要） |
| 🔶 | **GH-Game-Puton** | **无 Release**（API 实测 0 个） | `npm i` + `npm run 打包exe` + 后台账号 |

**结论：5 个开箱即用，4 个装一次依赖即可，1 个需要自己打包。没有任何项目需要申请 API 密钥才能跑起来。**

---

## 4. 仓库里没有的东西（重要）

这些是按设计**刻意排除**的，不要找，也不要让 AI 去猜：

| 缺什么 | 影响哪些项目 | 怎么办 |
|---|---|---|
| 账号 / 密码 / Token | 全部 | 由使用者自己登录或初始化 |
| 飞书 App ID / Secret / Chat ID | GameNews | 只影响推送；不填仍可采集与生成海报 |
| 公司后台凭据（`and-admin.ghzs.com`） | Game-Puton、GameSearch | 在界面内手动登录 |
| `.env` / `*.key` / `*.pem` / `*.db` | 全部 | `.gitignore` 已排除，历史提交也已核查干净 |
| 成品打包文件 | Game-Puton | 自己 `npm run 打包exe` |

**2026-10-26 做过全量密钥审计**：扫描 10 个仓库全部文本文件（飞书 Secret/Webhook、GitHub Token、OpenAI、AWS、Google、Slack、Bearer、硬编码 password），**0 条真实密钥**；`GH-CloudGame` 5 个历史提交的文件清单也逐条查过，干净。详见 [HANDOVER.md](HANDOVER.md)。

---

## 5. 让 AI Agent 接手

| 你想做什么 | 复制这段 |
|---|---|
| 让 AI 先摸清全部 10 个项目再决定从哪下手 | [`prompts/00-总览.md`](prompts/00-总览.md) |
| 跑通云端三源周报 | [`prompts/01-CloudGame.md`](prompts/01-CloudGame.md) |
| 用周报工具分析自己的数据 | [`prompts/02-WeeklyReport.md`](prompts/02-WeeklyReport.md) |
| 装技能包 / 规范 AI 协作流程 | [`prompts/03-KomoSkill.md`](prompts/03-KomoSkill.md) |
| 起 Gamehub 聚合站 | [`prompts/04-Gamehub.md`](prompts/04-Gamehub.md) |
| 用桌面成品 / 起数据服务 | [`prompts/05-GameGather.md`](prompts/05-GameGather.md) |
| 改 Android 查询 App | [`prompts/06-GameSearch.md`](prompts/06-GameSearch.md) |
| 配资讯采集与日报 | [`prompts/07-GameNews.md`](prompts/07-GameNews.md) |
| 起排期管理后台 | [`prompts/08-NewGameWIki.md`](prompts/08-NewGameWIki.md) |
| 打包后台上架工具 | [`prompts/09-Game-Puton.md`](prompts/09-Game-Puton.md) |

全部段落的合集版：[**PROMPTS.md**](PROMPTS.md)（一个文件，直接搜索项目名）

### 通用的三条红线（每段 prompt 都复述了）

1. **不许猜凭据** —— 找不到就停下来问人，不要编造 Token / 密码 / Key，不要硬编码进代码。
2. **先自检再动手** —— 有 `doctor` / `setup-check` / `09_run_all` 的，先跑它们，通过之后再改代码。
3. **改动前先备份、先说明** —— 不要 `rm -rf`、不要 `git push --force`、不要改与本任务无关的仓库。

---

## 6. 目录说明

```
GH-Handover/
├── README.md         ← 你正在看的入口页
├── PROMPTS.md        ← 10 段 agent prompt 合集（复制用）
├── HANDOVER.md       ← 审计结论、实测记录、遗留待办
├── prompts/          ← 每段 prompt 单独成文件，有独立链接
│   ├── 00-总览.md
│   ├── 01-CloudGame.md
│   ├── 02-WeeklyReport.md
│   ├── 03-KomoSkill.md
│   ├── 04-Gamehub.md
│   ├── 05-GameGather.md
│   ├── 06-GameSearch.md
│   ├── 07-GameNews.md
│   ├── 08-NewGameWIki.md
│   └── 09-Game-Puton.md
└── tools/            ← 维护脚本（一般不用碰）
    ├── build-prompts.py   # 由 prompts/ 重新生成 PROMPTS.md（幂等）
    ├── add-backlink.py    # 给 10 个仓库 README 加总入口链接（幂等）
    └── verify-remote.py   # 逐文件比对本地与远端 blob sha
```

改了 `prompts/` 里的内容之后，跑一次 `python tools/build-prompts.py` 重新生成合集，再提交。

### 自检命令

```bash
python tools/verify-remote.py        # 校验本仓库推送完整性（逐文件 blob sha）
python tools/add-backlink.py --dry-run   # 检查 10 个仓库是否都已挂上总入口
```


---

## 7. 已知遗留（不影响接手）

| # | 事项 | 影响 |
|---|---|---|
| 1 | `GH-CloudGame` README 写「jsdom 不装也行」，**实测是直接中止** | 必须装 jsdom，已在本页第 2 节写成必装步骤 |
| 2 | `GH-GameNews` 仓库 177 MB（历史归档大文件） | 首次 clone 慢 |
| 3 | `GH-Game-Puton` 无 Release 成品 | 需自己打包 |
| 4 | 6 个仓库无 LICENSE 文件 | 内部交接无碍；对外发布需补 |
| 5 | 10 个仓库均未启用 GitHub Pages | 网页版需本地起服务 |

---

*最后核对：2026-10-26 14:50（北京时间）*
