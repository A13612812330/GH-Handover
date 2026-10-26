# 01 · GH-CloudGame —— 端游云游戏三源周报

**能干什么**：用神策搜索、鲸云下载、SteamDB 销量三份导出数据，跑出一份 Excel 五表 + HTML 看板周报。仓库自带两期真实样例，**不需要任何密钥就能完整跑通**。

**实测**：`09_run_all.py` 9 步 104.2 秒跑完，`08` 门禁 `ERROR 0 · WARN 0 → PASS`。

**用法**：复制下面整段发给 AI。

---

## 可复制 prompt

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
