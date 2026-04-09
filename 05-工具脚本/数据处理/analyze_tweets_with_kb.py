#!/usr/bin/env python3
"""
对 CEX 推文进行知识库匹配分析，生成 FinTax 专业回复建议。
使用 Claude relay API + TaxDAO 文章库。
"""

import csv
import json
import re
import time
import pandas as pd
import requests

RELAY_API_KEY = "sk-OIqndkQAn50fOPFTueWUhEzWvN3Bh1Pt8XxddS2cACrYhbNz"
RELAY_BASE_URL = "https://api.ikuncode.cc/v1"
MODEL = "claude-sonnet-4-6"

TWEETS_FILE = "/Users/nightyoung/社媒运营工具/sector-radar/output/cex_tweets_cn_analyzed.xlsx"
KB_FILE = "/Users/nightyoung/Desktop/taxdao_articles_cn.csv"
OUTPUT_FILE = "/Users/nightyoung/Desktop/tweets_kb_replies.xlsx"


def search_articles(query: str, articles: list[dict], top_k: int = 5) -> list[dict]:
    """Simple keyword-based search in article content."""
    # Extract keywords from query
    keywords = re.findall(r'[\u4e00-\u9fa5a-zA-Z]+', query)
    # Filter to meaningful keywords (>=2 chars)
    keywords = [k for k in keywords if len(k) >= 2][:10]

    scored = []
    for art in articles:
        text = f"{art.get('title','')} {art.get('keyword','')} {art.get('digest','')} {art.get('article','')[:500]}"
        score = sum(text.count(kw) for kw in keywords)
        if score > 0:
            scored.append((score, art))

    scored.sort(key=lambda x: -x[0])
    return [art for _, art in scored[:top_k]]


def call_claude(prompt: str) -> str:
    """Call Claude via relay API using streaming mode."""
    headers = {
        "Authorization": f"Bearer {RELAY_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "max_tokens": 1200,
        "stream": True,
        "messages": [{"role": "user", "content": prompt}],
    }
    resp = requests.post(
        f"{RELAY_BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        timeout=90,
        stream=True,
    )
    if resp.status_code != 200:
        return f"[API Error {resp.status_code}]: {resp.text[:100]}"

    full_text = ""
    for line in resp.iter_lines():
        if not line:
            continue
        if line == b"data: [DONE]":
            break
        if line.startswith(b"data: "):
            try:
                chunk = json.loads(line[6:])
                choices = chunk.get("choices", [])
                if choices:
                    delta = choices[0].get("delta", {}).get("content", "")
                    if delta:
                        full_text += delta
            except Exception:
                pass
    return full_text


def analyze_tweet(tweet_cn: str, angle: str, relevant_articles: list[dict]) -> dict:
    """Analyze a tweet and generate a reply using relevant articles."""
    # Prepare article excerpts
    article_excerpts = ""
    for i, art in enumerate(relevant_articles[:3]):
        article_excerpts += f"""
【文章{i+1}】标题：{art.get('title', '')}
关键词：{art.get('keyword', '')}
摘要：{art.get('digest', '')}
内容节选：{art.get('article', '')[:400]}
---"""

    prompt = f"""你是 FinTax（加密货币税务合规 SaaS 平台）的社媒运营专家。

【CEX 推文内容（中文）】
{tweet_cn}

【已有互动角度建议】
{angle}

【知识库中检索到的相关文章】
{article_excerpts if article_excerpts.strip() else "（未找到高度相关文章）"}

请完成以下两项任务：

1. **知识库可回答性判断**（一句话）：基于知识库中的文章，判断 FinTax 是否有足够的内容支撑来回复这条推文？回答格式：「✅ 可以回答」或「⚠️ 部分可回答」或「❌ 知识库内容不足」，并简述原因（30字以内）。

2. **专业回复建议**（如果可以回答）：
   - 用英文撰写一条 Twitter 回复（≤280字符）
   - 语气：专业、有洞察力，体现 FinTax 作为加密税务合规专家的权威性
   - 要自然地引用或呼应知识库中的具体内容（如具体法规名称、国家政策、数据等）
   - 结尾可加 #CryptoTax #Compliance 等标签
   - 不要过度推销，要像行业专家发表见解

请直接输出 JSON：
{{
  "can_answer": "✅ 可以回答 / ⚠️ 部分可回答 / ❌ 知识库内容不足",
  "reason": "原因说明",
  "reply_en": "英文回复内容（如可回答）",
  "key_article": "引用的主要文章标题（如有）"
}}"""

    result = call_claude(prompt)

    # Parse JSON from response (handle markdown code blocks)
    try:
        # Strip markdown code fences if present
        cleaned = re.sub(r'```(?:json)?\s*', '', result).strip()
        json_match = re.search(r'\{[\s\S]*\}', cleaned)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass

    return {
        "can_answer": "⚠️ 解析失败",
        "reason": result[:100],
        "reply_en": "",
        "key_article": ""
    }


