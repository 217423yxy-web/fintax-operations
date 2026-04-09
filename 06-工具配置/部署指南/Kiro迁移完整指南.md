# Kiro/Cline 完整迁移指南

## 📋 迁移概览

本指南将帮助你将当前电脑上的 Kiro/Cline、对话历史、项目文件和环境配置完整迁移到新电脑。

---

## 🎯 第一步：备份对话历史

### Cline 对话历史位置

Cline 的对话历史存储在以下位置：

**macOS:**
```
~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/
```

**Windows:**
```
%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\
```

**Linux:**
```
~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/
```

### 备份步骤

1. **打开终端，执行以下命令备份对话历史：**

```bash
# 创建备份目录
mkdir -p ~/Desktop/Kiro迁移备份

# 备份 Cline 对话历史
cp -r ~/Library/Application\ Support/Code/User/globalStorage/saoudrizwan.claude-dev ~/Desktop/Kiro迁移备份/cline-history

# 查看备份内容
ls -la ~/Desktop/Kiro迁移备份/cline-history
```

2. **备份 VS Code 设置（可选但推荐）：**

```bash
# 备份 VS Code 用户设置
cp -r ~/Library/Application\ Support/Code/User/settings.json ~/Desktop/Kiro迁移备份/

# 备份已安装的扩展列表
code --list-extensions > ~/Desktop/Kiro迁移备份/vscode-extensions.txt
```

---

## 📦 第二步：备份项目文件

### 你的主要项目列表

根据当前桌面扫描，以下是需要迁移的主要项目：

**AI 相关项目：**
- `ai-team-auto/` - AI团队自动化系统
- `ai-team-project/` - AI团队项目
- `claude-to-im/` - Claude到IM的桥接
- `cline-bridge/` - Cline桥��服务
- `remote-control-bot/` - 远程控制机器人

**前端项目：**
- `operations-platform-frontend/` - 运营平台前端

**文档：**
- `FinTax架构学习指南.md`
- `双部门AI架构设计方案.md`
- `COMPLETE_SYSTEM_PLAN.md`
- `claude-to-im-安装指南.md`
- `claude-to-im-下一步操作.md`
- 以及其他 .md 和 .html 文件

### 备份命令

```bash
# 方案1���打包所有项目到一个压缩文件（推荐）
cd ~/Desktop
tar -czf ~/Desktop/Kiro迁移备份/desktop-projects.tar.gz \
  ai-team-auto \
  ai-team-project \
  claude-to-im \
  cline-bridge \
  remote-control-bot \
  operations-platform-frontend \
  *.md \
  *.html

# 方案2：直接复制整个桌面（如果空间足够）
# cp -r ~/Desktop ~/Desktop/Kiro迁移备份/Desktop-backup
```

---

## 🔐 第三步：备份敏感配置

### 环境变量和密钥文件

```bash
# 备份所有 .env 文件
find ~/Desktop -name ".env" -type f -exec cp --parents {} ~/Desktop/Kiro迁移备份/ \;

# 或者手动备份关键项目的 .env
cp ~/Desktop/ai-team-auto/config/.env ~/Desktop/Kiro迁移备份/ai-team-auto.env
cp ~/Desktop/claude-to-im/.env ~/Desktop/Kiro迁移备份/claude-to-im.env
cp ~/Desktop/remote-control-bot/.env ~/Desktop/Kiro迁移备份/remote-control-bot.env
```

### 重要提示
⚠️ `.env` 文件包含敏感信息（API密钥等），请确保：
- 使用加密的U盘或云存储传输
- 传输后立即删除临时备份
- 不要上传到公共Git仓库

---

## 💾 第四步：选择传输方式

### 方式1：外部存储设备（推荐）

```bash
# 假设U盘挂载在 /Volumes/USB
cp -r ~/Desktop/Kiro迁移备份 /Volumes/USB/
```

### 方式2：云存储

```bash
# 使用 iCloud
cp -r ~/Desktop/Kiro迁移备份 ~/Library/Mobile\ Documents/com~apple~CloudDocs/

# 或使用其他云盘（百度网盘、阿里云盘等）
# 手动上传 ~/Desktop/Kiro迁移备份 文件夹
```

### 方式3：网络传输

```bash
# 使用 rsync 通过局域网传输到新电脑
# 在新电脑上运行 SSH 服务，然后：
rsync -avz ~/Desktop/Kiro迁移备份 username@new-computer-ip:~/Desktop/
```

---

## 🖥️ 第五步：在新电脑上恢复

### 1. 安装基础软件

```bash
# 安装 Homebrew (macOS)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Node.js
brew install node

# 安装 Python
brew install python@3.11

# 安装 Git
brew install git
```

