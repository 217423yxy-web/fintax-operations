#!/usr/bin/env python3
"""
Generate replies for 76 tweets based on kb_chunks content.
Merges search_tweets_with_kb.json into search_matches_v3.json and regenerates final_reply.
"""
import json
import time
import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are an industry observer specializing in crypto taxation and compliance.
You reply to tweets about crypto taxes with concise, insightful comments.

Rules:
- Tone: neutral industry observer, NOT promotional, no sales language
- Structure: phenomenon → rule → conclusion (minimal complete point)
- Angles: counter-intuitive insight / rule clarification / practical scenario
- Length: strictly under 220 characters
- Language: English only
- Do NOT mention any brand names or company names (especially FinTax)
- Ground the reply in the specific knowledge base content provided
- Be specific: cite actual rules, thresholds, form numbers, or regulatory details from the KB"""

def build_prompt(tweet_text: str, kb_chunks: list, tweet_cn: str = "") -> str:
    chunks_text = ""
    for i, chunk in enumerate(kb_chunks):
        score = chunk.get("score", 0)
        text = chunk.get("text", "").strip()
        if text and len(text) > 10:
            chunks_text += f"\n[KB Chunk {i+1}, relevance={score:.3f}]\n{text[:600]}\n"

    prompt = f"""Tweet to reply to:
{tweet_text}

Knowledge base content retrieved for this tweet:
{chunks_text if chunks_text else "[No specific KB content retrieved]"}

Task: Write a reply tweet that:
1. Draws on specific facts, rules, or data from the KB chunks above
2. Adds insight the original tweet missed or reinforces with a concrete rule/scenario
3. Is strictly under 220 characters
4. Picks one angle: counter-intuitive / rule clarification / practical scenario

Reply (just the text, no quotes, no hashtags):"""
    return prompt

def classify_angle(reply: str, tweet_text: str) -> str:
    """Classify the angle based on reply content."""
    reply_lower = reply.lower()
    tweet_lower = tweet_text.lower()

    counter_signals = ["actually", "opposite", "wrong", "not what", "misses", "reverse", "counterintuitive", "can reverse", "but actually", "irony"]
    rule_signals = ["under irs", "rev. rul.", "pub.", "form ", "schedule", "section", "rule", "regulation", "threshold", "require", "must report", "no exception", "until congress"]
    scenario_signals = ["example", "e.g.", "scenario", "if you", "say you", "imagine", "real case", "client", "basis becomes", "when you sell"]

    counter_count = sum(1 for s in counter_signals if s in reply_lower)
    rule_count = sum(1 for s in rule_signals if s in reply_lower)
    scenario_count = sum(1 for s in scenario_signals if s in reply_lower)

    max_count = max(counter_count, rule_count, scenario_count)
    if max_count == 0:
        return "规则解读型"
    if counter_count == max_count:
        return "反直觉观点型"
    if scenario_count == max_count:
        return "场景落地型"
    return "规则解读型"

def generate_reply(tweet_text: str, kb_chunks: list, tweet_cn: str = "", max_retries: int = 3) -> str:
    prompt = build_prompt(tweet_text, kb_chunks, tweet_cn)

    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=300,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
            reply = response.content[0].text.strip()
            # Remove quotes if present
            if reply.startswith('"') and reply.endswith('"'):
                reply = reply[1:-1]
            # Truncate if over 220
            if len(reply) > 220:
                # Try to cut at last sentence/clause boundary
                truncated = reply[:217]
                # find last period or comma
                for sep in ['. ', ', ', ' — ', ' - ', ' ']:
                    idx = truncated.rfind(sep)
                    if idx > 150:
                        truncated = truncated[:idx]
                        break
                reply = truncated + "..."
            return reply
        except Exception as e:
            print(f"  Error on attempt {attempt+1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)

    return ""  # fallback empty

def main():
    print("Loading files...")
    with open('search_matches_v3.json') as f:
        v3 = json.load(f)
    with open('search_tweets_with_kb.json') as f:
        kb_data = json.load(f)

    print(f"Total records: {len(v3)}")

    used_kb_count = 0
    over_220_count = 0

    for i, (record, kb_item) in enumerate(zip(v3, kb_data)):
        tweet_text = record.get('tweet_text', '')
        tweet_cn = record.get('tweet_cn', '')
        kb_chunks = kb_item.get('kb_chunks', [])
        relevance = kb_item.get('relevance', 0)

        # Merge kb data
        record['kb_chunks'] = kb_chunks
        record['relevance'] = relevance

        print(f"[{i+1}/76] @{record['tweet_account']} relevance={relevance}")

        # Determine if KB has useful content
        has_useful_kb = bool(kb_chunks) and any(
            len(c.get('text', '').strip()) > 30 for c in kb_chunks
        )

        if has_useful_kb:
            used_kb_count += 1

        reply = generate_reply(tweet_text, kb_chunks if has_useful_kb else [], tweet_cn)

        if not reply:
            # fallback to existing final_reply
            reply = record.get('final_reply', '')
            print(f"  -> FALLBACK to existing reply")
        else:
            angle = classify_angle(reply, tweet_text)
            record['final_reply'] = reply
            record['final_angle'] = angle

            if len(reply) > 220:
                over_220_count += 1
                print(f"  -> OVER 220: {len(reply)} chars")
            else:
                print(f"  -> OK ({len(reply)} chars): {reply[:80]}...")

        # Small delay to avoid rate limits
        time.sleep(0.3)

    # Save output
    with open('search_matches_v3.json', 'w', encoding='utf-8') as f:
        json.dump(v3, f, ensure_ascii=False, indent=2)

    print("\n=== SUMMARY ===")
    print(f"Total records: {len(v3)}")
    print(f"Over 220 chars: {over_220_count}")
    print(f"Used kb_chunks: {used_kb_count}")

if __name__ == '__main__':
    main()
