#!/usr/bin/env python3
"""Upload TaxDAO Chinese articles to Dify knowledge base."""

import csv
import json
import time
import requests

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZTA2ZmI5NTEtZTMwMC00ZTE0LTg4N2QtNWVmMmE5Yjc4ZDZlIiwiZXhwIjoxNzc0OTYzNjEzLCJpc3MiOiJTRUxGX0hPU1RFRCIsInN1YiI6IkNvbnNvbGUgQVBJIFBhc3Nwb3J0In0.0sgNWlZTtXrLaNylJSjXeW2DSVUXZVRpf3Hd5QZxmiY"
CSRF_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzQ5NjM2MTMsInN1YiI6ImUwNmZiOTUxLWUzMDAtNGUxNC04ODdkLTVlZjJhOWI3OGQ2ZSJ9.f5uVAJw7GH8JTpYaCoNiYIhxTWP6fTGQ2bAVPCZ6xzA"
DATASET_ID = "35bc4e08-4d42-4d4c-93a3-16485f297ea4"
BASE_URL = "http://localhost/console/api"
CSV_FILE = "/Users/nightyoung/Desktop/taxdao_articles_cn.csv"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "X-CSRF-Token": CSRF_TOKEN,
    "Content-Type": "application/json",
    "Cookie": f"access_token={ACCESS_TOKEN}; csrf_token={CSRF_TOKEN}",
}

def upload_article(article_id, title, keyword, digest, content, create_time):
    """Upload a single article as a document."""
    # Combine metadata + content into the document text
    doc_text = f"标题：{title}\n关键词：{keyword}\n摘要：{digest}\n发布时间：{create_time}\n\n{content}"

    payload = {
        "name": title[:200],  # max title length
        "text": doc_text,
        "indexing_technique": "high_quality",
        "doc_form": "text_model",
        "doc_language": "zh-Hans",
        "process_rule": {
            "mode": "automatic"
        }
    }

    resp = requests.post(
        f"{BASE_URL}/datasets/{DATASET_ID}/document/create-by-text",
        headers=HEADERS,
        json=payload,
        timeout=30,
    )
    return resp.status_code, resp.json()


def main():
    articles = []
    with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            articles.append(row)

    print(f"Total articles to upload: {len(articles)}")

    success = 0
    failed = 0

    for i, article in enumerate(articles):
        art_id = article.get('id', '')
        title = article.get('title', '').strip()
        keyword = article.get('keyword', '').strip()
        digest = article.get('digest', '').strip()
        content = article.get('article', '').strip()
        create_time = article.get('createTime', '').strip()

        if not title or not content:
            print(f"[{i+1}/{len(articles)}] Skipping article {art_id}: empty title or content")
            continue

        status, result = upload_article(art_id, title, keyword, digest, content, create_time)

        if status == 200 and 'document' in result:
            success += 1
            doc_id = result['document']['id']
            print(f"[{i+1}/{len(articles)}] OK: {title[:50]}... (doc_id={doc_id})")
        else:
            failed += 1
            print(f"[{i+1}/{len(articles)}] FAIL (status={status}): {title[:50]}... -> {str(result)[:100]}")

        # Rate limiting: avoid overwhelming the API
        time.sleep(0.3)

        # Save progress every 50 articles
        if (i + 1) % 50 == 0:
            print(f"\n--- Progress: {success} success, {failed} failed ---\n")

    print(f"\nDone! Total: {success} success, {failed} failed")


if __name__ == "__main__":
    main()
