# Chrome MCP Server 使用示例

## 服务状态

✅ **Chrome MCP Server 运行正常**
- 版本：v1.0.31
- 端口：http://127.0.0.1:12306/mcp
- PID：37735
- Chrome 扩展 ID：hbdgbgagpkpjffpklnamcljpakneikee

## 可用工具（30+ 个）

### 1. 浏览器基础操作
```javascript
// 获取所有窗口和标签页
{
  "name": "get_windows_and_tabs",
  "arguments": {}
}

// 导航到 URL
{
  "name": "chrome_navigate",
  "arguments": {
    "url": "https://example.com",
    "newWindow": false
  }
}

// 截图
{
  "name": "chrome_screenshot",
  "arguments": {
    "storeBase64": true,
    "fullPage": true
  }
}

// 关闭标签页
{
  "name": "chrome_close_tabs",
  "arguments": {
    "tabIds": [123, 456]
  }
}
```

### 2. 页面交互
```javascript
// 读取页面元素（可访问性树）
{
  "name": "chrome_read_page",
  "arguments": {
    "filter": "interactive",  // 只返回可交互元素
    "depth": 5
  }
}

// 计算机控制（鼠标键盘）
{
  "name": "chrome_computer",
  "arguments": {
    "action": "left_click",
    "coordinates": { "x": 100, "y": 200 }
  }
}

// 点击元素
{
  "name": "chrome_click_element",
  "arguments": {
    "selector": "#login-button",
    "selectorType": "css"
  }
}

// 填充表单
{
  "name": "chrome_fill_or_select",
  "arguments": {
    "selector": "input[name='email']",
    "value": "test@example.com"
  }
}
```

### 3. 网络功能
```javascript
// 网络请求（带浏览器 cookies）
{
  "name": "chrome_network_request",
  "arguments": {
    "url": "https://api.example.com/data",
    "method": "POST",
    "headers": { "Content-Type": "application/json" },
    "body": "{\"key\":\"value\"}"
  }
}

// 网络捕获
{
  "name": "chrome_network_capture",
  "arguments": {
    "action": "start",
    "needResponseBody": true
  }
}

// 停止捕获
{
  "name": "chrome_network_capture",
  "arguments": {
    "action": "stop"
  }
}

// 获取网页内容
{
  "name": "chrome_get_web_content",
  "arguments": {
    "url": "https://example.com",
    "textContent": true
  }
}
```

### 4. JavaScript 执��
```javascript
// 执行 JavaScript
{
  "name": "chrome_javascript",
  "arguments": {
    "code": "return document.title;",
    "timeoutMs": 5000
  }
}

// 控制台日志
{
  "name": "chrome_console",
  "arguments": {
    "mode": "buffer",
    "includeExceptions": true
  }
}
```

### 5. 浏览器数据
```javascript
// 搜索历史记录
{
  "name": "chrome_history",
  "arguments": {
    "text": "github",
    "startTime": "1 week ago",
    "maxResults": 50
  }
}

// 搜索书签
{
  "name": "chrome_bookmark_search",
  "arguments": {
    "query": "documentation",
    "maxResults": 20
  }
}

// 添加书签
{
  "name": "chrome_bookmark_add",
  "arguments": {
    "url": "https://example.com",
    "title": "Example Site",
    "parentId": "1"
  }
}
```

### 6. 高级功能
```javascript
// 文件上传
{
  "name": "chrome_upload_file",
  "arguments": {
    "selector": "input[type='file']",
    "filePath": "/path/to/file.pdf"
  }
}

// 处理对话框
{
  "name": "chrome_handle_dialog",
  "arguments": {
    "action": "accept",
    "promptText": "确认"
  }
}

// 处理下载
{
  "name": "chrome_handle_download",
  "arguments": {
    "filenameContains": "report",
    "waitForComplete": true,
    "timeoutMs": 60000
  }
}

// GIF 录制
{
  "name": "chrome_gif_recorder",
  "arguments": {
    "action": "start",
    "fps": 5,
    "durationMs": 10000
  }
}
```

### 7. 性能分析
```javascript
// 开始性能追踪
{
  "name": "performance_start_trace",
  "arguments": {
    "reload": true,
    "autoStop": true,
    "durationMs": 5000
  }
}

// 停止追踪
{
  "name": "performance_stop_trace",
  "arguments": {
    "saveToDownloads": true,
    "filenamePrefix": "perf-trace"
  }
}

// 分析性能
{
  "name": "performance_analyze_insight",
  "arguments": {
    "insightName": "DocumentLatency"
  }
}
```

## 通过 MCP 协议调用

### 方式 1：通过 stdio（推荐用于 AI 助手集成）
```javascript
const { spawn } = require('child_process');

const mcpServer = spawn('node', [
  '/Users/nightyoung/.npm-global/lib/node_modules/mcp-chrome-bridge/dist/mcp/mcp-server-stdio.js'
]);

const request = {
  jsonrpc: '2.0',
  id: 1,
  method: 'tools/call',
  params: {
    name: 'get_windows_and_tabs',
    arguments: {}
  }
};

mcpServer.stdin.write(JSON.stringify(request) + '\n');

mcpServer.stdout.on('data', (data) => {
  console.log('Response:', JSON.parse(data.toString()));
});
```

### 方式 2：通过 HTTP（需要 session ID）
```bash
# 需要先建立 MCP session
curl -X POST http://127.0.0.1:12306/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_windows_and_tabs","arguments":{}}}'
```

## 配置文件位置

- **Native Messaging Host**: `/Users/nightyoung/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.chromemcp.nativehost.json`
- **MCP 配置**: `/Users/nightyoung/.npm-global/lib/node_modules/mcp-chrome-bridge/dist/mcp/stdio-config.json`
- **日志目录**: `/Users/nightyoung/Library/Logs/mcp-chrome-bridge/`

## 诊断命令

```bash
# 检查服务状态
mcp-chrome-bridge doctor

# 查看端口占用
lsof -i :12306

# 查看日志
ls -la /Users/nightyoung/Library/Logs/mcp-chrome-bridge/

# 测试连接
curl -s http://127.0.0.1:12306/ping
```

## 注意事项

1. **并发限制**：MCP Server 同时只能有一个活动的 stdio 连接
2. **Chrome 扩展**：必须安装并启用 Chrome 扩展才能使用工具
3. **权限**：某些操作需要用户授权（如文件上传、下载）
4. **超时**：长时间运行的操作建议设置合理的超时时间
5. **调试端口**：Chrome 需要启用远程调试端口（默认 9222）

## 实际应用场景

1. **自动化测试**：模拟用户操作，验证网页功能
2. **数据采集**：抓取网页内容，监控网络请求
3. **性能分析**：记录页面加载性能，生成报告
4. **浏览器控制**：通过 AI 助手控制浏览器操作
5. **录制演示**：生成操作步骤的 GIF 动画

---

**最后更新**: 2026-03-17
**版本**: mcp-chrome-bridge v1.0.31
