# 网络搜索 API 配置指南

## 方案一：Google Custom Search API（推荐）

### 步骤 1：创建 Google Cloud 项目
1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 登录你的 Google 账号
3. 点击"创建项目"或选择现有项目
4. 记下你的项目 ID

### 步骤 2：启用 Custom Search API
1. 在 Google Cloud Console 中，进入"API 和服务" > "库"
2. 搜索"Custom Search API"
3. 点击"启用"

### 步骤 3：创建 API 密钥
1. 进入"API 和服务" > "凭据"
2. 点击"创建凭据" > "API 密钥"
3. 复制生成的 API 密钥（格式类似：`AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`）
4. （可选）点击"限制密钥"来设置使用限制

### 步骤 4：创建自定义搜索引擎
1. 访问 [Google Programmable Search Engine](https://programmablesearchengine.google.com/)
2. 点击"添加"创建新的搜索引擎
3. 在"要搜索的网站"中输入 `*`（搜索整个网络）
4. 创建后，记下你的"搜索引擎 ID"（格式类似：`a1b2c3d4e5f6g7h8i`）

### 步骤 5：配置环境变量
创建一个 `.env` 文件（或配置到系统环境变量）：

```bash
GOOGLE_API_KEY=你的API密钥
GOOGLE_CSE_ID=你的搜索引擎ID
```

### 费用说明
- **免费额度**：每天 100 次搜索请求
- **付费**：超过免费额度后，每 1000 次请求 $5

---

## 方案二：Bing Search API

### 步骤 1：创建 Azure 账号
1. 访问 [Azure Portal](https://portal.azure.com/)
2. 注册或登录 Azure 账号
3. 新用户可获得 $200 免费额度

### 步骤 2：创建 Bing Search 资源
1. 在 Azure Portal 中，点击"创建资源"
2. 搜索"Bing Search v7"
3. 点击"创建"
4. 选择定价层（F1 免费层或 S1 付费层）
5. 完成创建

### 步骤 3：获取 API 密钥
1. 进入创建的 Bing Search 资源
2. 在左侧菜单选择"密钥和终结点"
3. 复制"密钥 1"或"密钥 2"

### 步骤 4：配置环境变量
```bash
BING_API_KEY=你的Bing_API密钥
```

### 费用说明
- **免费层 (F1)**：每月 1000 次搜索请求
- **付费层 (S1)**：每 1000 次请求 $7

---

## 方案三：SerpAPI（最简单）

### 步骤 1：注册账号
1. 访问 [SerpAPI](https://serpapi.com/)
2. 注册账号

### 步骤 2：获取 API 密钥
1. 登录后，进入 Dashboard
2. 复制你的 API 密钥

### 步骤 3：配置环境变量
```bash
SERPAPI_KEY=你的SerpAPI密钥
```

### 费用说明
- **免费额度**：每月 100 次搜索
- **付费**：$50/月起（5000 次搜索）

---

## 推荐方案对比

| 方案 | 免费额度 | 配置难度 | 推荐度 |
|------|---------|---------|--------|
| Google Custom Search | 100次/天 | 中等 | ⭐⭐⭐⭐⭐ |
| Bing Search | 1000次/月 | 中等 | ⭐⭐⭐⭐ |
| SerpAPI | 100次/月 | 简单 | ⭐⭐⭐ |

**我的建议**：使用 Google Custom Search API，因为：
- 免费额度充足（100次/天 = 3000次/月）
- 搜索质量高
- 文档完善

---

## 配置完成后

配置好 API 密钥后，你需要告诉我：
1. 你选择的是哪个方案
2. 你的 API 密钥和相��配置信息
3. 我会帮你配置到系统中

或者，如果你想先跳过搜索功能的配置，我们可以直接开始你的原始任务：**创建 X 账号数据收集工具**。
