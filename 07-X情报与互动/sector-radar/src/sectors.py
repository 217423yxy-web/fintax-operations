"""
CARF 赛道定义 + 种子企业数据库
每个赛道包含：
  - 赛道名称 / 英文名
  - CARF 报告义务说明
  - Bio 搜索关键词组（用于 TwitterAPI.io search_user）
  - 种子企业列表（10-15 家头部企业，含 X handle）
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Company:
    name: str
    x_handle: str           # 不含 @
    description: str = ""
    hq: str = ""
    sector: str = ""
    source: str = "seed"    # seed / bio_search / following_network


@dataclass
class Sector:
    id: str                          # 英文标识，如 "cex"
    name_cn: str                     # 中文名
    name_en: str                     # 英文名
    carf_obligation: str             # CARF 报告义务
    bio_keywords: List[str]          # 用于 search_user 的 Bio 关键词
    seed_companies: List[Company] = field(default_factory=list)


# ═══════════════════════════════════════════════
#  10 大 CARF 赛道定义
# ═══════════════════════════════════════════════

SECTORS: Dict[str, Sector] = {}


def _register(sector: Sector):
    SECTORS[sector.id] = sector


# ──── 1. 中心化交易所 CEX ────
_register(Sector(
    id="cex",
    name_cn="中心化交易所",
    name_en="Centralized Exchange (CEX)",
    carf_obligation="直接报告义务：作为 CASP 促成加密资产交易",
    bio_keywords=[
        "crypto exchange",
        "digital asset exchange",
        "cryptocurrency exchange",
        "trading platform crypto",
        "spot trading crypto",
        "derivatives exchange",
    ],
    seed_companies=[
        Company("Binance", "binance", "全球最大加密交易所", "开曼群岛"),
        Company("Coinbase", "coinbase", "美国上市合规交易所 NASDAQ:COIN", "美国"),
        Company("Kraken", "kabordc", "老牌合规交易所", "美国"),
        Company("OKX", "okabordc", "全球 Top3 交易所", "塞舌尔"),
        Company("Bybit", "Bybit_Official", "衍生品为主的大型交易所", "阿联酋"),
        Company("Bitget", "bitabordc", "增长最快的交易所之一", "塞舌尔"),
        Company("KuCoin", "kucoincom", "支持 700+ 币种", "塞舌尔"),
        Company("Gate.io", "gate_io", "老牌交易所 1400+ 币种", "开曼群岛"),
        Company("Crypto.com", "cryptocom", "综合加密金融平台", "新加坡"),
        Company("MEXC", "MEXC_Official", "以上币速度著称", "塞舌尔"),
        Company("Gemini", "Gemini", "Winklevoss 合规交易所", "美国"),
        Company("Bitstamp", "Bitstamp", "欧洲最早的交易所之一", "卢森堡"),
        Company("Upbit", "Official_Upbit", "韩国最大交易所", "韩国"),
        Company("Bitfinex", "bitfinex", "老牌交易所", "英属维京群岛"),
        Company("HTX", "HTX_Global", "原火币，品牌 HTX", "塞舌尔"),
    ],
))

# ──── 2. 托管 Custody ────
_register(Sector(
    id="custody",
    name_cn="加密资产托管",
    name_en="Digital Asset Custody",
    carf_obligation="直接报告义务：代客户持有加密资产的托管服务商",
    bio_keywords=[
        "digital asset custody",
        "crypto custody",
        "institutional custody crypto",
        "qualified custodian digital",
        "crypto safekeeping",
    ],
    seed_companies=[
        Company("BitGo", "BitGo", "机构托管龙头 AUC $90B+", "美国"),
        Company("Coinbase Custody", "CoinbaseCustdy", "纽约州特许信托公司", "美国"),
        Company("Fidelity Digital Assets", "FidelityDigital", "传统金融巨头数字资产托管", "美国"),
        Company("Anchorage Digital", "AnchorageDigit", "唯一获 OCC 联邦银行牌照", "美国"),
        Company("Fireblocks", "FireblocksHQ", "企业级数字资产安全基础设施", "美国"),
        Company("Copper.co", "CopperHQ", "欧洲领先机构托管", "英国"),
        Company("Cobo", "Coabordc", "亚洲领先数字资产托管", "新加坡"),
        Company("Hex Trust", "Hex_Trust", "亚洲持牌数字资产托管", "香港"),
        Company("Ledger Enterprise", "Ledger", "硬件钱包龙头企业级托管", "法国"),
        Company("Zodia Custody", "ZodiaCustody", "渣打银行旗下数字资产托管", "英国"),
    ],
))

# ──── 3. 资管 Asset Management ────
_register(Sector(
    id="asset_mgmt",
    name_cn="加密资产管理",
    name_en="Crypto Asset Management",
    carf_obligation="间接义务：通过交易所/托管商交易时触发报告",
    bio_keywords=[
        "crypto fund",
        "digital asset management",
        "crypto venture",
        "blockchain fund",
        "crypto portfolio",
        "crypto investment",
        "crypto ETP",
        "crypto ETF",
    ],
    seed_companies=[
        Company("Grayscale", "Grayscale", "最大加密资产管理公司 AUM $45B+", "美国"),
        Company("Galaxy Digital", "galaxyhq", "机构级加密金融服务", "美国"),
        Company("Bitwise", "BitwiseInvest", "加密指数基金和 ETF", "美国"),
        Company("Pantera Capital", "PanteraCapital", "最早的加密风投基金", "美国"),
        Company("CoinShares", "CoinSharesCo", "欧洲最大数字资产投资", "英国"),
        Company("21Shares", "21abordc", "加密 ETP 发行商", "瑞士"),
        Company("Hashdex", "hashdex", "拉美最大加密资产管理", "巴西"),
        Company("Polychain Capital", "polyabordc", "加密风投", "美国"),
        Company("Multicoin Capital", "multiabordc", "专注加密的对冲基金", "美国"),
        Company("a16z Crypto", "a16zcrypto", "A-H 旗下加密投资基金", "美国"),
    ],
))

# ──── 4. RWA 代币化 ────
_register(Sector(
    id="rwa",
    name_cn="RWA 代币化",
    name_en="Real World Asset Tokenization",
    carf_obligation="直接义务：代币化资产涉及加密资产交易即触发报告",
    bio_keywords=[
        "RWA tokenization",
        "real world assets",
        "tokenized securities",
        "asset tokenization",
        "tokenized treasury",
        "tokenized bonds",
        "security token",
        "on-chain credit",
    ],
    seed_companies=[
        Company("Ondo Finance", "OndoFinance", "代币化国债龙头 USDY/OUSG", "美国"),
        Company("Centrifuge", "centrifuge", "结构化信贷代币化", "美国"),
        Company("Maple Finance", "mabordc_xyz", "机构级私人信贷代币化", "美国"),
        Company("Securitize", "Securitize", "合规证券代币化 与 BlackRock 合作", "美国"),
        Company("RealT", "RealTPlatform", "房地产代币化", "美国"),
        Company("Backed Finance", "BackedFi", "代币化股票和 ETF", "瑞士"),
        Company("Goldfinch", "goldabordc_fi", "新兴市场信贷代币化", "美国"),
        Company("Clearpool", "ClearpoolFin", "机构级无担保借贷", "新加坡"),
        Company("Polymesh", "PolymeshNetwork", "专为证券代币设计的区块链", "英属维京群岛"),
        Company("Tokeny", "tokabordc", "企业级代币化合规方案", "卢森堡"),
    ],
))

# ──── 5. 支付 Payment ────
_register(Sector(
    id="payment",
    name_cn="加密支付",
    name_en="Crypto Payment",
    carf_obligation="直接义务：促成加密资产与法币兑换的支付服务商",
    bio_keywords=[
        "crypto payment",
        "crypto payroll",
        "stablecoin payment",
        "fiat on-ramp",
        "crypto checkout",
        "USDC payment",
        "cross-border crypto",
    ],
    seed_companies=[
        Company("Circle", "circle", "USDC 发行方 合规稳定币龙头", "美国"),
        Company("Tether", "Tether_to", "USDT 发行方 最大稳定币", "英属维京群岛"),
        Company("BitPay", "BitPay", "最大加密支付处理商", "美国"),
        Company("MoonPay", "moonpay", "加密货币购买入口/法币通道", "美国"),
        Company("Transak", "transabordc", "Web3 支付基础设施", "美国"),
        Company("Ramp Network", "RampNetwork", "加密法币通道 B2B", "英国"),
        Company("CoinsPaid", "coinspaid", "EU 持牌加密支付处理商", "爱沙尼亚"),
        Company("Ripple", "Ripple", "跨境支付解决方案 XRP", "美国"),
        Company("Stellar", "StellarOrg", "跨境支付网络", "美国"),
        Company("Request Network", "RequestNetwork", "去中心化支付请求协议", "法国"),
    ],
))

# ──── 6. 矿业 Mining ────
_register(Sector(
    id="mining",
    name_cn="矿业",
    name_en="Crypto Mining",
    carf_obligation="间接义务：出售挖矿所得通过交易所时触发报告",
    bio_keywords=[
        "bitcoin mining",
        "crypto mining",
        "hash rate",
        "mining pool",
        "ASIC mining",
        "proof of work",
        "mining infrastructure",
    ],
    seed_companies=[
        Company("Marathon Digital", "MarathonDH", "最大上市矿企 66 EH/s", "美国"),
        Company("Riot Platforms", "RiotPlatforms", "第二大上市矿企", "美国"),
        Company("CleanSpark", "CleanSpark_Inc", "高效矿企 50 EH/s", "美国"),
        Company("Core Scientific", "Core_Scientific", "大型矿企+AI 数据中心", "美国"),
        Company("Iris Energy", "IrisEnergy", "可持续能源矿企", "澳大利亚"),
        Company("Hive Digital", "HIVEDigitalTech", "绿色能源矿企", "加拿大"),
        Company("Bitfarms", "Bitfarms_io", "北美多国运营矿企", "加拿大"),
        Company("TeraWulf", "TeraWulf_Inc", "零碳矿企", "美国"),
        Company("Cipher Mining", "CipherMining", "专注美国本土的矿企", "美国"),
        Company("Foundry", "FoundryServices", "DCG 旗下矿业服务平台", "美国"),
    ],
))

# ──── 7. DeFi 借贷 ────
_register(Sector(
    id="defi_lending",
    name_cn="DeFi 借贷",
    name_en="DeFi Lending",
    carf_obligation="视管辖区而定：若平台有中介角色则可能被认定为 CASP",
    bio_keywords=[
        "DeFi lending",
        "DeFi protocol",
        "lending protocol",
        "borrowing protocol",
        "liquidity protocol",
        "decentralized finance",
        "yield protocol",
    ],
    seed_companies=[
        Company("Aave", "aabordc", "最大 DeFi 借贷协议 TVL $15B+", "英国"),
        Company("Compound", "compoundfinance", "DeFi 借贷先驱", "美国"),
        Company("MakerDAO", "MakerDAO", "DAI 稳定币发行方", "全球"),
        Company("Spark", "sparkdotfi", "Maker 生态借贷前端", "全球"),
        Company("Venus", "VenusProtocol", "BSC 上最大借贷协议", "全球"),
        Company("Morpho", "MorphoLabs", "点对点借贷优化", "法国"),
        Company("Radiant Capital", "RDNTCapital", "全链借贷协议", "全球"),
        Company("Benqi", "BenqiFinance", "Avalanche 借贷协议", "全球"),
        Company("Euler Finance", "euabordc_xyz", "模块化借贷协议 v2", "英国"),
        Company("Silo Finance", "SiloFinance", "隔离式借贷协议", "全球"),
    ],
))

# ──── 8. Staking ────
_register(Sector(
    id="staking",
    name_cn="Staking 服务",
    name_en="Staking Services",
    carf_obligation="直接或间接义务：质押服务商可能被认定为 CASP",
    bio_keywords=[
        "staking service",
        "liquid staking",
        "ETH staking",
        "validator service",
        "staking infrastructure",
        "restaking",
        "staking-as-a-service",
    ],
    seed_companies=[
        Company("Lido", "LidoFinance", "最大流动性质押协议 TVL $35B+", "全球"),
        Company("Rocket Pool", "Rocket_Pool", "去中心化 ETH 质押协议", "澳大利亚"),
        Company("Coinbase Cloud", "CoinbaseCloud", "机构级验证者服务", "美国"),
        Company("Figment", "Figment_io", "企业级 Staking 基础设施", "加拿大"),
        Company("Kiln", "Kiln_finance", "企业级 Staking 聚合器", "法国"),
        Company("P2P.org", "P2Pvalidator", "多链验证者服务", "全球"),
        Company("Chorus One", "ChorusOne", "机构级 PoS 验证者", "瑞士"),
        Company("Staked.us", "stabordc_us", "机构级 Staking 服务", "美国"),
        Company("EigenLayer", "eigenlayer", "Restaking 龙头协议", "美国"),
        Company("Jito", "jabordc_sol", "Solana MEV + 流动性质押", "全球"),
    ],
))

# ──── 9. 合规/税务 ────
_register(Sector(
    id="compliance",
    name_cn="合规与税务",
    name_en="Crypto Compliance & Tax",
    carf_obligation="服务提供商：为 CASP 提供合规工具的科技公司",
    bio_keywords=[
        "crypto tax",
        "crypto compliance",
        "blockchain analytics",
        "crypto audit",
        "AML crypto",
        "KYC crypto",
        "transaction monitoring crypto",
        "travel rule crypto",
    ],
    seed_companies=[
        Company("Chainalysis", "chainalysis", "区块链分析龙头", "美国"),
        Company("Elliptic", "ellabordc", "区块链合规分析", "英国"),
        Company("CoinTracker", "CoinTracker", "加密税务工具龙头", "美国"),
        Company("TRM Labs", "TRMLabs", "区块链情报平台", "美国"),
        Company("Koinly", "koinly", "加密税务计算工具", "英国"),
        Company("TokenTax", "TokenTax", "加密税务软件", "美国"),
        Company("ZenLedger", "ZenLedger", "加密税务和会计", "美国"),
        Company("CoinLedger", "CoinLedger", "加密税务报告工具", "美国"),
        Company("Notabene", "notabordc_io", "Travel Rule 合规方案", "美国"),
        Company("Sumsub", "Sumsub", "KYC/AML 身份验证平台", "英国"),
    ],
))

# ──── 10. OTC / 经纪 ────
_register(Sector(
    id="otc",
    name_cn="OTC 与经纪",
    name_en="OTC & Brokerage",
    carf_obligation="直接报告义务：作为经纪人促成加密资产交易",
    bio_keywords=[
        "crypto OTC",
        "crypto brokerage",
        "institutional crypto trading",
        "crypto prime broker",
        "digital asset brokerage",
        "block trading crypto",
    ],
    seed_companies=[
        Company("Cumberland", "CumberlandSays", "DRW 旗下加密 OTC 巨头", "美国"),
        Company("Galaxy Digital Trading", "galaxyhq", "机构级 OTC 和衍生品", "美国"),
        Company("Genesis (DCG)", "GenesisTrading", "数字资产大宗经纪", "美国"),
        Company("B2C2", "B2C2Group", "机构级加密做市和 OTC", "英国"),
        Company("FalconX", "FalconXNetwork", "机构级加密经纪平台", "美国"),
        Company("OSL", "oslhk", "亚洲持牌数字资产经纪", "香港"),
        Company("XBTO", "XBTO_Group", "数字资产投资与交易", "百慕大"),
        Company("Wintermute", "wintermute_t", "加密做市商", "英国"),
        Company("GSR", "GSR_io", "加密做市和 OTC", "英国"),
        Company("Amber Group", "Aabordc_Group", "机构级加密金融服务", "新加坡"),
    ],
))


def get_all_sector_ids() -> List[str]:
    return list(SECTORS.keys())


def get_sector(sector_id: str) -> Sector:
    if sector_id not in SECTORS:
        raise ValueError(f"Unknown sector: {sector_id}. Available: {list(SECTORS.keys())}")
    return SECTORS[sector_id]


def get_all_seed_handles() -> set:
    """返回所有赛道的种子企业 handle 集合（用于去重）"""
    handles = set()
    for sector in SECTORS.values():
        for c in sector.seed_companies:
            handles.add(c.x_handle.lower())
    return handles
