#!/usr/bin/env python3
"""
Path A 测试：转推/引用链深挖
对指定账号的最新推文，抓取转推者列表，筛选出行业相关账号

运行：
  python3.11 path_a_retweeters.py
"""
import asyncio
import json
import time
from pathlib import Path

# twikit ClientTransaction patch
import twikit.x_client_transaction.transaction as _txn

async def _patched_init(self, session, headers):
    self.home_page_response = None
    self.DEFAULT_ROW_INDEX = 2
    self.DEFAULT_KEY_BYTES_INDICES = [12, 14]
    self.key = "obfiowerehiring"
    self.key_bytes = [0] * 64
    self.animation_key = "0" * 16

_txn.ClientTransaction.init = _patched_init
_txn.ClientTransaction.generate_transaction_id = lambda self, method, path, **kw: ""

from twikit import Client

# ── 测试账号（10 个）──────────────────────────────────────────────────────────
TEST_HANDLES = [
    "binance", "coinbase", "Bybit_Official", "kucoincom", "gate_io",
    "cryptocom", "MEXC_Official", "Gemini", "Bitstamp", "HashKeyExchange",
]

# Bio 关键词过滤（命中任一则保留）
RELEVANT_KEYWORDS = [
    "crypto", "bitcoin", "blockchain", "defi", "web3", "exchange",
    "trading", "finance", "fintech", "compliance", "tax", "fund",
    "invest", "venture", "capital", "token", "nft", "staking",
    "custody", "wallet", "payment", "mining", "regulation",
]

OUTPUT_FILE = Path("output/path_a_retweeters_test.json")
MIN_FOLLOWERS = 100  # 过滤掉小账号


def is_relevant(user) -> bool:
    """判断账号是否行业相关"""
    bio = (user.description or "").lower()
    name = (user.name or "").lower()
    return any(kw in bio or kw in name for kw in RELEVANT_KEYWORDS)


def load_cookies() -> dict:
    cookie_file = Path.home() / "twitter_cookies.json"
    with open(cookie_file, encoding="utf-8") as f:
        raw = json.load(f)
    return {c["name"]: c["value"] for c in raw}


async def fetch_retweeters(client, handle: str) -> list[dict]:
    """抓取账号最新推文的转推者"""
    results = []
    try:
        user = await client.get_user_by_screen_name(handle)
        tweets = await client.get_user_tweets(user.id, "Tweets", count=1)

        if not tweets:
            print(f"  @{handle}: 没有推文")
            return []

        tweet = tweets[0]
        print(f"  @{handle}: 最新推文「{tweet.full_text[:50].replace(chr(10),' ')}...」")
        print(f"           转推数={tweet.retweet_count}  引用数={tweet.quote_count}")

        if tweet.retweet_count == 0:
            print(f"           无转推，跳过")
            return []

        # 抓转推者（最多 100 个）
        retweeters = await tweet.get_retweeters(count=100)
        for u in retweeters:
            followers = u.followers_count or 0
            if followers < MIN_FOLLOWERS:
                continue
            results.append({
                "source_handle": handle,
                "source_tweet_id": tweet.id,
                "source_tweet": tweet.full_text[:100],
                "discovery_type": "retweet",
                "handle": u.screen_name,
                "name": u.name,
                "followers": followers,
                "bio": u.description or "",
                "relevant": is_relevant(u),
                "url": f"https://x.com/{u.screen_name}",
            })

        relevant_count = sum(1 for r in results if r["relevant"] and r["source_handle"] == handle)
        print(f"           转推者 {len(retweeters)} 个 → 粉丝>{MIN_FOLLOWERS} 的 {len([r for r in results if r['source_handle']==handle])} 个 → 行业相关 {relevant_count} 个")

    except Exception as e:
        print(f"  @{handle}: 错误 - {e}")

    return results


async def main():
    client = Client("en-US")
    client.set_cookies(load_cookies())
    print(f"Cookies 加载完成，开始抓取 {len(TEST_HANDLES)} 个账号...\n")

    all_results = []
    for i, handle in enumerate(TEST_HANDLES):
        print(f"[{i+1}/{len(TEST_HANDLES)}] @{handle}")
        results = await fetch_retweeters(client, handle)
        all_results.extend(results)
        if i < len(TEST_HANDLES) - 1:
            await asyncio.sleep(3)

    # 去重（同一个账号可能转推了多家企业）
    seen = {}
    for r in all_results:
        h = r["handle"]
        if h not in seen:
            seen[h] = r
            seen[h]["discovered_via"] = [r["source_handle"]]
        else:
            seen[h]["discovered_via"].append(r["source_handle"])

    unique_results = list(seen.values())
    relevant_results = [r for r in unique_results if r["relevant"]]

    # 按粉丝数排序
    unique_results.sort(key=lambda x: x["followers"], reverse=True)
    relevant_results.sort(key=lambda x: x["followers"], reverse=True)

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "summary": {
                "tested_handles": TEST_HANDLES,
                "total_discovered": len(unique_results),
                "relevant_accounts": len(relevant_results),
                "multi_source": len([r for r in unique_results if len(r.get("discovered_via", [])) > 1]),
            },
            "relevant": relevant_results,
            "all": unique_results,
        }, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"完成！发现 {len(unique_results)} 个唯一账号")
    print(f"行业相关：{len(relevant_results)} 个")
    print(f"多源交叉：{len([r for r in unique_results if len(r.get('discovered_via',[])) > 1])} 个")
    print(f"输出：{OUTPUT_FILE}")

    # 打印前 10 个相关账号预览
    if relevant_results:
        print(f"\n--- Top 10 行业相关账号 ---")
        for r in relevant_results[:10]:
            via = ", ".join(r.get("discovered_via", [r["source_handle"]]))
            print(f"@{r['handle']} ({r['followers']:,} 粉丝) via {via}")
            print(f"  Bio: {r['bio'][:80]}")


if __name__ == "__main__":
    asyncio.run(main())
