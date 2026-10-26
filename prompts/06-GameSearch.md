# 06 · GH-GameSearch —— Android 游戏信息查询 App

**能干什么**：内部 Android App（Kotlin）。通过 WebView 登录公司后台，按**账号本身的权限**读取游戏信息、详情与镜像数据。

**实测**：`dist/GH-GameSearch.apk`（890,470 B）可直接安装使用；改代码才需要 Android Studio + JDK 17 + SDK 35。

**重要**：这个 App 不绕过后台权限 —— 账号能看到什么，取决于后台账号权限。

**用法**：复制下面整段发给 AI。

---

## 可复制 prompt

```text
仓库：https://github.com/GHZS-Project/GH-GameSearch
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
