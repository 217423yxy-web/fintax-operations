# FinTax AI 工作记录

> 本文档记录 FinTax 团队使用 AI 工具（Claude）完成的各类工作，涵盖目的、流程、工具和产出，供团队成员参考复用。

---

## 工具体系

### 核心工具
| 工具 | 用途 |
|------|------|
| **Claude Code（CLI）** | 本地开发、脚本编写、文件处理、自动化任务 |
| **Claude Desktop（Cowork 模式）** | 复杂多步任务、跨工具协作、长时间运行的代理任务 |

### MCP 服务器（工具扩展）
| 服务 | 功能 |
|------|------|
| `chrome-mcp-server` | 控制本地 Chrome 浏览器，用于网页操作和内容发布 |
| `twitter-collector` | X（Twitter）数据采集，支持历史推文和私信 |
| `wechat-mp-collector` | 微信公众号数据采集 |
| `xactions` | 自定义操作工具链（本地 MCP 服务） |

### 发布 Skills（一键发布工作流）
| Skill | 支持平台 |
|-------|---------|
| `linkedin-article-publish` | LinkedIn 公司页（FinTax Technology Limited） |
| `x-article-publish` | X（Twitter）长文章，含封面图、内嵌图、引用推文 |
| `wechat-publish` | 微信公众号草稿箱（通过 wenyan-mcp） |
| `webflow-publish` | FinTax 官网 Blog（fintax.tech / Webflow） |
| `taxdao-publish` | TaxDAO 运营管理平台 |
| `panews-publish` | PANews 创作者中心 |

---

## 业务模块

### 一、社媒数据采集与分析

**目的：** 全面了解 FinTax 各平台的内容表现和受众互动情况，支撑运营决策。

**流程：**
1. 通过 MCP 工具（twitter-collector / wechat-mp-collector）自动采集各平台历史数据
2. Claude 对原始数据进行清洗、结构化，导出 Excel 数据表
3. 生成交互式 HTML 可视化看板，支持在浏览器中直接查看

**覆盖平台：** X（Twitter）官方号 / X 中文号 / 微信公众号 / LinkedIn / 小宇宙播客 / 私信管理

**产出文件：**
- `01-社媒数据/数据表/` — 各平台结构化数据（xlsx）
- `01-社媒数据/可视化看板/` — 14 个交互式数据看板（html）
- `01-社媒数据/私信管理/` — 推特及领英私信汇总（含翻译版本）

---

### 二、多平台内容发布

**目的：** 将同一篇文章一键发布到多个平台，减少重复操作，保持各平台内容同步。

**流程：**
1. 准备文章（Markdown 格式）
2. 根据目标平台调用对应 Skill
3. Claude 自动控制浏览器完成：登录验证 → 创建文章 → 填写内容 → 上传封面图和内嵌图 → 发布

**特殊处理：**
- LinkedIn：处理富文本格式、表格截图、图片说明
- X：处理 DraftJS 编辑器的特殊输入方式，用引用推文发布社媒简介
- 微信：通过 wenyan-mcp 接口推送至草稿箱

**产出文件：**
- `02-内容发布/发布记录/推特文章内容.txt` — 已发布的 X 文章正文
- `02-内容发布/发布记录/推特文章-复制粘贴用.html` — X 文章格式化版本
- `02-内容发布/发布记录/wx_image_uploader.html` — 微信图片批量上传工具

---

### 三、营销素材生成

**目的：** 快速产出品牌传播所需的文字素材，包括新闻稿、媒体投放计划和演讲稿。

**流程：**
1. 提供背景资料（SOC 报告、活动信息等）
2. Claude 分析资料，生成对应格式的营销文本
3. 人工审核调整后对外发布或内部使用

**产出文件：**

*SOC 认证（`03-营销素材/SOC认证/`）：*
- `FinTax-SOC认证新闻稿.md` — 对外发布的官方新闻稿
- `FinTax-SOC公告拆解与新闻稿.md` — SOC 报告内容拆解与传播策略
- `FinTax-SOC报告品牌营销素材包.md` — 多平台推广素材合集

*媒体投放（`03-营销素材/媒体投放/`）：*
- `B26_媒体名单分析.xlsx` — B26 活动媒体资源分析
- `FinTax_B26_社媒营销计划.xlsx` — 对应的社媒推广执行计划
- `Top20媒体五维分析.xlsx` — 目标媒体综合评估

*演讲稿（`03-营销素材/演讲稿/`）：*
- `260314 新火讲座《数字资产全球税务合规与筹划实践》演讲稿.md`
- `OSL演讲稿-修改意见.md`

---

### 四、官网内容与设计

