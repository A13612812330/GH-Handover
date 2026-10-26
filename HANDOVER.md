# 交接说明与实测记录

> 核对时间：2026-10-26 15:05（北京时间）　·　组织：`GHZS-Project`
> 适用对象：接手这 10 个 `GH-` 仓库的人，以及协助他的 AI Agent

---

## 〇、仓库归属（2026-10-26 迁移）

11 个仓库已从个人账号 `A13612812330` 转移到组织 **`GHZS-Project`**，交接入口变为：

**https://github.com/GHZS-Project/GH-Handover**

| 项 | 迁移前 | 迁移后 |
|---|---|---|
| 归属 | 个人账号 `A13612812330` | 组织 `GHZS-Project` |
| 仓库数 | 10 个散在个人名下 | 11 个（10 业务 + 1 入口）集中在组织下 |
| 交接方式 | 逐个加 collaborator | 把对方加入组织 **Owner**，一次覆盖全部 |
| 旧链接 | — | **301 自动重定向**到新地址，已发出的链接不会断 |

迁移验证方式（不是看页面 200，而是比内容）：迁移前后逐个核对 `commit sha`，**10 个业务仓库 sha 完全不变**；
`GH-Handover` 因迁移前又推了一次脚本而不同（`8f43c80 → e469100`），属预期。
文档内 56 处链接 + 10 个仓库 README 回链已全部改成新归属，`A13612812330/GH` 残留 **0** 处。

---

## 一、安全审计结论（2026-10-26 全量重扫）

**10 个仓库中未发现任何真实密钥。** 扫描范围：全部文本文件，覆盖以下模式：

| 检查项 | 结果 |
|---|---|
| 飞书 App Secret / Webhook / Verification Token | 0 命中 |
| GitHub Token（`ghp_` / `gho_` / `github_pat_`） | 0 命中 |
| OpenAI `sk-` / AWS `AKIA` / Google `AIza` / Slack `xox` | 0 命中 |
| Bearer / 硬编码 `password=` / `api_key=` | 0 命中（仅字段名与空占位符） |
| `.env` / `*.key` / `*.pem` / `*.jks` / `*.db` / 日志文件 | 仓库内均不存在 |
| 历史提交（`GH-CloudGame` 全部 5 个提交的文件清单） | 无 `config.json`、无密钥、无个人路径 |

### 保留的敏感项（功能必需，不是密钥）

| 项 | 位置 | 为什么保留 |
|---|---|---|
| 公司后台域名 `and-admin.ghzs.com` | `GH-Game-Puton` 脚本、`GH-GameSearch` Kotlin 源码 | 删掉工具就不能用；它只是地址，没有账号仍进不去 |
| 内网 IP `192.168.8.162` | `GH-Game-Puton` 的 `局域网启动服务.cmd` | 局域网使用说明需要，可自行改 |
| 默认管理员用户名 | `GH-Gamehub` / `GH-GameGather-UPSTREAM` 的 `data/admin-account.js` 中 `DEFAULT_USER` | 仅是默认用户名常量；密码走 `scrypt(pass, salt)` 哈希，凭据文件在 `.gitignore` 里 |

### 凭据设计（刻意排除，不是遗漏）

- `GH-Gamehub` / `GH-GameGather-UPSTREAM` 的 `.gitignore` 明确排除 `data/admin-account.json`、`data/admin-token.json`、`data/magnet-config.json`
- `UPSTREAM` 的 `.gitignore` 原话：**「凭据：本仓库刻意不含，请用环境变量提供」**
- 所有仓库均不含 `.env` 实体，只提供 `.env.example`

---

## 二、可用性实测记录

实测方式：clone 到本地、按 README 步骤执行、观察真实退出码与产物。**不看文档判断，只看实际结果。**

