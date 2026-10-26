# 09 · GH-Game-Puton —— 游戏后台上架批量导入

**能干什么**：Windows 桌面工具（Electron），批量往 `and-admin.ghzs.com` 填游戏上架信息。含交接文档、操作手册、字段映射表、局域网启动脚本。

**⚠️ 这个仓库没有 Release 成品包**（API 实测 0 个，本地打包产物也是空的），README 已修正。要直接运行只能自己打包。

**用法**：复制下面整段发给 AI。

---

## 可复制 prompt

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
