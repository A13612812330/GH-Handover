# 02 · GH-WeeklyReport —— Excel 周报分析工具

**能干什么**：把周报 Excel 变成当周汇总、跨周对比、收益汇总和趋势图，浏览器里看。**零依赖**，`node` 直接跑。

**实测**：`PORT=18787 node server/server.mjs` → HTTP 200，页面标题「周报分析」。

**用法**：复制下面整段发给 AI。

---

## 可复制 prompt

```text
仓库：https://github.com/GHZS-Project/GH-WeeklyReport
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
