#!/usr/bin/env python3
"""
Sector Radar — 赛道企业发现工具
用法:
  # 单赛道模式（发现某一赛道的 100 家企业）
  python run.py --sector cex

  # 全赛道模式（10 个赛道各 100 家）
  python run.py --all

  # 仅输出种子企业（不调用 API，用于验证种子数据）
  python run.py --sector rwa --seeds-only

  # 自定义目标数量
  python run.py --sector mining --target 50

可用赛道 ID:
  cex         中心化交易所
  custody     加密资产托管
  asset_mgmt  加密资产管理
  rwa         RWA 代币化
  payment     加密支付
  mining      矿业
  defi_lending DeFi 借贷
  staking     Staking 服务
  compliance  合规与税务
  otc         OTC 与经纪
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# 将项目根目录加入 path
sys.path.insert(0, str(Path(__file__).parent))

from src.sectors import get_all_sector_ids, get_sector, SECTORS, Company
from src.pipeline import SectorPipeline, save_results_json
from src.excel_export import export_sector_excel, export_all_sectors_excel


def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def run_seeds_only(sector_id: str, output_dir: str) -> str:
    """仅导出种子企业（不调用任何 API）"""
    sector = get_sector(sector_id)
    companies = []
    for c in sector.seed_companies:
        c.sector = sector_id
        c.source = "seed"
        companies.append(c)

    date_str = datetime.now().strftime("%Y%m%d")
    filepath = os.path.join(output_dir, f"seeds_{sector_id}_{date_str}.xlsx")
    export_sector_excel(companies, sector_id, filepath)
    return filepath


def run_single_sector(sector_id: str, target: int, output_dir: str, api_key: str) -> str:
    """运行单赛道 Pipeline"""
    from src.twitter_client import TwitterAPIClient
    client = TwitterAPIClient(api_key=api_key)
    pipeline = SectorPipeline(client=client, target=target)
    companies = pipeline.run(sector_id)

    date_str = datetime.now().strftime("%Y%m%d")
    # JSON
    json_path = os.path.join(output_dir, f"sector_{sector_id}_{date_str}.json")
    save_results_json(companies, json_path)
    # Excel
    xlsx_path = os.path.join(output_dir, f"sector_{sector_id}_{date_str}.xlsx")
    export_sector_excel(companies, sector_id, xlsx_path)
    return xlsx_path


def run_all_sectors(target: int, output_dir: str, api_key: str) -> str:
    """运行全赛道 Pipeline"""
    from src.twitter_client import TwitterAPIClient
    client = TwitterAPIClient(api_key=api_key)

    all_results = {}
    for sector_id in get_all_sector_ids():
        pipeline = SectorPipeline(client=client, target=target)
        companies = pipeline.run(sector_id)
        all_results[sector_id] = companies

    date_str = datetime.now().strftime("%Y%m%d")
    xlsx_path = os.path.join(output_dir, f"all_sectors_{date_str}.xlsx")
    export_all_sectors_excel(all_results, xlsx_path)
    return xlsx_path


def main():
    parser = argparse.ArgumentParser(
        description="Sector Radar — CARF 赛道企业 X 账号发现工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--sector", type=str, help="赛道 ID (如 cex, rwa, mining)")
    parser.add_argument("--all", action="store_true", help="运行全部 10 个赛道")
    parser.add_argument("--seeds-only", action="store_true", help="仅输出种子企业（不调 API）")
    parser.add_argument("--target", type=int, default=100, help="每赛道目标企业数 (默认 100)")
    parser.add_argument("--output-dir", type=str, default="./output", help="输出目录")
    parser.add_argument("--api-key", type=str, default="", help="TwitterAPI.io API Key")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细日志")
    parser.add_argument("--list-sectors", action="store_true", help="列出所有可用赛道")

    args = parser.parse_args()
    setup_logging(args.verbose)

    if args.list_sectors:
        print("\n可用赛道:")
        print(f"{'ID':<15} {'中文名':<15} {'英文名':<35} {'种子数'}")
        print("-" * 80)
        for sid, sector in SECTORS.items():
            print(f"{sid:<15} {sector.name_cn:<15} {sector.name_en:<35} {len(sector.seed_companies)}")
        return

    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)

    api_key = args.api_key or os.environ.get("TWITTER_API_KEY", "")

    if args.seeds_only:
        if not args.sector:
            print("--seeds-only 需要指定 --sector")
            sys.exit(1)
        path = run_seeds_only(args.sector, args.output_dir)
        print(f"\n✅ 种子企业已导出: {path}")
        return

    if not api_key:
        print("⚠️  未提供 TwitterAPI.io API Key!")
        print("   设置环境变量: export TWITTER_API_KEY=your_key")
        print("   或使用参数:   --api-key your_key")
        print("\n   可以先用 --seeds-only 模式查看种子企业。")
        sys.exit(1)

    if args.all:
        path = run_all_sectors(args.target, args.output_dir, api_key)
        print(f"\n✅ 全赛道结果已导出: {path}")
    elif args.sector:
        path = run_single_sector(args.sector, args.target, args.output_dir, api_key)
        print(f"\n✅ 赛道结果已导出: {path}")
    else:
        print("请指定 --sector <赛道ID> 或 --all")
        print("使用 --list-sectors 查看可用赛道")
        sys.exit(1)


if __name__ == "__main__":
    main()