| 项目 | 实测动作 | 结果 |
|---|---|---|
| **GH-CloudGame** | `pipeline/09_run_all.py` | 9 步 **104.2 秒**完成；`08` 门禁 `ERROR 0 · WARN 0 → PASS`；产出 HTML 看板 + 多 sheet Excel |
| **GH-WeeklyReport** | `PORT=18787 node server/server.mjs` | HTTP `200`，`<title>` 为「周报分析」；确认**零依赖** |
| **GH-KomoSkill** | `scripts/doctor.py` | 8 项全 `OK`；`install.py` 支持 claude / codex / workbuddy 三目标 |
| **GH-GameSearch** | 检查 `dist/GH-GameSearch.apk` | 890,470 B，可直接安装；README 中哈希 `D3C0BAD5…` 与该文件对应 |
| **GH-GameGather-APP** | 检查 Release 与 `demo/` | Release `v28` 262 MB 整包；`demo/index.html` 双击可看 |
| **GH-Gamehub** | 依赖与自检脚本 | 依赖仅 **3 个**；`npm run doctor` / `handover` 可用；线上版 200 |
| **GH-GameGather-UPSTREAM** | 依赖清单 | 依赖 **3 个**，`npm start` → `server.js` |
| **GH-NewGameWIki** | `.env.example` 检查 | 无必填密钥（Firecrawl 为可选兜底） |
| **GH-GameNews** | `.env.example` 检查 | 飞书 5 组密钥仅推送需要；采集与海报可离线跑 |
| **GH-Game-Puton** | Releases API | **0 个 Release**；本地 `github-release-build/` 为空 → 必须自己打包 |

**结论：5 个开箱即用，4 个装一次依赖，1 个需自行打包。没有任何项目需要申请 API 密钥才能跑。**

---

## 三、本次交接做的文档修订

| 仓库 | 改了什么 | 提交 |
|---|---|---|
| `GH-GameSearch` | 补「接手须知 + 凭据说明」；个人路径 `E:\新建文件夹\...` → `D:\projects\...` | `dd7252d` |
| `GH-CloudGame` | 补「接手须知」：仓库无凭据可读，任务是读 `AGENT.md` 用 `samples/` 跑通并遵守 `08` 门禁 | `4bc38f5` |
| `GH-Game-Puton` | 修正错误指引：原文写「请下载 Releases」，实际 **0 个 Release**；改为「需 `npm run 打包exe`」 | `0b4fe74` |
| `GH-Gamehub` / `UPSTREAM` | `DEFAULT_USER` 由前任名字改为现任接手人账号名 | `694aa08` / `dd3db35` |

可见性变更：`GH-CloudGame`、`GH-GameSearch` 由私有 → 公开，匿名 API 访问均返回 `200`、`visibility=public`。

---

## 四、遗留待办（不影响接手）

| # | 事项 | 影响 | 建议 |
|---|---|---|---|
| 1 | `GH-CloudGame` README 写「jsdom 不装也行，09 会跳过」，**实测是直接报 `[环境自检未通过]` 中止** | 照文档走会卡住 | 已在 `prompts/01-CloudGame.md` 里写成必装；建议顺手改 README |
| 2 | `GH-GameNews` 仓库 177 MB（历史归档大文件） | 首次 clone 慢 | 用 `--depth 1` 浅克隆 |
| 3 | `GH-GameSearch` 的 `.github/workflows/android.yml` 未推送 | 仓库内无 CI | 需 `gh auth refresh -s workflow` 后才能推 |
| 4 | 6 个仓库无 LICENSE 文件 | 内部交接无碍 | 对外发布前补 |
| 5 | 10 个仓库均未启用 GitHub Pages | 想看网页版需本地起服务 | 需要时再开 |
| 6 | `GH-Game-Puton` 无成品包 | 接手人必须自己打包 | 建议补一个 Release |

---

## 五、接手人需要自备的东西

| 缺什么 | 影响项目 | 怎么办 |
|---|---|---|
| 后台账号 | GameSearch、Game-Puton | 在界面内手动登录，仓库内无凭据 |
| 管理员初始密码 | Gamehub | `npm run admin:init` 自行设定 |
| 飞书 App ID / Secret / Chat ID | GameNews | 只影响推送；不填仍可采集与生成海报 |
| 平台导出数据 | CloudGame、WeeklyReport | 仓库自带样例可先跑通；换成自己的数据再看 `AGENT.md` / `HANDOFF.md` |
| 打包环境 | Game-Puton | `npm i` + `npm run 打包exe` |
| Android 构建环境 | GameSearch（仅改代码时） | JDK 17 + SDK 35 + Android Studio；只使用不改代码则不需要 |
