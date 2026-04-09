# Playbook — 每轮成功操作方式

> 本文件只记录**已验证可行**的操作方式，供后续直接复用。

---

## 一、构建赛道企业数据库（312 家）

### 方式：种子库 + Web 搜索补充

**步骤**：
1. 人工整理每个赛道的头部企业作为种子（10 赛道各 10 家，共 105 家）
2. 通过 Google/Bing 搜索每个赛道的企业列表，逐条添加 X handle
3. 用 TwitterAPI.io `user/info` 端点抽样验证 handle 是否真实存在
4. 用 `src/excel_export.py` 导出为 Excel，按来源颜色标记

**产出**：`output/CARF_10赛道企业X账号_完整版.xlsx`（312 家企业）

**注意**：
- Path B（Bio 搜索）和 Path C（Following 网络）因 API 额度不足未充分跑通，但代码完整可用
- `sectors.py` 中部分 handle 有 "abordc" 错误，需修正后才能用于其他赛道

---

## 二、互动链深挖（从 312 家企业扩展账号）

### 目标
以 312 家企业账号为原点，通过三条互动链路发现更多行业相关账号（企业或从业者）。

### 三条路径权重

| 路径 | 权重 | 内容 |
|------|------|------|
| A. 转推/引用链 | 50% | 谁在转发或引用这 312 家企业的推文 |
| B. 关注网络 | 40% | 这 312 家企业互相关注的账号 |
| C. 评论挖掘 | 10% | 谁在这些企业推文下高质量评论 |

### 路径 A：转推/引用链（50%）

**方式**：twikit 抓取每家企业的最新推文 → 获取转推者/引用者账号

```python
# twikit 支持的方法
tweet.retweeters()    # 获取转推者列表
tweet.quote_tweets()  # 获取引用推文列表
```

**筛选逻辑**：
- 过滤掉粉丝数 < 100 的账号（噪音太多）
- 优先保留 Bio 中含行业关键词的账号（crypto / compliance / tax / exchange 等）
- 企业账号和个人从业者分开标记

**产出**：转推/引用者账号列表，含 handle、Bio、粉丝数

---

### 路径 B：关注网络（40%）

**方式**：TwitterAPI.io `user/followings` 端点，获取每家企业关注的账号列表，取交集

```bash
# 需充值 TwitterAPI.io，每次调用 $0.0015
export TWITTER_API_KEY=new1_ad975caf0bde4ecb860267533dcfb662
```

**筛选逻辑**：
- 被 3 家以上企业共同关注的账号优先级最高
- 过滤掉明显无关账号（新闻媒体、娱乐账号等）

**产出**：高交叉关注度账号列表，含共同关注数量排名

---

### 路径 C：评论挖掘（10%）

**方式**：twikit 抓取企业推文的回复

```python
# twikit 支持的方法
client.get_tweet_replies(tweet_id)
```

**筛选逻辑**：
- 只抓点赞数 >= 5 的评论（过滤低质量噪音）
- 优先保留评论内容含专业词汇的账号

**产出**：高质量评论者账号列表

---

### 汇总去重

三条路径结果合并后：
1. 去除已在 312 家企业名单中的账号
2. 按「被发现次数」排序（多路径交叉出现的优先级最高）
3. 导出为 Excel，标注发现来源（转推/关注/评论）

---

## 三、免费抓取推文（twikit）

### 方式：twikit 纯 HTTP 抓取

**前置条件**：
- 已登录的 X 账号 cookies，保存为 `~/twitter_cookies.json`
- 格式：`[{"name": "auth_token", "value": "..."}, {"name": "ct0", "value": "..."}, ...]`
- 获取方式：浏览器登录 x.com → 用 Cookie-Editor 扩展导出

**安装**：
```bash
pip install twikit
```

**运行**：
```bash
# 全部 48 个 CEX 账号，每个取 1 条最新推文
python fetch_tweets_free.py --count 1 --delay 2

# 指定账号
python fetch_tweets_free.py --handles binance coinbase okx --count 5

# 指定输出路径
python fetch_tweets_free.py --output output/my_tweets.json
```

**产出**：`output/cex_tweets_twikit_YYYYMMDD_HHMM.json`

**注意**：
- 脚本顶部有 monkey-patch 绕过 `ClientTransaction` 签名问题，不需要修改
- `--delay 2` 是推荐间隔，过快可能被限流
- cookies 有效期约 1-2 周，过期后需重新导出

---

## 三、推文翻译 + FinTax 互动分析

### 方式：Bing 翻译 + 关键词匹配 + 人工标注

