# GH 系列 · AI Agent Prompt 合集

> 每一节都是一段**完整可复制**的 prompt。复制代码块里的整段文字发给任意 AI 即可。

> 想单独拿某一个项目的链接：点下表右列。总览与可用性判定见 [README.md](README.md)。


## 三条通用红线（每段 prompt 里都已复述）

1. **不许猜凭据** —— 找不到就停下问人，不编造 Token / 密码 / Key，不硬编码进代码。
2. **先自检再动手** —— 有 `doctor` / `setup-check` / `09_run_all` 的，先跑它们，通过后再改代码。
3. **改动前先备份、先说明** —— 不 `rm -rf`、不 `git push --force`、不改无关仓库。


## 索引

| 段 | 适用场景 | 单独链接 |
|---|---|---|
| `00-总览` | 刚接手 / 不知道从哪开始 | [打开](prompts/00-总览.md) |
| `01-CloudGame` | 跑通三源周报流水线 | [打开](prompts/01-CloudGame.md) |
| `02-WeeklyReport` | 分析自己的周报 Excel | [打开](prompts/02-WeeklyReport.md) |
| `03-KomoSkill` | 装 AI 协作规范 | [打开](prompts/03-KomoSkill.md) |
| `04-Gamehub` | 起游戏聚合站 | [打开](prompts/04-Gamehub.md) |
| `05-GameGather` | 用桌面成品 / 起数据服务 | [打开](prompts/05-GameGather.md) |
| `06-GameSearch` | 看懂或重编 Android App | [打开](prompts/06-GameSearch.md) |
| `07-GameNews` | 配资讯采集与日报 | [打开](prompts/07-GameNews.md) |
| `08-NewGameWIki` | 起排期管理后台 | [打开](prompts/08-NewGameWIki.md) |
| `09-Game-Puton` | 打包后台上架工具 | [打开](prompts/09-Game-Puton.md) |

---

## 00 · 总览 —— 让 AI 先摸清全部项目再动手

**什么时候用**：刚接手、不知道从哪开始、想先要一份"我该先跑哪个"的判断。

**用法**：把下面整段复制，连同 `https://github.com/A13612812330/GH-Handover` 一起发给 AI。

---

### 可复制 prompt

```text
我要接手一批 GitHub 项目，账号 A13612812330 下所有 GH- 开头的仓库，共 10 个。
交接总入口在这里：https://github.com/A13612812330/GH-Handover

请先做三件事，全部做完再问我下一步，中间不要改任何文件：

一、通读交接页
1. 读 GH-Handover 仓库的 README.md、PROMPTS.md、HANDOVER.md
2. 整理出一张表：项目名 / 一句话用途 / 运行形态 / 上手难度 / 需要我自备什么
3. 把 10 个项目按"我现在最可能用得上"排个序，说明理由（我的角色是产品经理兼开发者，
   主要做游戏发行与运营，日常需要资讯采集、数据周报、后台上架）

二、检查我的本机环境
4. 报告：node -v、npm -v、python --version、git --version、java -version、adb version
5. 判断哪些项目当前环境下能直接跑，哪些缺前置条件（写成清单，不要替我安装）

三、给建议
6. 推荐 1 个项目作为"第一个跑起来"的目标，给出具体到命令的步骤
7. 指出 2 个你读完文档后仍然不确定的点，等我确认

红线：
- 不要 clone 全部 10 个仓库（有的 177MB 甚至 262MB），先只读交接页
- 不要猜测任何账号、密码、Token、API Key。文档写明仓库里没有凭据，找不到就停下来问我
- 不要执行任何 npm i / pip install，先给我清单让我确认
- 汇报用中文，表格优先，不要长篇大论
```

---

## 01 · GH-CloudGame —— 端游云游戏三源周报

**能干什么**：用神策搜索、鲸云下载、SteamDB 销量三份导出数据，跑出一份 Excel 五表 + HTML 看板周报。仓库自带两期真实样例，**不需要任何密钥就能完整跑通**。

