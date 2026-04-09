# Sector Radar — 社媒情报工具

> 本文件是写给 Claude Code 的项目上下文文档。阅读此文件后你就能理解整个项目的目标、架构、现状和待办事项。

## 项目归属

**FinTax** — 加密资产税务合规公司（support@fintax.tech）。该项目是 FinTax 的社媒运营工具之一。

---

## 一、项目目标

构建一个 **X/Twitter 社媒情报系统**，分为两步：

### Step 1：赛道企业雷达（已完成 ~80%）
发现 CARF（加密资产报告框架，OECD 制定）定义的 **10 个赛道** 中每个赛道 100 家企业的 X 账号。三条发现路径：
- **Path A**：内置种子企业（人工整理的头部企业）
- **Path B**：TwitterAPI.io `search_user` — Bio 关键词搜索
- **Path C**：种子企业的 following 网络扩展

**当前进度**：已通过种子 + Web 搜索补充，形成 **312 家企业数据库**（输出在 `output/CARF_10赛道企业X账号_完整版.xlsx`）。API 发现路径（Path B/C）因额度耗尽未充分跑通。

### Step 2：从业者线索扩展（未开始）
从 312 家企业扩展到 **3000 个个人从业者**线索，三条路径：
- 评论挖掘（60%）：抓取企业推文下的高质量评论者
- 粉丝交叉分析（15%）：关注多个同赛道企业的账号
- 互动链追踪（25%）：转推/引用推文的行业 KOL

---

## 二、10 个 CARF 赛道

| ID | 中文名 | 英文名 | 种子数 |
|---|---|---|---|
| cex | 中心化交易所 | Centralized Exchange | 15 |
| custody | 加密资产托管 | Digital Asset Custody | 10 |
| asset_mgmt | 加密资产管理 | Crypto Asset Management | 10 |
| rwa | RWA 代币化 | Real World Asset Tokenization | 10 |
| payment | 加密支付 | Crypto Payment | 10 |
| mining | 矿业 | Crypto Mining | 10 |
| defi_lending | DeFi 借贷 | DeFi Lending | 10 |
| staking | Staking 服务 | Staking Services | 10 |
| compliance | 合规与税务 | Crypto Compliance & Tax | 10 |
| otc | OTC 与经纪 | OTC & Brokerage | 10 |

---

## 三、项目文件结构

```
sector-radar/
├── CLAUDE.md              ← 你正在读的文件
├── config.yaml            ← 项目配置（API、速率、目标数）
├── requirements.txt       ← pip 依赖（requests, openpyxl）
├── run.py                 ← CLI 入口（--sector / --all / --seeds-only）
├── fetch_tweets.py        ← 付费版推文抓取（TwitterAPI.io，$0.00015/条）
├── fetch_tweets_free.py   ← 免费版推文抓取（twikit，纯 HTTP，需 cookies）
├── translate_and_analyze.py ← 推文翻译 + FinTax 互动机会分析
├── RUN_ME.sh              ← 一键安装+运行脚本
├── src/
│   ├── __init__.py
│   ├── sectors.py         ← 10 赛道定义 + 105 种子企业 ⚠️ 部分 handle 有误
│   ├── twitter_client.py  ← TwitterAPI.io REST 客户端
│   ├── pipeline.py        ← 三路径发现 Pipeline（A→B→C）
│   └── excel_export.py    ← Excel 导出（颜色标记来源）
└── output/
    ├── CARF_10赛道企业X账号_完整版.xlsx  ← 312 家企业总表
    ├── CEX_最新推文.xlsx                ← 早期 9 条推文（TwitterAPI.io 抓取）
    ├── cex_tweets_twikit_*.json         ← twikit 抓取的推文（最新 563 条）
    ├── cex_tweets_twikit_*.xlsx         ← 推文 Excel 版
    ├── cex_tweets_cn_analyzed.xlsx      ← 翻译+互动分析版
    └── cex_tweets_translated_analyzed.xlsx
```

---

## 四、关键文件说明

### 4.1 `fetch_tweets_free.py`（主力推文抓取脚本）

**技术方案**：twikit（Python 库，模拟 X 内部 API，纯 HTTP 无需浏览器）

