# Apollo.io API 完整配置方案

## 1. API 认证配置

### 获取 API Key
1. 登录 Apollo.io 账户
2. 进入 Settings → API
3. 复制你的 API Key

### 认证方式
Apollo.io 使用 API Key 进行认证，有两种方式：

**方式一：Header 认证（推荐）**
```
X-Api-Key: YOUR_API_KEY
```

**方式二：Query 参数认证**
```
?api_key=YOUR_API_KEY
```

## 2. 核心 API 端点

### Base URL
```
https://api.apollo.io/v1/
```

### 主要端点

#### 2.1 人员搜索 (People Search)
- **端点**: `POST /mixed_people/search`
- **用途**: 搜索符合条件的领英用户
- **限制**: 根据套餐不同，有不同的配额限制

#### 2.2 获取人员详情
- **端点**: `GET /people/match`
- **用途**: 根据邮箱或领英 URL 获取详细信息

#### 2.3 组织搜索
- **端点**: `POST /mixed_companies/search`
- **用途**: 搜索公司信息

## 3. 人员搜索 API 详细配置

### 请求示例

```bash
curl -X POST https://api.apollo.io/v1/mixed_people/search \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: YOUR_API_KEY" \
  -d '{
    "page": 1,
    "per_page": 25,
    "person_titles": ["CEO", "CTO", "Founder"],
    "person_locations": ["United States"],
    "organization_num_employees_ranges": ["1,10", "11,50"],
    "q_keywords": "software engineer"
  }'
```

### 主要搜索参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `page` | integer | 页码（从1开始） | 1 |
| `per_page` | integer | 每页结果数（最大100） | 25 |
| `person_titles` | array | 职位标题 | ["CEO", "VP Sales"] |
| `person_locations` | array | 地理位置 | ["San Francisco", "New York"] |
| `person_seniorities` | array | 职级 | ["senior", "manager", "director"] |
| `organization_ids` | array | 公司 ID | ["5f5e2b..."] |
| `organization_num_employees_ranges` | array | 公司规模 | ["1,10", "11,50", "51,200"] |
| `q_keywords` | string | 关键词搜索 | "machine learning" |
| `person_not_titles` | array | 排除的职位 | ["Intern"] |
| `contact_email_status` | array | 邮箱状态 | ["verified", "guessed"] |
| `prospected_by_current_team` | array | 是否已联系 | ["yes", "no"] |

### 职级选项 (Seniorities)
- `senior` - 高级
- `entry` - 初级
- `manager` - 经理
- `director` - 总监
- `vp` - 副总裁
- `cxo` - C级高管
- `owner` - 所有者
- `partner` - 合伙人

### 公司规模范围
- `1,10` - 1-10人
- `11,50` - 11-50人
- `51,200` - 51-200人
- `201,500` - 201-500人
- `501,1000` - 501-1000人
- `1001,5000` - 1001-5000人
- `5001,10000` - 5001-10000人
- `10001+` - 10000人以上

## 4. 响应格式

### 成功响应示例

```json
{
  "breadcrumbs": [],
  "partial_results_only": false,
  "disable_eu_prospecting": false,
  "partial_results_limit": 10000,
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total_entries": 1234,
    "total_pages": 50
  },
  "people": [
    {
      "id": "5f5e2b...",
      "first_name": "John",
      "last_name": "Doe",
      "name": "John Doe",
      "linkedin_url": "https://www.linkedin.com/in/johndoe",
      "title": "CEO",
      "email": "john@example.com",
      "email_status": "verified",
      "photo_url": "https://...",
      "twitter_url": null,
      "github_url": null,
      "facebook_url": null,
      "organization": {
        "id": "5f5e2b...",
        "name": "Example Corp",
        "website_url": "https://example.com",
        "linkedin_url": "https://www.linkedin.com/company/example",
        "primary_domain": "example.com",
        "industry": "Computer Software",
        "num_employees": 150
      },
      "phone_numbers": [
        {
          "raw_number": "+1234567890",
          "sanitized_number": "+1234567890",
          "type": "mobile"
        }
      ],
      "city": "San Francisco",
      "state": "California",
      "country": "United States"
    }
  ],
  "num_fetch_result": 25
}
```

## 5. 错误处理

### 常见错误码

| 状态码 | 说明 | 解决方案 |
|--------|------|----------|
| 401 | 未授权 | 检查 API Key 是否正确 |
| 403 | 禁止访问 | 检查账户权限和配额 |
| 422 | 参数错误 | 检查请求参数格式 |
| 429 | 请求过多 | 降低请求频率，等待后重试 |
| 500 | 服务器错误 | 稍后重试 |

### 错误响应示例

```json
{
  "error": "Invalid API key",
  "message": "The API key provided is invalid"
}
```

## 6. 速率限制

- **免费版**: 每月有限的 API 调用次数
- **付费版**: 根据套餐不同，有不同的配额
- **建议**: 实现指数退避重试机制

## 7. 最佳实践

1. **使用环境变量存储 API Key**
   ```bash
   export APOLLO_API_KEY="your_api_key_here"
   ```

2. **实现重试机制**
   - 遇到 429 错误时等待后重试
   - 使用指数退避算法

3. **批量处理**
   - 使用分页获取大量数据
   - 合理设置 `per_page` 参数

4. **缓存结果**
   - 避免重复查询相同数据
   - 节省 API 配额

5. **错误日志**
   - 记录所有 API 调用和错误
   - 便于调试和监控

## 8. 注意事项

⚠️ **重要提示**:
- Apollo.io API 需要付费订阅才能使用
- 遵守数据使用政策和隐私法规（GDPR、CCPA等）
- 不要滥用 API 或进行垃圾邮件活动
- 定期检查 API 配额使用情况
- LinkedIn 数据的使用需遵守 LinkedIn 的服务条款