**实测**：`09_run_all.py` 9 步 104.2 秒跑完，`08` 门禁 `ERROR 0 · WARN 0 → PASS`。

**用法**：复制下面整段发给 AI。

---

### 可复制 prompt

```text
仓库：https://github.com/A13612812330/GH-CloudGame
目标：在我本机完整跑通三源周报流水线，先跑仓库自带的样例数据，确认能出看板和 Excel。

环境：Windows，Git Bash，Node 22，Python 3.11 或 3.13。

步骤：
1. clone 到 D:\projects\GH-CloudGame（如果 D 盘没权限就换我指定的目录）
2. 先读 README.md 和 AGENT.md，把流水线 9 个步骤各自干什么用三行话讲给我听
3. 装依赖：
   - pip install -r requirements.txt（pandas / openpyxl / Pillow）
   - npm install jsdom
   ⚠️ jsdom 是必装项。README 里写"不装也能跳过"，但我实测过，
     缺 jsdom 时 08_preflight_check.py 会直接报 [环境自检未通过] 并中止，不会跳过。
4. 如果 config 不存在，用 pipeline/setup.py 生成（样例数据在 samples/，
   输出目录用 outputs/_local，期次用仓库自带的样例期次）
5. cd pipeline && python 09_run_all.py
6. 验收（必须逐条报给我实际数值，不许说"应该没问题"）：
   - 09 的退出码
   - 08 门禁的 ERROR 数和 WARN 数
   - 总耗时
   - outputs 下新生成的 HTML 看板和 Excel 的完整路径 + 文件大小
7. 把 HTML 看板的绝对路径告诉我，我要自己打开看

失败处理：
- 报错就把完整错误原文贴出来，先给根因分析再动手改，不要直接改代码试错
- 不要修改 samples/ 里的样例数据来"让流程通过"
- 不要改动口径计算逻辑（01~05 的脚本），那是业务定义，改了数就不对

红线：
- 严禁猜测或硬编码任何平台账号、Cookie、Token
- 严禁 git push 到原仓库
- 严禁删除仓库里已有的 outputs 历史产出

做完后告诉我：这套流程换成我自己的三份导出表，需要替换哪些文件、改哪个配置。
```

---

## 02 · GH-WeeklyReport —— Excel 周报分析工具

**能干什么**：把周报 Excel 变成当周汇总、跨周对比、收益汇总和趋势图，浏览器里看。**零依赖**，`node` 直接跑。

**实测**：`PORT=18787 node server/server.mjs` → HTTP 200，页面标题「周报分析」。

**用法**：复制下面整段发给 AI。

---

### 可复制 prompt

```text
仓库：https://github.com/A13612812330/GH-WeeklyReport
目标：把它跑起来，并教我怎么把手上自己的周报 Excel 喂进去。

环境：Windows，Node 22。这个项目零依赖，不需要 npm install。

步骤：
1. clone 到 D:\projects\GH-WeeklyReport
2. 读 README.md 和 HANDOFF.md，告诉我：
   - 它接受的 Excel 是什么结构（列名、sheet 名、日期格式）
   - 端口怎么改（默认 8787，我看到代码里支持 PORT 环境变量）
3. 启动：PORT=18787 node server/server.mjs（用 18787 是因为我本机 8787 被别的项目占了）
4. 验收：
   - curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18787/ 返回 200
   - 页面 <title> 是「周报分析」
   - 截图或把首屏文字贴给我
5. 然后告诉我：如果我要导入自己的 Excel，具体放在哪个目录、要不要改名、点哪个按钮

红线：
- 不要改 8787 以外的默认端口配置，我其他项目依赖它
- 不要动我本机已经在跑的 8787 服务
- 不要执行 npm install（这项目没有依赖，装了反而引入风险）

做完给我一份"三步上手"：放文件 → 启动 → 点哪里看结果。
```

---

## 03 · GH-KomoSkill —— AI 协作工作法技能包