**工作原理**：
1. 从 `~/twitter_cookies.json` 加载已登录的 X 账号 cookies
2. 用 twikit Client 设置 cookies 认证
3. 对每个账号：先 `get_user_by_screen_name()` 获取 user_id → 再 `get_user_tweets()` 获取推文
4. 自动跳过转推，提取原创推文的文本、日期、互动数据、浏览量
5. 输出 JSON 到 `output/` 目录

**已知问题**：
- twikit 的 `ClientTransaction` 签名机制可能会报错（`ondemand.s.a.js` 返回 404），脚本已内置 monkey-patch 绕过
- 需要有效的 X 账号 cookies，cookies 过期后需重新导出

**运行方式**：
```bash
pip install twikit
python fetch_tweets_free.py                           # 全部 48 个 CEX
python fetch_tweets_free.py --handles binance okx     # 指定账号
python fetch_tweets_free.py --count 5 --delay 3       # 每个账号 5 条，间隔 3 秒
```

**cookies 获取方法**：
用浏览器登录 x.com → 用 Cookie-Editor 等扩展导出所有 cookies → 保存为 `~/twitter_cookies.json`，格式为 `[{"name": "...", "value": "..."}, ...]`

### 4.2 `fetch_tweets.py`（付费版，TwitterAPI.io）

**成本**：$0.00015/条推文（`user/last_tweets` 端点，15 credits/call，$1 = 100,000 credits）

**运行**：
```bash
export TWITTER_API_KEY=new1_ad975caf0bde4ecb860267533dcfb662
python fetch_tweets.py
```

注意：当前 API 余额为 $0（已消耗 $0.29），需充值后才能使用。建议充值 $5 足够覆盖所有操作。

### 4.3 `translate_and_analyze.py`

读取 twikit 抓取的 JSON → 用 Bing 翻译到中文 → 分析每条推文是否有 FinTax 互动机会。

**互动机会判断逻辑**：
- 关键词匹配：tax, compliance, regulation, staking reward, tokenization, audit 等
- 预标注角度：针对特定高价值推文给出具体互动建议（如何以 FinTax 身份评论）
- 输出两个 Sheet：全部推文 + 互动机会汇总（按点赞数排序）

**依赖**：`pip install translators`

### 4.4 `src/sectors.py`

**⚠️ 重大问题：部分种子企业 handle 有误**

由于早期会话压缩导致数据损坏，以下 handle 包含 "abordc" 错误模式，需要修正：

| 错误 handle | 正确 handle | 企业名 |
|---|---|---|
| `kabordc` | `kraken` | Kraken |
| `okabordc` | `okx` | OKX |
| `bitabordc` | `bitget` | Bitget |
| `Coabordc` | `Cobo_Global` | Cobo |
| `21abordc` | `21Shares` | 21Shares |
| `polyabordc` | `polyabordc_cap` 或 `Polychain` | Polychain Capital |
| `multiabordc` | `multicoincap` | Multicoin Capital |
| `mabordc_xyz` | `maple_finance` | Maple Finance |
| `goldabordc_fi` | `goldabordc_fi` (待确认) | Goldfinch |
| `transabordc` | `transabordc` (待确认) | Transak |
| `aabordc` | `AaveAave` | Aave |
| `euabordc_xyz` | `eulerfinance` | Euler Finance |
| `stabordc_us` | `stabordc_us` (待确认) | Staked.us |
| `jabordc_sol` | `jabordc_sol` (待确认) | Jito |
| `ellabordc` | `elliptic` | Elliptic |
| `notabordc_io` | `notabordc_io` (待确认) | Notabene |
| `tokabordc` | `tokabordc` (待确认) | Tokeny |
| `Aabordc_Group` | `Aabordc_Group` (待确认) | Amber Group |

**注意**：`fetch_tweets.py` 和 `fetch_tweets_free.py` 中的 CEX handle 列表已经是修正后的正确版本，只有 `sectors.py` 中仍有错误。非 CEX 赛道的 handle 有些尚未确认正确值，需要逐个在 x.com 上验证。

### 4.5 `src/pipeline.py`

三路径发现 Pipeline 的核心逻辑。目前因 API 额度不足，Path B 和 Path C 未能充分运行。代码逻辑完整可用，充值 API 后即可直接运行。

### 4.6 `src/twitter_client.py`

