#!/usr/bin/env python3
"""
两轮质检：new_100_replies.xlsx
Round 1: 推文匹配度（回帖是否真的回应了推文话题）
Round 2: 知识库幻觉检查（回帖中的具体事实/规则是否有KB依据）
输出：new_100_replies_qc.xlsx（新增6列质检结果）
"""

import json
import time
import pandas as pd
import anthropic

client = anthropic.Anthropic()

# ─── Round 1: 推文匹配度 ───────────────────────────────────────────
MATCH_SYSTEM = """You are a quality checker for crypto tax Twitter replies.
Evaluate whether a reply is well-matched to its original tweet.

Output valid JSON only, no markdown, no explanation.
Format:
{
  "match_score": <1-5>,
  "match_issue": "<short issue description or empty string>"
}

Scoring:
5 = Perfect match. Reply directly addresses the tweet's core topic with relevant insight.
4 = Good match. Reply is on-topic but adds a tangentially related point.
3 = Weak match. Reply is in the same general domain but misses the tweet's focus.
2 = Poor match. Reply barely connects to the tweet content.
1 = Mismatch. Reply seems to be for a different tweet entirely.

match_issue should be empty for score 4-5. For 1-3, briefly state the disconnect (max 80 chars)."""

def check_match(tweet: str, reply: str) -> dict:
    prompt = f"""Original tweet:
{tweet}

Reply to evaluate:
{reply}

Evaluate match quality. Output JSON only."""

    for attempt in range(3):
        try:
            resp = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=150,
                system=MATCH_SYSTEM,
                messages=[{"role": "user", "content": prompt}]
            )
            text = resp.content[0].text.strip()
            return json.loads(text)
        except Exception as e:
            print(f"  [Match] attempt {attempt+1} error: {e}")
            time.sleep(1)
    return {"match_score": 0, "match_issue": "API_ERROR"}


# ─── Round 2: 知识库幻觉检查 ──────────────────────────────────────
HALLUC_SYSTEM = """You are a fact-checker for crypto tax Twitter replies.
Check if the reply's specific claims are supported by the knowledge base content.

Output valid JSON only, no markdown, no explanation.
Format:
{
  "halluc_risk": "low|medium|high",
  "halluc_issue": "<specific unsupported claim or empty string>"
}

Rules:
- "low": All specific facts in the reply (form numbers, thresholds, rule names, percentages) are either present in the KB or are widely-known public facts.
- "medium": Reply contains a specific claim that is plausible but NOT directly in the KB content.
- "high": Reply contains a specific claim that CONTRADICTS the KB, or invents precise figures/rules with no KB basis.
- If the reply is purely conceptual (no specific numbers/rules), default to "low".
- halluc_issue should name the specific unsupported/contradicting claim (max 100 chars). Empty for "low"."""

def check_hallucination(reply: str, kb_content: str) -> dict:
    kb_excerpt = str(kb_content)[:800] if kb_content else "[No KB content]"
    prompt = f"""Reply to fact-check:
{reply}

Knowledge base content retrieved for this tweet:
{kb_excerpt}

Check if reply's specific claims are supported. Output JSON only."""

    for attempt in range(3):
        try:
            resp = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=150,
                system=HALLUC_SYSTEM,
                messages=[{"role": "user", "content": prompt}]
            )
            text = resp.content[0].text.strip()
            return json.loads(text)
        except Exception as e:
            print(f"  [Halluc] attempt {attempt+1} error: {e}")
            time.sleep(1)
    return {"halluc_risk": "unknown", "halluc_issue": "API_ERROR"}


# ─── 综合评级 ─────────────────────────────────────────────────────
def overall_verdict(match_score: int, halluc_risk: str) -> str:
    if match_score >= 4 and halluc_risk == "low":
        return "✅ 通过"
    elif halluc_risk == "high":
        return "🔴 重写"
    elif match_score <= 2:
        return "🔴 重写"
    else:
        return "🟡 改进"


# ─── 主流程 ───────────────────────────────────────────────────────
def main():
    input_file = "new_100_replies.xlsx"
    output_file = "new_100_replies_qc.xlsx"

    print(f"Loading {input_file}...")
    df = pd.read_excel(input_file)
    total = len(df)
    print(f"Total rows: {total}")

    # Init new columns
    df["匹配分(1-5)"] = 0
    df["匹配问题"] = ""
    df["幻觉风险"] = ""
    df["幻觉问题"] = ""
    df["综合评级"] = ""

    pass_count = rewrite_count = improve_count = 0

    for i, row in df.iterrows():
        tweet = str(row.get("推文（英文）", ""))
        reply = str(row.get("回帖（英文）", ""))
        kb = str(row.get("知识库内容", ""))
        account = str(row.get("账号", ""))

        print(f"[{i+1}/{total}] {account}")

        # Round 1
        m = check_match(tweet, reply)
        match_score = m.get("match_score", 0)
        match_issue = m.get("match_issue", "")
        print(f"  Match: {match_score}/5  {match_issue[:60] if match_issue else ''}")

        # Round 2
        h = check_hallucination(reply, kb)
        halluc_risk = h.get("halluc_risk", "unknown")
        halluc_issue = h.get("halluc_issue", "")
        print(f"  Halluc: {halluc_risk}  {halluc_issue[:60] if halluc_issue else ''}")

        # Verdict
        verdict = overall_verdict(match_score, halluc_risk)
        if "通过" in verdict: pass_count += 1
        elif "重写" in verdict: rewrite_count += 1
        else: improve_count += 1

        print(f"  → {verdict}")

        df.at[i, "匹配分(1-5)"] = match_score
        df.at[i, "匹配问题"] = match_issue
        df.at[i, "幻觉风险"] = halluc_risk
        df.at[i, "幻觉问题"] = halluc_issue
        df.at[i, "综合评级"] = verdict

        # Save checkpoint every 20 rows
        if (i + 1) % 20 == 0:
            df.to_excel(output_file, index=False)
            print(f"  [Checkpoint saved at row {i+1}]")

        time.sleep(0.3)

    df.to_excel(output_file, index=False)

    print("\n" + "="*50)
    print("质检完成！")
    print(f"✅ 通过:  {pass_count}")
    print(f"🟡 改进:  {improve_count}")
    print(f"🔴 重写:  {rewrite_count}")
    print(f"输出文件: {output_file}")
    print("="*50)

    # Print rewrite candidates
    rewrite_df = df[df["综合评级"].str.contains("重写", na=False)]
    if not rewrite_df.empty:
        print(f"\n需要重写的 {len(rewrite_df)} 条回帖：")
        for _, row in rewrite_df.iterrows():
            print(f"  账号: {row['账号']}  匹配:{row['匹配分(1-5)']}  幻觉:{row['幻觉风险']}")
            if row['匹配问题']: print(f"    匹配问题: {row['匹配问题']}")
            if row['幻觉问题']: print(f"    幻觉问题: {row['幻觉问题']}")

if __name__ == "__main__":
    main()