**前置条件**：
- 已有推文 JSON 文件（由步骤二生成）
- 修改 `translate_and_analyze.py` 顶部的 `INPUT_FILE` 指向目标 JSON

**安装**：
```bash
pip install translators openpyxl
```

**运行**：
```bash
PYTHONUNBUFFERED=1 python translate_and_analyze.py
```

**产出**：`output/cex_tweets_cn_analyzed.xlsx`，包含两个 Sheet：
- **全部推文（含翻译）**：所有推文 + 中文翻译，可互动推文黄色高亮
- **⭐ 互动机会汇总**：筛选出的可互动推文，按点赞数排序，每条附互动角度建议

**互动判断逻辑**（修改 `translate_and_analyze.py` 来调整）：
- `ENGAGE_ANGLES` 字典：对特定推文（以 tweet ID 为 key）写入具体互动建议
- `ENGAGE_KEYWORDS` 列表：关键词匹配，命中则自动生成通用建议

**注意**：
- 必须用 `PYTHONUNBUFFERED=1` 或 `print(..., flush=True)`，否则后台运行时看不到进度
- Bing 翻译限速约 2 秒/条，563 条约需 25 分钟
- 非英文推文（韩语/泰语/西班牙语）会标注「非英文，保留原文」，不翻译

---

## 四、付费 API 补充发现（TwitterAPI.io）

> 当前余额 $0，需充值后使用。充 $5 足够覆盖完整的 Path B + Path C 运行。

**安装**：无需额外安装，`requests` 已包含在 `requirements.txt`

**配置**：
```bash
export TWITTER_API_KEY=new1_ad975caf0bde4ecb860267533dcfb662
```

**运行**：
```bash
# 跑单个赛道，目标 100 家企业
python run.py --sector cex --target 100

# 跑全部 10 个赛道
python run.py --all --target 100

# 只导出种子企业（不消耗 API 额度）
python run.py --sector cex --seeds-only
```

**成本参考**：
| 操作 | 端点 | 成本 |
|------|------|------|
| 搜索用户（Path B） | `user/search` | $0.0015/次 |
| 获取关注列表（Path C） | `user/followings` | $0.0015/次 |
| 验证 handle | `user/info` | $0.00015/次 |
| 抓取推文 | `user/last_tweets` | $0.00015/次 |

---

## 五、发布互动推文（引用转推）

### 来源
`/Users/nightyoung/xactions/quote_tweet.js` — 基于 Puppeteer 无头浏览器，无需 API 费用。

### 前置条件
- Node.js 已安装
- 已安装 puppeteer：`npm install puppeteer`
- X 账号的 `auth_token` cookie（从浏览器 DevTools 获取，或复用 `~/twitter_cookies.json` 里的值）

### 设置 auth_token
```bash
export XACTIONS_SESSION_COOKIE=你的auth_token值
```

或每次运行时作为第三个参数传入。

### 运行方式
```bash
# 单条引用转推
node /Users/nightyoung/xactions/quote_tweet.js <推文URL> "<评论内容>"

# 示例：对 coinbase 税务推文发布 FinTax 评论
node /Users/nightyoung/xactions/quote_tweet.js \
  https://x.com/coinbase/status/2036816814655828190 \
  "除了借贷方案，企业还可以用 FinTax 提前规划纳税时点——我们的 CARF/1099DA 申报平台帮交易所和机构提前识别应税事件，避免被动触发。"
```

### 与 Step 三的衔接

`cex_tweets_cn_analyzed.xlsx` 的「⭐ 互动机会汇总」Sheet 已包含：
- 推文链接（第 7 列）
- 互动角度建议（第 4 列，即评论内容）

按点赞数从高到低逐条处理，复制链接和建议内容，运行上述命令即可发布。

### 注意
- 每条引用转推之间建议间隔 **3-5 分钟**，避免被 X 判定为垃圾行为
- 互动角度建议是中文，发布前确认是否需要调整为英文（大多数 CEX 推文是英文）
- 优先处理 ⭐⭐⭐ 级别的高价值推文（Excel 第 4 列开头有标注）

---

## 快速参考

```bash
# 验证 cookies 是否有效
python fetch_tweets_free.py --handles binance --count 1

# 完整流程（免费版）
python fetch_tweets_free.py --count 1 --delay 2
PYTHONUNBUFFERED=1 python translate_and_analyze.py

# 完整流程（付费版，需充值）
export TWITTER_API_KEY=new1_ad975caf0bde4ecb860267533dcfb662
python run.py --all --target 100
```