**目的：** 持续优化 FinTax 官网的视觉设计和页面内容，支持产品迭代和品牌升级。

**流程：**
1. 描述设计需求或提供参考
2. Claude 生成 HTML 原型（直接可在浏览器预览）
3. 多轮迭代优化后，导出 Webflow 嵌入代码上线

**产出文件：**

*首页设计稿（`04-官网内容/首页设计稿/`）：*
- `fintax-v4.html` 至 `fintax-v15.html` — 首页设计迭代（12个版本）
- `fintax-homepage-v3.html` — 首页 v3 定稿

*功能页面（`04-官网内容/功能页面/`）：*
- `官网Tax-Tool页面替换初稿.md` — Tax Tool 页面文案初稿
- `ai_roi_calculator.html` — AI ROI 计算器
- `dashboard.html` — 数据仪表板
- `product-carousel-demo.html` — 产品轮播展示
- `fintax-dashboard-0320.html` / `fintax-dashboard-simple.html` — FinTax 数据看板

*Webflow 嵌入代码（`04-官网内容/Webflow代码/`）：*
- `wf_head_code.txt` — `<head>` 区域嵌入代码
- `wf_body_code.txt` — `<body>` 区域嵌入代码
- `wf_js_code.txt` — 自定义 JavaScript

---

### 五、工具脚本开发

**目的：** 开发可复用的数据采集、处理和自动化脚本，减少人工操作。

**数据采集（`05-工具脚本/数据采集/`）：**
| 文件 | 功能 |
|------|------|
| `公众号数据提取脚本.js` | 从微信公众号后台提取文章数据 |
| `scroll_x_messages.js` | 滚动加载 X 平台私信 |
| `scroll_x_playwright.js` | 使用 Playwright 控制 X 页面滚动 |

**数据处理（`05-工具脚本/数据处理/`）：**
| 文件 | 功能 |
|------|------|
| `analyze_tweets_with_kb.py` | 结合知识库分析推文内容 |
| `process_messages.js` | 私信数据清洗与结构化 |
| `translate_messages.js` | 私信内容批量翻译 |

**自动化（`05-工具脚本/自动化/`）：**
| 文件 | 功能 |
|------|------|
| `upload_taxdao_batch.py` | 批量上传文章至 TaxDAO 平台 |
| `upload_taxdao_to_dify.py` | 将 TaxDAO 文章同步至 Dify 知识库 |
| `setup_xactions.sh` | xactions 工具链安装脚本 |
| `start_computer_use.sh` | Computer Use 功能启动脚本 |

---

### 六、X 情报监控与互动

**目的：** 系统性发现加密税务赛道的高价值 X 帖子，以 FinTax 品牌身份进行专业互动，扩大品牌曝光。

**流程：**
1. **企业数据库建设**：整理 CARF 定义的 10 个加密赛道中 312 家头部企业的 X 账号
2. **推文采集**：用 twikit（免费）或 TwitterAPI.io（付费）抓取目标企业最新推文
3. **翻译 + 分析**：Bing 翻译推文 → Claude 评估 FinTax 互动价值 → 标注互动角度
4. **知识库匹配**：将高价值推文与 TaxDAO 文章库匹配，生成有据可查的专业回复
5. **发布互动**：通过 `xactions/quote_tweet.js` 发布引用转推，每条间隔 3-5 分钟

**工具：**
- `sector-radar/fetch_tweets_free.py` — twikit 免费抓取（需 X 账号 cookies）
- `sector-radar/translate_and_analyze.py` — 翻译 + 互动机会分析
- `xactions/quote_tweet.js` — Puppeteer 无头浏览器发布引用转推
- TwitterAPI.io — 付费精准搜索（Key: `new1_ad975caf0bde4ecb860267533dcfb662`，需充值）

**产出文件（`07-X情报与互动/`）：**
- `sector-radar/` — 完整工具源码（含 CLAUDE.md、PLAYBOOK.md 操作手册）
- `sector-radar/output/CARF_10赛道企业X账号_完整版.xlsx` — 312 家企业数据库
- `sector-radar/output/cex_tweets_cn_analyzed.xlsx` — CEX 推文翻译 + 互动分析
- `tweets_kb_replies.xlsx` — 结合 TaxDAO 知识库生成的专业回复建议
- `FinTax-X热点分析与自动互动方案.md` — 完整系统架构设计方案
- `topic-research-demo.html` — 选题调研模块演示页面

**注意事项：**
- twikit cookies 有效期约 1-2 周，过期需重新从浏览器导出 `~/twitter_cookies.json`
- `sectors.py` 中部分 handle 有 "abordc" 错误，详见 `sector-radar/CLAUDE.md` 第四节

---

### 七、知识库配置与使用

