# 05 · GH-GameGather —— 桌面 App + 配套数据服务

**这是两个仓库，必须一起理解**：

| 仓库 | 角色 |
|---|---|
| [`GH-GameGather-APP`](https://github.com/A13612812330/GH-GameGather-APP) | 前端**桌面成品**（Electron）。Release `v28` 262 MB，解压双击 `GameIntel.exe` 就能用 |
| [`GH-GameGather-UPSTREAM`](https://github.com/A13612812330/GH-GameGather-UPSTREAM) | 后端**数据服务**：Express + 15 个抓取器 + 93.6 MB JSON 索引快照 |

**关键认知**：只 clone APP 仓库是跑不起来的（那是外壳源码）。要完整体验，装 Release 包；要改数据逻辑，起 UPSTREAM。

**用法**：复制下面整段发给 AI。

---

## 可复制 prompt

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
