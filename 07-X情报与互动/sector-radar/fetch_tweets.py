#!/usr/bin/env python3
"""
批量获取 CEX 账号最新推文
用法: TWITTER_API_KEY=xxx python fetch_tweets.py

充值 TwitterAPI.io 额度后运行此脚本即可补全所有账号。
"""
import os, sys, json, time, requests
from datetime import datetime

API_KEY = os.environ.get("TWITTER_API_KEY", "")
if not API_KEY:
    print("请设置 TWITTER_API_KEY 环境变量")
    sys.exit(1)

BASE = "https://api.twitterapi.io/twitter"
HEADERS = {"X-API-Key": API_KEY}

CEX_ACCOUNTS = [
    "binance","coinbase","kraken","okx","Bybit_Official","bitget",
    "kucoincom","gate_io","cryptocom","MEXC_Official","Gemini",
    "Bitstamp","Official_Upbit","bitfinex","HTX_Global",
    "DeribitExchange","Phemex_official","BingXOfficial","BitMartExchange",
    "LBank_Exchange","Poloniex","WhiteBit","CoinExGlobal","AscendEX_Global",
    "ProBit_Exchange","BithumbOfficial","CoinoneOfficial","BitkubOfficial",
    "coinhako","LunoGlobal","korbit","CoinDCX","WazirXIndia","Bitso",
    "BTSEcom","blockchain","swissborg","BullishGlobal","BackpackExchange",
    "HashKeyExchange","bitflyer","Bitvavo","Bitpanda","rainfinancial",
    "MercadoBitcoin","Swyftx","coincheckjp","inreserve"
]

results = []
errors = []

for i, handle in enumerate(CEX_ACCOUNTS):
    print(f"[{i+1}/{len(CEX_ACCOUNTS)}] @{handle}...", end=" ", flush=True)
    for attempt in range(3):
        try:
            resp = requests.get(
                f"{BASE}/user/last_tweets",
                params={"userName": handle, "count": 1},
                headers=HEADERS, timeout=30
            )
            data = resp.json()
            if data.get("status") == "success":
                tweets = data.get("data", {}).get("tweets", [])
                if tweets:
                    t = tweets[0]
                    results.append({
                        "handle": handle,
                        "name": t.get("author", {}).get("name", handle),
                        "text": t.get("text", ""),
                        "date": t.get("createdAt", ""),
                        "likes": t.get("likeCount", 0),
                        "retweets": t.get("retweetCount", 0),
                        "views": t.get("viewCount", 0),
                        "url": t.get("url", ""),
                    })
                    print(f"✓ {t.get('text','')[:50]}")
                    break
                else:
                    print("(no tweets)")
                    errors.append(handle)
                    break
            elif "Too Many Requests" in str(data):
                print(f"(rate limit, retry {attempt+1})...", end=" ", flush=True)
                time.sleep(15)
            elif "Credits" in str(data.get("message", "")):
                print(f"\n\n❌ API 额度不足！已获取 {len(results)} 条。请充值后重新运行。")
                break
            else:
                print(f"(error: {data.get('msg', 'unknown')})")
                errors.append(handle)
                break
        except Exception as e:
            print(f"(exception: {e})")
            errors.append(handle)
            break
    time.sleep(6)  # 免费版 5s 限速

# 保存 JSON
outfile = f"output/cex_tweets_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
os.makedirs("output", exist_ok=True)
with open(outfile, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\n✅ 完成: {len(results)} 条推文已保存到 {outfile}")
if errors:
    print(f"⚠️  {len(errors)} 个账号失败: {errors}")
