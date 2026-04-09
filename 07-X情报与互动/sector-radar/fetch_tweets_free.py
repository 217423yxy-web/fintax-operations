#!/usr/bin/env python3
"""
基于 twikit 的免费推文抓取工具（零 API 费用，无浏览器）

用法:
  # 安装依赖（仅首次）
  pip install twikit

  # 抓取所有 CEX 账号的最新推文
  python fetch_tweets_free.py

  # 抓取指定账号
  python fetch_tweets_free.py --handles binance coinbase okx

  # 指定每个账号抓取的推文数量
  python fetch_tweets_free.py --count 5
"""

import argparse
import asyncio
import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path

from twikit import Client

# ── 绕过 ClientTransaction 签名（ondemand.s.a.js 返回 404 导致 KEY_BYTE 提取失败）
# 只读操作传空 transaction ID 不影响结果，社区已确认
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

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

# ── 全部 CEX 账号 ──
CEX_HANDLES = [
    "binance", "coinbase", "kraken", "okx", "Bybit_Official", "bitget",
    "kucoincom", "gate_io", "cryptocom", "MEXC_Official", "Gemini",
    "Bitstamp", "Official_Upbit", "bitfinex", "HTX_Global",
    "DeribitExchange", "Phemex_official", "BingXOfficial", "BitMartExchange",
    "LBank_Exchange", "Poloniex", "WhiteBit", "CoinExGlobal", "AscendEX_Global",
    "ProBit_Exchange", "BithumbOfficial", "CoinoneOfficial", "BitkubOfficial",
    "coinhako", "LunoGlobal", "korbit", "CoinDCX", "WazirXIndia", "Bitso",
    "BTSEcom", "blockchain", "swissborg", "BullishGlobal", "BackpackExchange",
    "HashKeyExchange", "bitflyer", "Bitvavo", "Bitpanda", "rainfinancial",
    "MercadoBitcoin", "Swyftx", "coincheckjp", "inreserve",
]


def load_cookies() -> dict:
    """从 ~/twitter_cookies.json 加载 cookies，转换为 twikit 所需的 dict 格式"""
    cookie_file = Path.home() / "twitter_cookies.json"
    if not cookie_file.exists():
        raise FileNotFoundError(f"未找到 {cookie_file}，请先登录 Twitter 并导出 cookies")
    with open(cookie_file, encoding="utf-8") as f:
        raw = json.load(f)
    # twikit 需要 {name: value} 格式
    return {c["name"]: c["value"] for c in raw}


async def fetch_all(handles: list, count: int, delay: float, output_file: str) -> tuple[list, list]:
    client = Client("en-US")
    client.set_cookies(load_cookies())
    logger.info("Cookies 加载完成，开始抓取（纯 HTTP，无浏览器）")

    # 加载已有进度（支持断点续抓）
    if Path(output_file).exists():
        with open(output_file, encoding="utf-8") as f:
            all_tweets = json.load(f)
        done_handles = {t["handle"] for t in all_tweets}
        logger.info(f"续抓模式：已有 {len(all_tweets)} 条，跳过 {len(done_handles)} 个账号")
    else:
        all_tweets = []
        done_handles = set()

    errors = []

    for i, handle in enumerate(handles):
        if handle in done_handles:
            logger.info(f"[{i+1}/{len(handles)}] @{handle} 已完成，跳过")
            continue

        logger.info(f"[{i+1}/{len(handles)}] @{handle}")
        try:
            user = await client.get_user_by_screen_name(handle)
            results = await client.get_user_tweets(user.id, "Tweets", count=count)

            new_tweets = []
            for tweet in results:
                if tweet.retweeted_tweet:
                    continue
                new_tweets.append({
                    "handle": handle,
                    "text": tweet.full_text,
                    "date": tweet.created_at,
                    "likes": tweet.favorite_count,
                    "retweets": tweet.retweet_count,
                    "replies": tweet.reply_count,
                    "views": tweet.view_count or 0,
                    "url": f"https://x.com/{handle}/status/{tweet.id}",
                    "source": "twikit",
                })
            all_tweets.extend(new_tweets)

            preview = new_tweets[-1]["text"][:60].replace("\n", " ") if new_tweets else ""
            logger.info(f"  ✓ 获取 {len(new_tweets)} 条 | {preview}")

            # 每个账号抓完立即保存
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(all_tweets, f, ensure_ascii=False, indent=2)

        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "Rate limit" in err_str:
                wait = 60
                logger.warning(f"  ✗ @{handle}: 429 限速，等待 {wait}s 后重试...")
                await asyncio.sleep(wait)
                # 重试一次
                try:
                    user = await client.get_user_by_screen_name(handle)
                    results = await client.get_user_tweets(user.id, "Tweets", count=count)
                    new_tweets = [
                        {
                            "handle": handle,
                            "text": t.full_text,
                            "date": t.created_at,
                            "likes": t.favorite_count,
                            "retweets": t.retweet_count,
                            "replies": t.reply_count,
                            "views": t.view_count or 0,
                            "url": f"https://x.com/{handle}/status/{t.id}",
                            "source": "twikit",
                        }
                        for t in results if not t.retweeted_tweet
                    ]
                    all_tweets.extend(new_tweets)
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(all_tweets, f, ensure_ascii=False, indent=2)
                    logger.info(f"  ✓ 重试成功，获取 {len(new_tweets)} 条")
                except Exception as e2:
                    logger.error(f"  ✗ @{handle}: 重试失败 {e2}")
                    errors.append(handle)
            else:
                logger.error(f"  ✗ @{handle}: {e}")
                errors.append(handle)

        if i < len(handles) - 1:
            await asyncio.sleep(delay)

    return all_tweets, errors


def main():
    parser = argparse.ArgumentParser(description="twikit 免费推文抓取工具（无浏览器）")
    parser.add_argument("--handles", nargs="+", default=None, help="指定账号列表（默认全部 CEX）")
    parser.add_argument("--count", type=int, default=1, help="每个账号抓取推文数（默认 1）")
    parser.add_argument("--delay", type=float, default=2, help="每个账号间隔秒数（默认 2）")
    parser.add_argument("--output", type=str, default=None, help="输出 JSON 文件路径")
    args = parser.parse_args()

    handles = args.handles or CEX_HANDLES
    logger.info(f"共 {len(handles)} 个账号，每个取 {args.count} 条，间隔 {args.delay}s")
    logger.info(f"预计耗时: ~{len(handles) * (args.delay + 1) / 60:.1f} 分钟\n")

    output_file = args.output or f"output/cex_tweets_twikit_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    all_tweets, errors = asyncio.run(fetch_all(handles, args.count, args.delay, output_file))

    logger.info(f"\n{'='*50}")
    logger.info(f"完成: {len(all_tweets)} 条推文 → {output_file}")
    if errors:
        logger.warning(f"失败 {len(errors)} 个: {errors}")
    logger.info("费用: $0（免费）")


if __name__ == "__main__":
    main()
