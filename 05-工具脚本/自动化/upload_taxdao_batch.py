#!/usr/bin/env python3
"""Batch upload TaxDAO Chinese articles to Dify knowledge base via file upload API."""

import csv
import json
import os
import time
import tempfile
import requests

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZTA2ZmI5NTEtZTMwMC00ZTE0LTg4N2QtNWVmMmE5Yjc4ZDZlIiwiZXhwIjoxNzc0OTYzNjEzLCJpc3MiOiJTRUxGX0hPU1RFRCIsInN1YiI6IkNvbnNvbGUgQVBJIFBhc3Nwb3J0In0.0sgNWlZTtXrLaNylJSjXeW2DSVUXZVRpf3Hd5QZxmiY"
CSRF_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzQ5NjM2MTMsInN1YiI6ImUwNmZiOTUxLWUzMDAtNGUxNC04ODdkLTVlZjJhOWI3OGQ2ZSJ9.f5uVAJw7GH8JTpYaCoNiYIhxTWP6fTGQ2bAVPCZ6xzA"
DATASET_ID = "35bc4e08-4d42-4d4c-93a3-16485f297ea4"
BASE_URL = "http://localhost/console/api"
CSV_FILE = "/Users/nightyoung/Desktop/taxdao_articles_cn.csv"

# Upload in batches of 5 to reduce API calls
BATCH_SIZE = 5

HEADERS_BASE = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "X-CSRF-Token": CSRF_TOKEN,
    "Cookie": f"access_token={ACCESS_TOKEN}; csrf_token={CSRF_TOKEN}",
}


def upload_file(content: str, filename: str):
    """Upload text content as a file, return file_id."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', encoding='utf-8', delete=False) as f:
        f.write(content)
        tmp_path = f.name

    try:
        with open(tmp_path, 'rb') as f:
            resp = requests.post(
                f"{BASE_URL}/files/upload",
                headers=HEADERS_BASE,
                files={"file": (filename, f, "text/plain")},
                data={"source": "datasets"},
                timeout=30,
            )
        if resp.status_code == 201 or resp.status_code == 200:
            return resp.json()["id"]
        else:
            print(f"  File upload failed: {resp.status_code} {resp.text[:100]}")
            return None
    finally:
        os.unlink(tmp_path)


def add_documents(file_ids):
    """Add uploaded files to the dataset."""
    payload = {
        "indexing_technique": "high_quality",
        "data_source": {
            "info_list": {
                "data_source_type": "upload_file",
                "file_info_list": {"file_ids": file_ids}
            }
        },
        "process_rule": {"mode": "automatic"},
        "doc_form": "text_model",
        "doc_language": "zh-Hans",
    }
    resp = requests.post(
        f"{BASE_URL}/datasets/{DATASET_ID}/documents",
        headers={**HEADERS_BASE, "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"  Dataset add failed: {resp.status_code} {resp.text[:200]}")
        return None


def main():
    articles = []
    with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            articles.append(row)

    print(f"Total articles: {len(articles)}")
    print(f"Batch size: {BATCH_SIZE}")

    success = 0
    failed = 0
    i = 0

    while i < len(articles):
        batch = articles[i:i + BATCH_SIZE]
        batch_file_ids = []
        batch_titles = []

        # Upload each file in batch
        for article in batch:
            art_id = article.get('id', '')
            title = article.get('title', '').strip()
            keyword = article.get('keyword', '').strip()
            digest = article.get('digest', '').strip()
            content = article.get('article', '').strip()
            create_time = article.get('createTime', '').strip()

            if not title or not content:
                continue

            doc_text = f"标题：{title}\n关键词：{keyword}\n摘要：{digest}\n发布时间：{create_time}\n\n{content}"
            # Use safe filename
            safe_title = "".join(c for c in title[:40] if c.isalnum() or c in ' -_').strip()
            filename = f"{art_id}_{safe_title}.txt"

            file_id = upload_file(doc_text, filename)
            if file_id:
                batch_file_ids.append(file_id)
                batch_titles.append(title[:50])
            else:
                failed += 1

        if batch_file_ids:
            result = add_documents(batch_file_ids)
            if result and "documents" in result:
                doc_count = len(result["documents"])
                success += doc_count
                print(f"[{i+1}-{i+len(batch)}/{len(articles)}] Added {doc_count} docs: {batch_titles[0]}...")
            else:
                failed += len(batch_file_ids)
                print(f"[{i+1}-{i+len(batch)}/{len(articles)}] FAIL batch")

        i += BATCH_SIZE

        # Small delay to avoid rate limiting
        time.sleep(0.5)

        if i % 50 == 0:
            print(f"\n--- Progress: {success} success, {failed} failed ---\n")

    print(f"\nDone! Total: {success} success, {failed} failed")


if __name__ == "__main__":
    main()
