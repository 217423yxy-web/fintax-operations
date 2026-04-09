# X (Twitter) 数据收集工具使用说明

## 🎉 安装完成！

你的 X 数据收集 MCP 服务器已经成功安装并配置。

## 📋 可用功能

现在我拥有以下 5 个新工具来帮你收集 X 账号数据：

### 1. **x_login** - 登录 X 账号
- 启动浏览器并自动登录你的 X 账号
- 使用方法：直接告诉我"登录 X"或"login to X"

### 2. **x_get_account_stats** - 获取账号统计
- 获取指定用户的关注数、粉丝数等统计数据
- 使用方法：告诉我"获取 @FinTax_Official 的账号统计"

### 3. **x_get_recent_tweets** - 获取最近推文
- 获取指定用户最近的推文及其数据（浏览量、点赞、转发、评论）
- 可以指定获取的推文数量（默认 10 条）
- 使用方法：告诉我"获取 @FinTax_Official 最近 10 条推文的数据"

### 4. **x_get_notifications** - 获取通知
- 获取你的通知和私信数量
- 使用方法：告诉我"查看我的 X 通知"

### 5. **x_close** - 关闭浏览器
- 关闭浏览器并清理资源
- 使用方法：告诉我"关闭 X 浏览器"

## 🚀 快速开始

### 步骤 1：重启 VS Code
**重要**：你需要重启 VS Code 才能加载新的 MCP 服务器。

1. 关闭 VS Code
2. 重新打开 VS Code
3. 打开 Cline 扩展

### 步骤 2：验证安装
重启后，你应该能在 Cline 的系统提示中看到新的工具。

### 步骤 3：开始使用
尝试以下命令：

```
请帮我登录 X 账号
```

```
获取 @FinTax_Official 的账号统计数据
```

```
获取 @FinTax_Official 最近 5 条推文的数据
```

```
查看我的 X 通知
```

## 📝 使用示例

### 示例 1：收集自己账号的完整数据
```
1. 先登录 X
2. 获取 @FinTax_Official 的账号统计
3. 获取 @FinTax_Official 最近 20 条推文的数据
4. 查看我的通知
5. 完成后关闭浏览器
```

### 示例 2：监控推文表现
```
每天帮我获取 @FinTax_Official 最近 10 条推文的数据，
并告诉我哪条推文表现最好（浏览量、点赞数最高）
```

## ⚙️ 配置信息

### 账号信息
- **用户名**: contact@fintax.tech
- **密码**: 已安全存储在本地配置文件中

### 配置文件位置
```
/Users/nightyoung/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```

### 项目位置
```
/Users/nightyoung/Documents/Cline/MCP/twitter-collector/
```

## 🔧 修改配置

如果需要更改账号信息：

1. 打开配置文件：
```bash
code "/Users/nightyoung/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
```

2. 修改 `X_USERNAME` 和 `X_PASSWORD`

3. 重启 VS Code

## ⚠️ 注意事项

### 安全性
- 你的账号凭证仅存储在本地电脑上
- 不会被发送到任何外部服务器
- 建议定期更改密码

### 使用限制
- 浏览器自动化可能会被 X 检测为异常行为
- 建议不要频繁使用，避免账号被限制
- 如果遇到验证码或额外验证，需要手动完成

### 浏览器行为
- 浏览器会以非无头模式运行（可以看到浏览器窗口）
- 这样可以方便你观察登录过程和数据收集过程
- 如果需要无头模式，可以修改源代码中的 `headless: false` 为 `headless: true`

## 🐛 故障排除

### 问题 1：工具不可用
**解决方案**：确保已重启 VS Code

### 问题 2：登录失败
**解决方案**：
- 检查用户名和密码是否正确
- 如果遇到额外验证，手动完成后重试
- 检查网络连接

### 问题 3：无法获取数据
**解决方案**：
- 确保已先登录（使用 x_login）
- 检查用户名是否正确（不含 @ 符号）
- 等待页面加载完成

### 问题 4：浏览器无法启动
**解决方案**：
- 确保已安装 Puppeteer 的依赖
- 运行：`cd /Users/nightyoung/Documents/Cline/MCP/twitter-collector && npm install`

## 📊 数据格式

### 账号统计数据
```json
{
  "success": true,
  "data": {
    "following": "123",
    "followers": "456",
    "profileUrl": "https://twitter.com/FinTax_Official"
  }
}
```

### 推文数据
```json
{
  "success": true,
  "data": [
    {
      "text": "推文内容...",
      "replies": "5",
      "retweets": "10",
      "likes": "20",
      "views": "1000"
    }
  ],
  "count": 10
}
```

## 🔄 更新工具

如果需要修改功能：

1. 编辑源代码：
```bash
code /Users/nightyoung/Documents/Cline/MCP/twitter-collector/src/index.ts
```

2. 重新编译：
```bash
cd /Users/nightyoung/Documents/Cline/MCP/twitter-collector
npm run build
```

3. 重启 VS Code

## 💡 使用技巧

1. **批量收集数据**：可以让我一次性执行多个命令
2. **定期监控**：可以让我定期收集数据并生成报告
3. **数据分析**：收集数据后，可以让我分析推文表现趋势
4. **导出数据**：可以让我将收集的数据保存为 CSV 或 JSON 文件

## 📞 需要帮助？

如果遇到任何问题，直接告诉我：
- "X 数据收集工具出问题了"
- "如何使用 X 数据收集功能"
- "帮我调试 X 登录问题"

---

**祝使用愉快！** 🎊
