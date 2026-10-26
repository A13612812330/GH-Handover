# 08 · GH-NewGameWIki —— 新游资讯 / 活动 / 排期管理

**能干什么**：8 个平台采集 → SQLite → 后台管理，重点管**排期**。带 `AI_AGENT_SETUP.md`，把提示词发给 Agent 就能自行复刻。

**实测**：`npm run dev` 同时起前后端，端口 64111；有 `.env.example`，**无必填密钥**（Firecrawl key 是可选兜底）。

**用法**：复制下面整段发给 AI。

---

## 可复制 prompt

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