### 2. 安装 VS Code 和 Cline

1. 下载并安装 [Visual Studio Code](https://code.visualstudio.com/)
2. 打开 VS Code
3. 进入扩展市场（Cmd+Shift+X）
4. 搜索 "Cline" 并安装
5. 配置 API 密钥（在 Cline 设置中）

### 3. 恢复对话历史

```bash
# 将备份的对话历史复制到新电脑的正确位置
cp -r ~/Desktop/Kiro迁移备份/cline-history/* ~/Library/Application\ Support/Code/User/globalStorage/saoudrizwan.claude-dev/

# 重启 VS Code 以加载历史记录
```

### 4. 恢复项目文件

```bash
# 解压项目文件
cd ~/Desktop
tar -xzf ~/Desktop/Kiro迁移备份/desktop-projects.tar.gz

# 或者直接复制文件夹
cp -r ~/Desktop/Kiro迁移备份/Desktop-backup/* ~/Desktop/
```

### 5. 恢复环境配置

```bash
# 恢复 .env 文件到对应项目
cp ~/Desktop/Kiro迁移备份/ai-team-auto.env ~/Desktop/ai-team-auto/config/.env
cp ~/Desktop/Kiro迁移备份/claude-to-im.env ~/Desktop/claude-to-im/.env
cp ~/Desktop/Kiro迁移备份/remote-control-bot.env ~/Desktop/remote-control-bot/.env
```

### 6. 重新安装项目依赖

```bash
# Python 项目
cd ~/Desktop/ai-team-auto
pip install -r requirements.txt

cd ~/Desktop/claude-to-im
pip install -r requirements.txt

cd ~/Desktop/remote-control-bot
pip install -r requirements.txt

# Node.js 项目
cd ~/Desktop/operations-platform-frontend
npm install
```

### 7. 恢复 VS Code 扩展（可选）

```bash
# 从备份的扩展列表批量安装
cat ~/Desktop/Kiro迁移备份/vscode-extensions.txt | xargs -L 1 code --install-extension
```

---

## ✅ 第六步：验证迁移

### 检查清单

- [ ] VS Code 和 Cline 已安装并配置
- [ ] 对话历史可以在 Cline 中查看
- [ ] 所有项目文件已复制到新电脑
- [ ] .env 文件已恢复且包含正确的密钥
- [ ] Python 和 Node.js 依赖已安装
- [ ] 项目可以正常运行

### 测试命令

```bash
# 测试 Python 项目
cd ~/Desktop/ai-team-auto
python test_system.py

# 测试 Node.js 项目
cd ~/Desktop/operations-platform-frontend
npm run dev

# 测试 Cline 对话历史
# 在 VS Code 中打开 Cline，查看历史对话是否存在
```

---

## 🔧 常见问题

### Q1: 对话历史没有显示？

**解决方案：**
1. 确认文件复制到了正确的位置
2. 检查文件权限：`chmod -R 755 ~/Library/Application\ Support/Code/User/globalStorage/saoudrizwan.claude-dev/`
3. 完全退出并重启 VS Code

### Q2: API 密钥失效？

**解决方案：**
1. 在 Cline 设置中重新输入 API 密钥
2. 检查 .env 文件中的密钥是否正确
3. 确认 API 密钥在新电脑的网络环境下可用

### Q3: Python/Node.js 依赖安装失败？

**解决方案：**
```bash
# Python: 使用虚拟环境
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Node.js: 清除缓存重试
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Q4: 项目路径不同导致的问题？

**解决方案：**
- 如果新电脑的用户名不同，需要更新配置文件中的绝对路径
- 使用相对路径或环境变量来避免硬编码路径

---

## 📝 迁移检查表

打印此清单，逐项完成：

**旧电脑上：**
- [ ] 备份 Cline 对话历史
- [ ] 备份所有项目文件
- [ ] 备份 .env 配置文件
- [ ] 备份 VS Code 设置和扩展列表
- [ ] 将备份传输到新电脑

**新电脑上：**
- [ ] 安装 Homebrew、Node.js、Python、Git
- [ ] 安装 VS Code 和 Cline 扩展
- [ ] 恢复对话历史
- [ ] 恢复项目文件
- [ ] 恢复 .env 配置
- [ ] 安装项目依赖
- [ ] 测试所有项目是否正常运行
- [ ] 验证 Cline 对话历史可访问

---

## 🎉 完成！

迁移完成后，你应该能够：
- 在新电脑上看到所有历史对话
- 继续之前的项目工作
- 使用相同的配置和环境
- 无缝继续与 Kiro 的协作

如有任何问题，可以随时在 Cline 中询问我！

---

**最后更新：** 2026年3月17日
**适用系统：** macOS (其他系统路径需相应调整)
