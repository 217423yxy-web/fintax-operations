"""
TwitterAPI.io 客户端
封装 search_user 和 get_user_followings 两个核心接口
"""

import os
import time
import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)


class TwitterAPIClient:
    """TwitterAPI.io REST client for user discovery."""

    BASE_URL = "https://api.twitterapi.io/twitter"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("TWITTER_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "TwitterAPI.io API key is required. "
                "Set TWITTER_API_KEY env var or pass api_key parameter."
            )
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        })
        self._last_request_time = 0
        self._min_interval = 2.0  # 每次请求最少间隔 2 秒

    def _throttle(self):
        """简单速率控制"""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_request_time = time.time()

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """统一请求入口，带重试"""
        url = f"{self.BASE_URL}/{endpoint}"
        for attempt in range(3):
            self._throttle()
            try:
                resp = self.session.request(method, url, **kwargs)
                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 429:
                    wait = 30 * (attempt + 1)
                    logger.warning(f"Rate limited. Waiting {wait}s before retry...")
                    time.sleep(wait)
                    continue
                else:
                    logger.error(f"API error {resp.status_code}: {resp.text[:200]}")
                    resp.raise_for_status()
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (attempt {attempt+1}/3): {e}")
                if attempt < 2:
                    time.sleep(5 * (attempt + 1))
        return {}

    # ─── Core Endpoints ───────────────────────────────────────

    def search_users(self, query: str, cursor: str = "") -> dict:
        """
        搜索用户（基于 Bio / 用户名 / 显示名）

        TwitterAPI.io endpoint: GET /user/search

        Returns:
            {
                "users": [...],
                "next_cursor": "...",
                "has_next_page": true/false
            }
        """
        params = {"query": query, "type": "people"}
        if cursor:
            params["cursor"] = cursor
        return self._request("GET", "user/search", params=params)

    def get_user_info(self, username: str) -> dict:
        """
        获取单个用户详细信息

        TwitterAPI.io endpoint: GET /user/info
        """
        return self._request("GET", "user/info", params={"userName": username})

    def get_user_followings(self, user_id: str, cursor: str = "") -> dict:
        """
        获取用户的 following 列表

        TwitterAPI.io endpoint: GET /user/followings

        Returns:
            {
                "users": [...],
                "next_cursor": "...",
                "has_next_page": true/false
            }
        """
        params = {"userId": user_id}
        if cursor:
            params["cursor"] = cursor
        return self._request("GET", "user/followings", params=params)

    def get_user_followers(self, user_id: str, cursor: str = "") -> dict:
        """
        获取用户的 follower 列表

        TwitterAPI.io endpoint: GET /user/followers
        """
        params = {"userId": user_id}
        if cursor:
            params["cursor"] = cursor
        return self._request("GET", "user/followers", params=params)

    def advanced_search(self, query: str, cursor: str = "") -> dict:
        """
        高级搜索推文

        TwitterAPI.io endpoint: POST /tweet/advanced_search
        """
        payload = {"query": query, "queryType": "Latest"}
        if cursor:
            payload["cursor"] = cursor
        return self._request("POST", "tweet/advanced_search", json=payload)