**能干什么**：不是业务工具，是一套**让 AI 按规矩干活**的技能包：六阶段门禁（需求→方案→执行→验收→归档）、证据纪律（不许凭记忆说"已完成"）、防失忆。支持 Codex / WorkBuddy / Claude。

**实测**：`doctor.py` 8 项检查全 `OK`；`install.py --target {claude,codex,workbuddy}` 可用。

**用法**：复制下面整段发给 AI。

---

### 可复制 prompt

```text
仓库：https://github.com/A13612812330/GH-KomoSkill
目标：把这套协作规范装到我的 AI 环境里，让我以后让你干活时你按它的规矩来。

环境：Windows，Python 3.11+。

步骤：
1. clone 到 D:\projects\GH-KomoSkill
2. 读 README.md，用 5 行话讲清它到底约束了什么（不要复述目录结构，讲规则）
3. 跑自检：python scripts/doctor.py —— 把 8 项结果逐条贴给我，有 FAIL 的先解释原因
4. 告诉我 install.py 的三个目标分别装到哪里、装完之后怎么验证生效：
   - claude / codex / workbuddy（我三个环境都在用，帮我判断该装哪个，
     或者能不能三个都装、会不会冲突）
5. 先只跑 --help 和 --dry-run（如果有），把要写入的路径列给我看，
   ⚠️ 等我明确回复"可以装"之后你再真正执行安装

红线：
- 安装会往我的用户目录写文件，执行前必须把完整路径清单给我确认
- 不要覆盖我已有的 skills / 配置，遇到同名文件先停下问我
- 不要 pip install 任何东西（这项目只用标准库）

做完告诉我：装完之后，我在别的对话里怎么一句话触发它的规范。
```

---

## 04 · GH-Gamehub —— 单机游戏聚合站

**能干什么**：机地（jidiyouxi.com）+ XDGAME 的游戏、MOD、存档、修改器、模拟器配置聚合站，6 个页面 + 管理后台。

**实测**：依赖只有 3 个；自带 `npm run doctor` 自检和 `npm run handover` 交接检查；线上版 https://gamehub-agg-v4.app.workbuddy.host/ 实测 200。

**注意**：管理员账号由**使用者自己初始化**，仓库里没有、也不该有密码。

**用法**：复制下面整段发给 AI。

---

### 可复制 prompt

```text
仓库：https://github.com/A13612812330/GH-Gamehub
目标：在我本机起一个本地实例，能打开首页、能进管理后台，然后告诉我日常怎么维护。

环境：Windows，Node 22。默认端口 8123（我本机 8123 可能已被占用，先查再决定）。

步骤：
1. 先查端口：netstat -ano -p tcp | grep :8123 —— 如果被占，告诉我占用进程，不要直接杀
2. clone 到 D:\projects\GH-Gamehub，npm install（只有 3 个依赖）
3. 先跑自检：npm run doctor，把每一项结果逐条贴给我
   再跑交接检查：npm run handover
4. 启动：npm start（会监听 8123 或 PORT 指定的端口）
5. 验收：
   - 首页 HTTP 200，页面标题能取到
   - 逐个点开 6 个页面的路由，确认没有 404 或 500
   - 报给我：数据库/索引数据在哪里、多大、是一次性快照还是实时抓取
6. 管理员账号：
   - 用 npm run admin:init 初始化，账号名我稍后自己输入，密码我自己设
   - ⚠️ 你不要替我设定密码，也不要把密码写进任何文件或提交里
7. 最后告诉我：要让内容保持新鲜，是跑 pm2/计划任务定时抓，还是手动跑哪个脚本？

红线：
- 不要猜测、不要硬编码管理员账号密码；不要让我在聊天里发密码
- 不要改 .gitignore（它已经正确排除了 data/admin-account.json 等凭据文件）
- 不要 git push
- 不要动我本机正在运行的其他服务

做完给我一张运维小抄：启动 / 停服 / 看日志 / 重新抓数据 分别是哪条命令。
```