TwitterAPI.io REST 客户端，封装了以下端点：
- `user/search`：搜索用户（150 credits/call）—— 最贵，谨慎使用
- `user/last_tweets`：获取用户最新推文（15 credits/call）—— 最常用
- `user/info`：获取用户详情（15 credits/call）
- `user/followings`：获取用户关注列表（150 credits/call）
- `user/followers`：获取用户粉丝列表（150 credits/call）
- `tweet/advanced_search`：高级推文搜索（150 credits/call）

Base URL: `https://api.twitterapi.io/twitter`
认证: `X-API-Key` header

---

## 五、已有产出

| 文件 | 内容 |
|---|---|
| `output/CARF_10赛道企业X账号_完整版.xlsx` | 312 家企业，10 赛道，每赛道 28-48 家 |
| `output/cex_tweets_twikit_20260326_1335.json` | 563 条推文（48 个 CEX 账号，twikit 抓取） |
| `output/cex_tweets_cn_analyzed.xlsx` | 推文翻译 + FinTax 互动机会分析 |

---

## 六、待办事项（优先级排序）

### P0 — 立即可做
1. **修复 `sectors.py` 中的错误 handle**：逐个在 x.com 上确认正确 handle，替换所有 "abordc" 错误
2. **验证 twikit cookies 是否过期**：如果过期，重新从浏览器导出 `~/twitter_cookies.json`

### P1 — 短期目标
3. **扩展其他 9 个赛道的推文抓取**：当前只抓了 CEX，需要对 custody/asset_mgmt/rwa 等也运行 `fetch_tweets_free.py`（需先修正 handle）
4. **充值 TwitterAPI.io**：充 $5 即可跑通 Path B/C 扩展，将 312 家企业推到接近 1000 家

### P2 — Step 2（从业者线索）
5. **设计 Step 2 的数据管道**：评论挖掘 + 粉丝交叉 + 互动链追踪
6. **实现评论抓取模块**：twikit 支持 `get_tweet_replies()`，可以获取推文评论
7. **构建从业者筛选模型**：区分企业账号 vs 个人从业者，筛选有价值的行业人士

---

## 七、API 信息

### TwitterAPI.io（付费）
- API Key: `new1_ad975caf0bde4ecb860267533dcfb662`
- 当前余额: $0.00（已消耗 $0.29）
- 计费: $1 = 100,000 credits
- 免费层限制: 1 req/5s

### twikit（免费）
- 无 API Key 需要
- 需要 X 账号 cookies 认证
- cookies 文件: `~/twitter_cookies.json`
- 格式: `[{"name": "auth_token", "value": "..."}, {"name": "ct0", "value": "..."}, ...]`
- 关键 cookies: `auth_token`, `ct0`（CSRF token）

---

## 八、技术注意事项

1. **twikit ClientTransaction patch**：`fetch_tweets_free.py` 顶部有一段 monkey-patch 代码，绕过 X 的 `ondemand.s.a.js` 签名机制。如果 twikit 升级后修复了这个问题，可以移除 patch。
2. **速率控制**：twikit 抓取建议 `--delay 2`（每个账号间隔 2 秒），过快可能被限流。
3. **非 CEX 赛道 handle 未全部验证**：custody/rwa/payment 等赛道的种子 handle 部分来自 AI 生成，可能不准确，需人工验证。
4. **Excel 导出依赖 openpyxl**：所有 Excel 文件通过 openpyxl 生成，颜色编码按来源区分（黄=种子，蓝=Bio搜索，紫=Following网络）。

---

## 九、快速开始命令

```bash
# 安装依赖
pip install twikit openpyxl requests translators

# 查看所有赛道
python run.py --list-sectors

# 仅导出种子企业（不需要 API）
python run.py --sector cex --seeds-only

# 用 twikit 免费抓取 CEX 推文
python fetch_tweets_free.py --handles binance coinbase --count 1

# 全量抓取 48 个 CEX 最新推文
python fetch_tweets_free.py --count 1 --delay 2

# 翻译 + 互动分析
python translate_and_analyze.py

# 用付费 API 跑 Pipeline（需充值）
export TWITTER_API_KEY=new1_ad975caf0bde4ecb860267533dcfb662
python run.py --sector cex --target 100
```