def main():
    # Load tweets
    df = pd.read_excel(TWEETS_FILE)
    interactive = df[df['可互动?'] == '✅ 是'].copy().reset_index(drop=True)
    print(f"可互动推文: {len(interactive)} 条")

    # Load knowledge base articles
    articles = []
    with open(KB_FILE, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            articles.append(row)
    print(f"知识库文章: {len(articles)} 篇")

    results = []

    # Process all tweets, prioritize ⭐⭐⭐ first
    def star_count(row):
        m = re.search(r'(⭐+)', str(row.get('互动角度建议', '')))
        return len(m.group(1)) if m else 0

    interactive['_stars'] = interactive.apply(star_count, axis=1)
    interactive = interactive.sort_values('_stars', ascending=False)

    for i, row in interactive.iterrows():
        tweet_cn = str(row.get('中文翻译', '')).strip()
        angle = str(row.get('互动角度建议', '')).strip()
        account = str(row.get('账号', '')).strip()
        post_time = str(row.get('发布时间', '')).strip()
        link = str(row.get('链接', '')).strip()
        stars = row.get('_stars', 0)

        if not tweet_cn or tweet_cn == 'nan' or '[非英文' in tweet_cn:
            results.append({
                '账号': account,
                '发布时间': post_time,
                '推文内容': tweet_cn,
                '重要度': '⭐' * stars if stars else '⭐',
                '互动角度建议': angle,
                '知识库可回答性': '⚠️ 部分可回答',
                '原因': '推文内容为非英文/空',
                '建议英文回复': '',
                '引用文章': '',
                '链接': link,
            })
            continue

        # Search relevant articles
        search_query = f"{tweet_cn} {angle}"
        relevant = search_articles(search_query, articles)

        print(f"\n[{i+1}] {'⭐'*stars} {account}: {tweet_cn[:60]}...")
        print(f"  找到 {len(relevant)} 篇相关文章: {[a['title'][:30] for a in relevant[:2]]}")

        analysis = analyze_tweet(tweet_cn, angle, relevant)

        print(f"  → {analysis.get('can_answer', '?')}: {analysis.get('reason', '')[:60]}")
        if analysis.get('reply_en'):
            print(f"  → 回复: {analysis.get('reply_en', '')[:80]}...")

        results.append({
            '账号': account,
            '发布时间': post_time,
            '推文内容': tweet_cn[:200],
            '重要度': '⭐' * stars if stars else '⭐',
            '互动角度建议': angle,
            '知识库可回答性': analysis.get('can_answer', ''),
            '原因': analysis.get('reason', ''),
            '建议英文回复': analysis.get('reply_en', ''),
            '引用文章': analysis.get('key_article', ''),
            '链接': link,
        })

        time.sleep(1.5)  # rate limit

    # Save results
    result_df = pd.DataFrame(results)
    result_df.to_excel(OUTPUT_FILE, index=False)
    print(f"\n✅ 结果已保存到: {OUTPUT_FILE}")

    # Summary
    can_answer = result_df[result_df['知识库可回答性'].str.startswith('✅')]
    partial = result_df[result_df['知识库可回答性'].str.startswith('⚠️')]
    cannot = result_df[result_df['知识库可回答性'].str.startswith('❌')]
    print(f"\n统计：")
    print(f"  ✅ 可以回答: {len(can_answer)} 条")
    print(f"  ⚠️ 部分可回答: {len(partial)} 条")
    print(f"  ❌ 内容不足: {len(cannot)} 条")


if __name__ == "__main__":
    main()