---

## 05 · GH-GameGather —— 桌面 App + 配套数据服务

**这是两个仓库，必须一起理解**：

| 仓库 | 角色 |
|---|---|
| [`GH-GameGather-APP`](https://github.com/A13612812330/GH-GameGather-APP) | 前端**桌面成品**（Electron）。Release `v28` 262 MB，解压双击 `GameIntel.exe` 就能用 |
| [`GH-GameGather-UPSTREAM`](https://github.com/A13612812330/GH-GameGather-UPSTREAM) | 后端**数据服务**：Express + 15 个抓取器 + 93.6 MB JSON 索引快照 |

**关键认知**：只 clone APP 仓库是跑不起来的（那是外壳源码）。要完整体验，装 Release 包；要改数据逻辑，起 UPSTREAM。

**用法**：复制下面整段发给 AI。

---

### 可复制 prompt

```text
我要接手一个 PC/手游情报站项目，它拆成两个仓库：
- 前端桌面 App：https://github.com/A13612812330/GH-GameGather-APP
- 后端数据服务：https://github.com/A13612812330/GH-GameGather-UPSTREAM

环境：Windows，Node 22。

目标分两条，先做第一条，做完等我确认再做第二条。

第一条：让我最快看到东西（不改代码）
1. 从 GH-GameGather-APP 的 Releases 下载 v28 成品包（262 MB）
2. ⚠️ 必须整包解压后双击目录里的 GameIntel.exe。
   只把 exe 单独拷出来会报 ICU 相关错误 —— 这个坑要在步骤里提前说明
3. 同时看一下仓库里的 demo/index.html，双击就能看到静态界面
4. 告诉我：成品包解压后多大、启动后要不要连后端、不连后端能看到什么

第二条：跑起来后端数据服务（只有我确认后才做）
5. clone GH-GameGather-UPSTREAM，npm install（3 个依赖），npm start
6. 验收：curl 访问它的首页/健康检查接口，返回 200；报给我监听端口
7. 报给我：data/ 下 93.6 MB 的 JSON 快照是哪些文件、分别是什么内容、
   是离线快照还是需要定时重新抓
8. 告诉我 15 个抓取器分别抓哪个平台、哪个是核心、哪个可以关掉

红线：
- 不要 clone APP 仓库来"自己编译"，先用 Release 成品（除非我明确要求改外壳）
- 不要改抓取器的请求频率和 UA，可能触发对方封禁
- 不要猜测任何平台的账号或 Cookie
- 不要 git push

做完给我一个判断：如果我只想用、不想维护，该停在哪一步？
```

---

## 06 · GH-GameSearch —— Android 游戏信息查询 App

**能干什么**：内部 Android App（Kotlin）。通过 WebView 登录公司后台，按**账号本身的权限**读取游戏信息、详情与镜像数据。

**实测**：`dist/GH-GameSearch.apk`（890,470 B）可直接安装使用；改代码才需要 Android Studio + JDK 17 + SDK 35。

**重要**：这个 App 不绕过后台权限 —— 账号能看到什么，取决于后台账号权限。

**用法**：复制下面整段发给 AI。

---

### 可复制 prompt

```text
仓库：https://github.com/A13612812330/GH-GameSearch
这是一个内部 Android 游戏信息查询 App（Kotlin）。先读 README.md 和 SECURITY.md 再动手。

目标分两条，先回答我第一条，等我确认再进第二条。

第一条：先讲清楚（不要写代码）
1. 它是怎么认证的？账号密码存在哪里？会不会存到本地？
2. 它调用后台哪些接口？分别读写什么数据？
3. 权限边界在哪 —— 普通账号和管理员账号看到的东西差在哪？
4. dist/ 里的 APK 是什么版本、对应哪个 commit、README 里的哈希对不对得上

第二条：我要自己构建（只有我明确说"开始构建"才做）
5. 检查本机环境：java -version（要 JDK 17）、ANDROID_HOME、adb version
6. 缺什么列清单给我，不要自己下载安装 SDK
7. 构建命令用 gradlew 还是 Studio，给我准确命令
8. 构建产物路径 + 签名方式（debug 还是 release keystore），
   ⚠️ release keystore 我没有，如果必须签名就停下告诉我

红线（重要）：
- 严禁猜测、枚举、硬编码任何后台账号、密码、Token、Cookie 或接口密钥
- 严禁在代码里写死登录凭据；登录必须由使用者在 App 界面内完成
- 严禁尝试绕过后台权限校验、抓包重放越权请求
- 严禁把 .env / keystore / 账号信息提交进仓库
- 如果要改网络层，先告诉我为什么改，不要悄悄换接口域名

做完给我一句话结论：这个 App 我能直接用，还是必须自己编译？
```

---

## 07 · GH-GameNews —— 资讯采集与日报/周报

**能干什么**：7 个平台资讯采集 → 今日简讯 → 日报/周报海报 → 飞书投递，带定时调度。
对接平台：好游快爆、TapTap、九游、游民星空、机核、游侠网、Steam。

**实测**：9 个依赖；有 `.env.example`。**飞书密钥只影响推送**，不填也能采集和生成海报。

**注意**：仓库 177 MB（含历史归档大文件），clone 慢；公开版**已删掉人工编辑器**。

**用法**：复制下面整段发给 AI。

---

### 可复制 prompt

```text
仓库：https://github.com/A13612812330/GH-GameNews
目标：先在不配飞书的情况下把采集和海报跑通，推送最后再接。

环境：Windows，Node 22。注意仓库 177 MB，clone 慢，用 --depth 1 浅克隆。

步骤：
1. git clone --depth 1 到 D:\projects\GH-GameNews
2. 读 README.md，告诉我这个项目的完整链路：采集 → 存储 → 简讯 → 海报 → 推送，
   每一环对应哪个目录或脚本
3. 环境变量：cp .env.example .env.local
   - 飞书的 5 组 App ID/Secret/Chat ID 全部留空，先不配
   - 明确告诉我：留空的情况下哪些功能能用、哪些会报错、怎么优雅跳过
4. 装依赖 npm install，然后启动
   - 开发模式用 npm run dev（前后端一起）
   - 注意 package.json 的 start 是个 PowerShell 脚本，如果我在 Git Bash 里跑有问题，告诉我替代命令
5. 验收：
   - 前端页面能打开，报端口和 HTTP 状态码
   - 手动触发一次采集，报给我：7 个平台每个抓了多少条、耗时、有没有失败的
   - 生成一份简讯/海报，把产物路径告诉我
6. 逐个平台评估抓取质量：标题是否完整、时间是否正确、正文有没有截断、
   有没有抓到无关内容。做成表格，标出哪个平台最需要优化

红线：
- 不要为了"抓得更多"提高请求频率或并发数，会封 IP
- 不要写死任何平台的 Cookie / 账号 / 飞书密钥
- 不要修改 scheduled 定时任务的触发时间（早报 08:30 / 晚报 17:50 / 周报周一 08:35）
- 不要 git push

做完给我：不配飞书能跑到哪一步 + 接飞书需要我准备哪几个值（只列变量名，不要让我在聊天里发密钥）。
```

---

## 08 · GH-NewGameWIki —— 新游资讯 / 活动 / 排期管理

**能干什么**：8 个平台采集 → SQLite → 后台管理，重点管**排期**。带 `AI_AGENT_SETUP.md`，把提示词发给 Agent 就能自行复刻。

**实测**：`npm run dev` 同时起前后端，端口 64111；有 `.env.example`，**无必填密钥**（Firecrawl key 是可选兜底）。

**用法**：复制下面整段发给 AI。

---

### 可复制 prompt

```text
仓库：https://github.com/A13612812330/GH-NewGameWIki
目标：跑起来，并且让我理解它的数据模型和排期逻辑（这是我接手后最可能要改的部分）。

环境：Windows，Node 22。端口 64111。

步骤：
1. clone 到 D:\projects\GH-NewGameWIki
2. 先读两个文件：README.md 和 AI_AGENT_SETUP.md —— 后者是专门给 AI 看的复刻指南，
   读完用 5 行话总结它要求你怎么做
3. cp .env.example .env（先全部用默认值，Firecrawl 相关留空）
   ⚠️ 确认默认值里的 NEWWIKI_BROWSER_CACHE_DIR 指向项目目录而不是系统临时盘
4. npm install（前端 Vite + 后端 Express，依赖不多），然后 npm run dev
5. 验收：
   - 前端页面：HTTP 200，报端口
   - 后端接口：随便取一个列表接口，返回 200 且有数据
   - 报给我：SQLite 数据库文件在哪、有几张表、每张表多少行
6. 用一张表讲清数据模型：表名 / 存什么 / 和谁关联 / 排期字段叫什么
7. 告诉我 8 个平台的采集分别在哪配置、哪个可以关

红线：
- 不要改 NEWWIKI_MAX_BACKUP_PAIRS / NEWWIKI_PRUNE_BACKUPS 等保留策略，
  那些值是防止我丢历史快照的
- 不要清空 runtime-cache 或 SQLite 历史快照
- 不要猜测 Firecrawl 等可选服务的 Key
- 不要 git push

做完给我一份"改排期字段要动哪几个文件"的清单。
```

---

## 09 · GH-Game-Puton —— 游戏后台上架批量导入

**能干什么**：Windows 桌面工具（Electron），批量往 `and-admin.ghzs.com` 填游戏上架信息。含交接文档、操作手册、字段映射表、局域网启动脚本。

**⚠️ 这个仓库没有 Release 成品包**（API 实测 0 个，本地打包产物也是空的），README 已修正。要直接运行只能自己打包。

**用法**：复制下面整段发给 AI。

---

### 可复制 prompt

```text
仓库：https://github.com/A13612812330/GH-Game-Puton
这是一个 Windows 桌面工具（Electron），用来批量往公司游戏后台上架导入数据。
注意：这个仓库没有 Release 成品包，必须自己打包才能运行。

环境：Windows，Node 22。

步骤：
1. clone 到 D:\projects\GH-Game-Puton
2. 先读三个文档：README.md、交接文档.md、新增游戏字段映射表.md
   读完后用一张表讲给我：输入什么格式的数据 → 映射到后台哪些字段 → 输出什么
3. npm install
4. 先干跑，不要真的提交：npm run check
   ⚠️ 这是 --dry-run 模式，只校验不写入。把校验结果（通过几条、失败几条、失败原因）贴给我
5. 打包：npm run 打包exe（electron-builder --win portable）
   报给我：产物路径、大小、打包耗时；如果报错贴完整错误原文
6. 运行方式二选一，先告诉我区别再执行：
   - npm run app（直接跑 Electron）
   - npm run web（起 web-server.mjs，浏览器里用）
   注意有个 --manual-login 变体，说明它是给"手动登录后台"模式用的
7. 验收：程序能启动、能读到我的导入数据、能预览映射结果

红线（这条项目尤其重要）：
- 严禁在没有 dry-run 通过的情况下执行真实导入（npm run import / manual-import）
- 严禁猜测、硬编码公司后台账号密码；GHZS_ADMIN_USER / GHZS_ADMIN_PASS
  是真实后台凭据，仓库里刻意没有，必须由使用者手动登录
- 严禁把凭据写进 .env 后提交，或贴进聊天
- 涉及真实生产后台的写操作，执行前必须让我明确回复"确认导入"并说明影响多少条数据
- 不要改局域网启动脚本里的 IP 之外的东西

做完给我：从"有 Excel 数据"到"后台出现数据"的完整操作路径，标出哪一步不可逆。
```
