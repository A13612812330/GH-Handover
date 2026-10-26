# 03 · GH-KomoSkill —— AI 协作工作法技能包

**能干什么**：不是业务工具，是一套**让 AI 按规矩干活**的技能包：六阶段门禁（需求→方案→执行→验收→归档）、证据纪律（不许凭记忆说"已完成"）、防失忆。支持 Codex / WorkBuddy / Claude。

**实测**：`doctor.py` 8 项检查全 `OK`；`install.py --target {claude,codex,workbuddy}` 可用。

**用法**：复制下面整段发给 AI。

---

## 可复制 prompt

```text
仓库：https://github.com/GHZS-Project/GH-KomoSkill
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