**目的：** 将 TaxDAO 文章库作为 FinTax 的专业知识库，支撑 AI 生成有据可查的高质量内容和回复。

**知识库来源：**
- **TaxDAO 文章库**：收录 TaxDAO 发布的加密税务合规专业文章，共约 566 篇（英文）/ 11,894 篇（含中文翻译版）
- 覆盖话题：CARF 合规、DeFi 税务、NFT 税务、各国监管政策、加密会计等

**两种使用方式：**

**方式 A：脚本本地检索（轻量）**
```bash
# 关键词匹配搜索文章库，生成 Claude 提示词
python analyze_tweets_with_kb.py
```
- 文章库文件：`08-知识库/taxdao_articles_cn.csv`
- 不需要部署额外服务，直接在脚本中做关键词匹配
- 适合批量处理推文回复场景

**方式 B：Dify RAG 平台（完整）**
- 本地部署 Dify（`~/dify/`），将 CSV 文章库导入为 Knowledge Base
- 通过 Dify API 做向量检索，召回最相关文章
- 上传脚本：`05-工具脚本/自动化/upload_taxdao_to_dify.py`
- 适合构建完整的 RAG 应用或 Agent

**产出文件（`08-知识库/`）：**
- `taxdao_articles.csv` — TaxDAO 文章库（566 篇英文，含标题/关键词/摘要）
- `taxdao_articles_cn.csv` — TaxDAO 文章库中文版（11,894 篇，含中文翻译）
- `搜索API配置指南.md` — 搜索 API 配置说明

---

### 八、工具配置与文档

**工具使用说明（`06-工具配置/使用说明/`）：**
- `Chrome_MCP_Server_使用示例.md` — Chrome MCP 控制浏览器的使用方式
- `微信公众号数据收集工具使用说明.md` — 公众号采集工具操作指南
- `X数据收集工具使用说明.md` — X 平台数据采集操作指南
- `apollo-api-config.md` — Apollo 线索开发 API 配置说明

**部署指南（`06-工具配置/部署指南/`）：**
- `AiToEarn-部署指南.md` — AiToEarn 项目完整部署流程
- `Kiro迁移完整指南.md` — 从 Cursor 迁移到 Kiro 的操作指南

**内部文档（`06-工具配置/内部文档/`）：**
- `双部门AI架构设计方案.md` — 运营 + 技术双部门 AI 协作架构设计
- `FinTax架构学习指南.md` — FinTax 系统架构学习资料
- `COMPLETE_SYSTEM_PLAN.md` — 整体系统规划方案

---

## 文件索引

```
fintax-operations/
├── README.md
├── 01-社媒数据/
│   ├── 可视化看板/      # 14个交互式HTML看板 + index
│   ├── 数据表/          # Twitter/LinkedIn/微信/小宇宙 xlsx (5个)
│   └── 私信管理/        # 推特领英私信数据，含翻译版本 (3个)
├── 02-内容发布/
│   ├── 发布记录/        # X文章内容、微信图片工具 (3个)
│   └── 发布工具说明/    # 各平台发布 Skill 说明
├── 03-营销素材/
│   ├── SOC认证/         # 新闻稿、素材包 (3个md)
│   ├── 媒体投放/        # 媒体分析、营销计划 (3个xlsx)
│   └── 演讲稿/          # 新火讲座、OSL演讲 (2个md)
├── 04-官网内容/
│   ├── 首页设计稿/      # fintax-v4~v15 + v3 (13个html)
│   ├── 功能页面/        # 计算器、看板、轮播等 (7个)
│   └── Webflow代码/     # head/body/js 嵌入代码 (3个txt)
├── 05-工具脚本/
│   ├── 数据采集/        # 公众号、X平台采集脚本 (3个)
│   ├── 数据处理/        # 分析、清洗、翻译脚本 (3个)
│   └── 自动化/          # 上传、部署、启动脚本 (4个)
├── 06-工具配置/
│   ├── 使用说明/        # Chrome/微信/X/Apollo工具说明 (4个md)
│   ├── 部署指南/        # AiToEarn、Kiro迁移 (2个md)
│   └── 内部文档/        # AI架构、系统规划 (3个md)
├── 07-X情报与互动/
│   ├── sector-radar/    # 完整工具源码（含PLAYBOOK操作手册）
│   ├── tweets_kb_replies.xlsx       # 知识库匹配回复建议
│   ├── FinTax-X热点分析与自动互动方案.md
│   └── topic-research-demo.html
└── 08-知识库/
    ├── taxdao_articles.csv          # 566篇英文文章
    ├── taxdao_articles_cn.csv       # 11,894篇含中文翻译
    └── 搜索API配置指南.md
```
