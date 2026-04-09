"""
Step 1 Pipeline: 赛道企业发现
给定一个赛道 ID，通过三条路径找到 100 家企业的 X 账号

路径 A: 种子企业（内置 10-15 家头部）
路径 B: TwitterAPI.io search_user — Bio 关键词搜索
路径 C: 种子企业 following 网络中的同赛道企业
"""

import logging
import json
import re
from datetime import datetime
from typing import List, Set, Dict, Optional

from .sectors import Sector, Company, get_sector, SECTORS
from .twitter_client import TwitterAPIClient

logger = logging.getLogger(__name__)


class SectorPipeline:
    """从种子企业扩展到 100 家赛道企业"""

    def __init__(self, client: TwitterAPIClient, target: int = 100):
        self.client = client
        self.target = target
        self._seen_handles: Set[str] = set()   # 全局去重（小写）
        self._results: List[Company] = []

    def _is_new(self, handle: str) -> bool:
        return handle.lower() not in self._seen_handles

    def _add(self, company: Company) -> bool:
        key = company.x_handle.lower()
        if key in self._seen_handles:
            return False
        self._seen_handles.add(key)
        self._results.append(company)
        return True

    # ──── Path A: 种子企业 ────────────────────────────────

    def _load_seeds(self, sector: Sector) -> int:
        """加载内置种子企业"""
        added = 0
        for c in sector.seed_companies:
            c.sector = sector.id
            c.source = "seed"
            if self._add(c):
                added += 1
        logger.info(f"[Path A] Loaded {added} seed companies for {sector.name_en}")
        return added

    # ──── Path B: Bio 搜索 ────────────────────────────────

    def _bio_search(self, sector: Sector, max_per_keyword: int = 50) -> int:
        """通过 Bio 关键词搜索发现新企业"""
        added = 0
        for kw in sector.bio_keywords:
            if len(self._results) >= self.target:
                break
            logger.info(f"[Path B] Searching Bio keyword: '{kw}'")
            try:
                data = self.client.search_users(kw)
                users = data.get("users", [])
                logger.info(f"  → Got {len(users)} results")
                for u in users[:max_per_keyword]:
                    handle = u.get("userName") or u.get("screen_name") or ""
                    if not handle or not self._is_new(handle):
                        continue
                    # 过滤：至少 500 粉丝，且不像个人账号
                    followers = u.get("followers_count", 0) or u.get("followersCount", 0) or 0
                    if followers < 500:
                        continue
                    # 用 Bio 判断是否是企业/项目账号
                    bio = u.get("description", "") or u.get("bio", "") or ""
                    name = u.get("name", "") or u.get("displayName", "") or ""
                    if self._looks_like_company(bio, name, sector):
                        c = Company(
                            name=name,
                            x_handle=handle,
                            description=bio[:120],
                            hq="",
                            sector=sector.id,
                            source="bio_search",
                        )
                        if self._add(c):
                            added += 1
                            logger.debug(f"  + @{handle} ({name}) — {bio[:60]}")
            except Exception as e:
                logger.error(f"  Bio search error for '{kw}': {e}")
        logger.info(f"[Path B] Added {added} companies via Bio search")
        return added

    def _looks_like_company(self, bio: str, name: str, sector: Sector) -> bool:
        """简单启发式判断是否是企业/项目账号（而非个人）"""
        bio_lower = bio.lower()
        name_lower = name.lower()
        text = f"{bio_lower} {name_lower}"

        # 企业信号词
        company_signals = [
            "official", "protocol", "platform", "network", "exchange",
            "finance", "capital", "labs", "inc", "ltd", "foundation",
            "dao", "defi", "dex", "wallet", "custody", "mining",
            "staking", "tokeniz", "payment", "compliance", "otc",
            "brokerage", "trading", "institutional", "enterprise",
            "infra", "infrastructure",
        ]
        # 个人信号词（排除）
        personal_signals = [
            "my opinion", "personal", "dad", "mom", "husband", "wife",
            "views are my own", "not financial advice",
            "crypto enthusiast", "degen", "nfa",
        ]

        has_company_signal = any(s in text for s in company_signals)
        has_personal_signal = any(s in text for s in personal_signals)

        # 还要匹配赛道关键词
        has_sector_signal = any(kw.lower() in text for kw in sector.bio_keywords[:3])

        return has_company_signal and not has_personal_signal and has_sector_signal

    # ──── Path C: Following 网络 ──────────────────────────

    def _following_expansion(self, sector: Sector, top_n_seeds: int = 5, max_followings: int = 200) -> int:
        """从种子企业的 following 列表中挖掘同赛道企业"""
        added = 0

        # 选前 N 个种子企业做扩展
        seeds_to_expand = [c for c in self._results if c.source == "seed"][:top_n_seeds]

        for seed in seeds_to_expand:
            if len(self._results) >= self.target:
                break
            logger.info(f"[Path C] Expanding from @{seed.x_handle} followings...")

            try:
                # 先获取 user_id
                user_info = self.client.get_user_info(seed.x_handle)
                user_data = user_info.get("data", user_info)
                user_id = str(user_data.get("id") or user_data.get("userId") or user_data.get("rest_id", ""))
                if not user_id:
                    logger.warning(f"  Could not get user_id for @{seed.x_handle}")
                    continue

                # 拉取 followings
                data = self.client.get_user_followings(user_id)
                followings = data.get("users", [])
                logger.info(f"  → Got {len(followings)} followings")

                for u in followings[:max_followings]:
                    handle = u.get("userName") or u.get("screen_name") or ""
                    if not handle or not self._is_new(handle):
                        continue
                    followers = u.get("followers_count", 0) or u.get("followersCount", 0) or 0
                    if followers < 500:
                        continue
                    bio = u.get("description", "") or u.get("bio", "") or ""
                    name = u.get("name", "") or u.get("displayName", "") or ""
                    if self._looks_like_company(bio, name, sector):
                        c = Company(
                            name=name,
                            x_handle=handle,
                            description=bio[:120],
                            hq="",
                            sector=sector.id,
                            source="following_network",
                        )
                        if self._add(c):
                            added += 1
                            logger.debug(f"  + @{handle} ({name}) from @{seed.x_handle}'s following")
            except Exception as e:
                logger.error(f"  Following expansion error for @{seed.x_handle}: {e}")

        logger.info(f"[Path C] Added {added} companies via following network")
        return added

    # ──── Main Pipeline ───────────────────────────────────

    def run(self, sector_id: str) -> List[Company]:
        """
        执行完整的赛道企业发现 Pipeline

        Args:
            sector_id: 赛道标识，如 "cex", "rwa", "mining" 等

        Returns:
            List[Company]: 发现的企业列表（最多 target 家）
        """
        sector = get_sector(sector_id)
        logger.info(f"{'='*60}")
        logger.info(f"Starting sector pipeline: {sector.name_en} ({sector.name_cn})")
        logger.info(f"Target: {self.target} companies")
        logger.info(f"{'='*60}")

        # Path A: 加载种子
        self._load_seeds(sector)
        logger.info(f"Progress: {len(self._results)}/{self.target}")

        if len(self._results) < self.target:
            # Path B: Bio 搜索
            self._bio_search(sector)
            logger.info(f"Progress: {len(self._results)}/{self.target}")

        if len(self._results) < self.target:
            # Path C: Following 网络
            self._following_expansion(sector)
            logger.info(f"Progress: {len(self._results)}/{self.target}")

        # 截断到 target
        results = self._results[:self.target]
        logger.info(f"{'='*60}")
        logger.info(f"Pipeline complete: found {len(results)} companies")
        logger.info(f"  Seeds: {sum(1 for c in results if c.source == 'seed')}")
        logger.info(f"  Bio search: {sum(1 for c in results if c.source == 'bio_search')}")
        logger.info(f"  Following: {sum(1 for c in results if c.source == 'following_network')}")
        logger.info(f"{'='*60}")

        return results

    def run_all_sectors(self) -> Dict[str, List[Company]]:
        """对所有 10 个赛道执行 Pipeline"""
        all_results = {}
        for sector_id in SECTORS:
            # 每个赛道独立运行，重置状态
            self._seen_handles = set()
            self._results = []
            companies = self.run(sector_id)
            all_results[sector_id] = companies
        return all_results


def save_results_json(results: List[Company], filepath: str):
    """将结果保存为 JSON"""
    data = []
    for c in results:
        data.append({
            "name": c.name,
            "x_handle": c.x_handle,
            "x_url": f"https://x.com/{c.x_handle}",
            "description": c.description,
            "hq": c.hq,
            "sector": c.sector,
            "source": c.source,
        })
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"Results saved to {filepath}")
