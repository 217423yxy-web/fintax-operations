#!/usr/bin/env python3
"""
搜索非友商推文并匹配回帖
"""
import json
import time
import urllib.request
import urllib.parse

API_KEY = "new1_ad975caf0bde4ecb860267533dcfb662"
BASE_URL = "https://api.twitterapi.io/twitter/tweet/advanced_search"

# 友商账号（小写）
COMPETITOR_ACCOUNTS = {
    "coinledger", "taxbit", "crystalplatform", "merklescience", "cointracker",
    "sumsub", "complyadavantage", "complyadantage", "complyadv", "complyadvantage",
    "onfido", "chainalysis", "trmlabs", "koinly", "tokentax", "zenledger",
    "ledgible", "bitwaveinc", "lukkaofficial", "scorechain"
}

# 130条回帖数据（索引0-129）
REPLIES = [
    # 0 场景落地型 - Gas费/手续费计入成本基础
    ("Don't just track purchase price — gas fees and exchange fees add to cost basis too. Buy ETH at $3,000 + $15 gas? Basis is $3,015. Every missed fee is overpaid tax. Track them all from now.", "场景落地型"),
    # 1 规则解读型 - 手续费加入成本基础举例
    ("Fees work both directions under IRS rules: purchase fees raise your basis (lower gains), sale fees reduce proceeds (lower gains again). The $10k BTC + $50 fee example is textbook cost basis adjustment — not optional.", "规则解读型"),
    # 2 反直觉观点型 - 1099-DA不用附在税表上
    ("1099-DA looks authoritative but it's informational only — attaching it to your return is wrong. Real numbers go on Form 8949. Cross-platform transfers mean 1099-DA basis is almost certainly incorrect.", "反直觉观点型"),
    # 3 反直觉观点型 - 持有转账不用回答数字资产问题
    ("Most people assume any crypto = check 'Yes' on Form 1040. Wrong. IRS explicitly allows 'No' if you only held, transferred between your own wallets, or bought with fiat. Taxable disposals are the line.", "反直觉观点型"),
    # 4 规则解读型 - 1099-DA包含哪些交易类型
    ("Paying gas to transfer tokens is itself a taxable disposal at FMV — IRS treats it as a partial sale. Small amounts, but Form 8949 requires every one. Network fee disposals catch most people off guard.", "规则解读型"),
    # 5 反直觉观点型 - 16种加密资产被列为商品
    ("Commodity classification looked like a win — but commodity ≠ lower taxes. Under FIT21, CFTC jurisdiction applies. 'Digital commodity' is a legal category, not a tax break. Check which rules govern your exposure.", "反直觉观点型"),
    # 6 规则解读型 - 稳定币让Fintech获取收益
    ("Yield-bearing stablecoins shift the tax burden too. When fintechs earn reserve yield, that's ordinary income. Users holding yield-bearing tokens trigger their own income event at receipt — not at sale.", "规则解读型"),
    # 7 反直觉观点型 - 1099-DA缺成本基础不必报0
    ("Missing basis on 1099-DA doesn't mean you report $0 cost — that creates phantom gains and massive overtaxation. Form 8949 lets you enter actual basis with documentation. That's exactly what the form is for.", "反直觉观点型"),
    # 8 场景落地型 - 等1099-DA再申报税表
    ("If your 1099-DA proceeds differ from your own records, file Form 8949 with corrected numbers and explain the gap. IRS matching triggers on unexplained discrepancies — reconcile before filing, not after a notice.", "场景落地型"),
    # 9 场景落地型 - 加密亏损可抵扣3000美元普通收入
    ("Crypto losses offset W-2 income directly: up to $3k/year, unlimited carryforward. $20k unrealized loss? Harvest now — $3k offset this year, $17k forward. No wash-sale rule to block it. Act before year-end.", "场景落地型"),
    # 10 规则解读型 - 质押奖励等算普通收入
    ("IRS Rev. Rul. 2023-14 settled it: staking rewards are ordinary income at FMV at receipt — not at sale. Airdrops and interest follow the same rule. The later sale is a separate capital gains event.", "规则解读型"),
    # 11 反直觉观点型 - 跨钱包转入导致1099-DA不完整
    ("1099-DA only reflects what your current exchange sees. Crypto from another platform or self-custody wallet leaves a cost basis gap your exchange can't fill. You must reconstruct it — or pay tax on phantom gains.", "反直觉观点型"),
    # 12 规则解读型 - USDC做DeFi抵押
    ("USDC vs USDT isn't just liquidity — it's compliance structure. USDC's reserve transparency shapes issuer reporting obligations under GENIUS Act. For tax purposes, reserve composition affects regulatory treatment.", "规则解读型"),
    # 13 反直觉观点型 - 稳定币供应涨但使用量下降
    ("Supply growth without matching volume is misleading. Under CARF, tax authorities care about actual transaction data, not issuance. High supply, low usage means far fewer real taxable events than headlines suggest.", "反直觉观点型"),
    # 14 规则解读型 - 稳定币是什么及使用方式
    ("Stablecoins look neutral but use determines tax treatment: spending USDT is a disposal at FMV. Hold a yield-bearing stablecoin? That yield is ordinary income at receipt, not at redemption.", "规则解读型"),
    # 22 场景落地型 - GENIUS法案生效
    ("GENIUS Act is live. Stablecoin issuers need: licensed status, 1:1 reserve backing, AML/CFT controls, and transaction reporting. Audit your current setup against these four requirements now — not after enforcement.", "场景落地型"),
    # 23 规则解读型 - 每周监管动态
    ("Regulatory velocity isn't slowing. CARF, DAC8, GENIUS Act, FIT21 all have 2026 implementation timelines. Any crypto business operating cross-border now has simultaneous reporting obligations across jurisdictions.", "规则解读型"),
    # 34 场景落地型 - CARF和DAC8报税合规
    ("CARF goes live in 2026. For crypto businesses: step 1 is identifying reportable transactions, step 2 is building the data pipeline to your local tax authority. Webinars help — the deadline doesn't move.", "场景落地型"),
    # 49 场景落地型 - CARF和DAC8网络研讨会
    ("CARF is live in 2026. Before the webinar: confirm which transactions are cross-border, identify jurisdictions you operate in, and check if your data architecture produces the required reports. Deadline doesn't move.", "场景落地型"),
    # 52 场景落地型 - CARF和DAC8合规网络研讨会
    ("CARF requires automatic exchange of crypto user data between OECD authorities from 2026. Any crypto business with users in multiple countries must know which transactions are reportable. Act before enforcement.", "场景落地型"),
    # 66 规则解读型 - CARF和DAC8重塑加密税务透明度
    ("CARF and DAC8 are distinct instruments: CARF is the OECD global framework; DAC8 is EU law implementing CARF with binding enforcement. Both are live in 2026. Operating in Europe means compliance with both.", "规则解读型"),
    # 72 场景落地型 - TaxBit参与MiCA到DAC8欧洲过渡
    ("MiCA and DAC8 have overlapping but distinct scopes: MiCA covers issuance regulation; DAC8 covers tax reporting. EU businesses need both. DAC8 reporting infrastructure must be live by January 2026.", "场景落地型"),
    # 94 场景落地型 - 调查3000名加密投资者税务准备
    ("The survey gap is actionable: export exchange transaction histories, add DeFi wallet records, identify missing basis. The 65% who haven't fixed their records have a limited window before CARF cross-referencing begins.", "场景落地型"),
    # 99 场景落地型 - TaxBit节日祝福展望2026
    ("2026 compliance calendar: CARF goes live, GENIUS Act enforcement begins, per-wallet IRS rules fully in effect. Year-end loss harvesting and basis optimization are still actionable now — don't wait for Q1 filing pressure.", "场景落地型"),
    # 128 场景落地型 - TaxBit与BCB合作支持CARF和DAC8合规
    ("CARF requires automated data pipelines from transaction systems to tax authorities. Manual reporting at institutional scale doesn't work — compliance infrastructure must be built before enforcement begins, not after.", "场景落地型"),
]

# 15条搜索查询
SEARCH_QUERIES = [
    ("1099-DA Form 8949 crypto cost basis", [2, 7, 8, 11]),
    ("crypto cost basis gas fees IRS", [0, 1, 4]),
    ("staking rewards ordinary income IRS tax", [10]),
    ("crypto tax loss harvesting W2 income", [9]),
    ("CARF DAC8 crypto reporting 2026", [34, 49, 66]),
    ("GENIUS Act stablecoin compliance AML", [22, 12]),
    ("FIT21 digital commodity classification tax", [5]),
    ("per-wallet cost basis IRS 2025 tracking", [0, 1]),
    ("stablecoin payments tax disposal FMV", [14, 6]),
    ("crypto losses offset ordinary income wash sale", [9]),
    ("crypto mining income tax deductions depreciation", [15, 91, 93] if False else []),
    ("DeFi swap taxable event capital gains IRS", [4, 48]),
    ("tokenized assets CARF reporting cross-border", [17, 18, 25]),
    ("1099-DA missing cost basis phantom gains", [7, 11]),
    ("crypto ETF 1099-B tax treatment vs direct", [79, 100]),
]

# 完整REPLIES列表（从文件中提取的130条）
ALL_REPLIES = [
    ("Don't just track purchase price — gas fees and exchange fees add to cost basis too. Buy ETH at $3,000 + $15 gas? Basis is $3,015. Every missed fee is overpaid tax. Track them all from now.", "场景落地型"),
    ("Fees work both directions under IRS rules: purchase fees raise your basis (lower gains), sale fees reduce proceeds (lower gains again). The $10k BTC + $50 fee example is textbook cost basis adjustment — not optional.", "规则解读型"),
    ("1099-DA looks authoritative but it's informational only — attaching it to your return is wrong. Real numbers go on Form 8949. Cross-platform transfers mean 1099-DA basis is almost certainly incorrect.", "反直觉观点型"),
    ("Most people assume any crypto = check 'Yes' on Form 1040. Wrong. IRS explicitly allows 'No' if you only held, transferred between your own wallets, or bought with fiat. Taxable disposals are the line.", "反直觉观点型"),
    ("Paying gas to transfer tokens is itself a taxable disposal at FMV — IRS treats it as a partial sale. Small amounts, but Form 8949 requires every one. Network fee disposals catch most people off guard.", "规则解读型"),
    ("Commodity classification looked like a win — but commodity ≠ lower taxes. Under FIT21, CFTC jurisdiction applies. 'Digital commodity' is a legal category, not a tax break. Check which rules govern your exposure.", "反直觉观点型"),
    ("Yield-bearing stablecoins shift the tax burden too. When fintechs earn reserve yield, that's ordinary income. Users holding yield-bearing tokens trigger their own income event at receipt — not at sale.", "规则解读型"),
    ("Missing basis on 1099-DA doesn't mean you report $0 cost — that creates phantom gains and massive overtaxation. Form 8949 lets you enter actual basis with documentation. That's exactly what the form is for.", "反直觉观点型"),
    ("If your 1099-DA proceeds differ from your own records, file Form 8949 with corrected numbers and explain the gap. IRS matching triggers on unexplained discrepancies — reconcile before filing, not after a notice.", "场景落地型"),
    ("Crypto losses offset W-2 income directly: up to $3k/year, unlimited carryforward. $20k unrealized loss? Harvest now — $3k offset this year, $17k forward. No wash-sale rule to block it. Act before year-end.", "场景落地型"),
    ("IRS Rev. Rul. 2023-14 settled it: staking rewards are ordinary income at FMV at receipt — not at sale. Airdrops and interest follow the same rule. The later sale is a separate capital gains event.", "规则解读型"),
    ("1099-DA only reflects what your current exchange sees. Crypto from another platform or self-custody wallet leaves a cost basis gap your exchange can't fill. You must reconstruct it — or pay tax on phantom gains.", "反直觉观点型"),
    ("USDC vs USDT isn't just liquidity — it's compliance structure. USDC's reserve transparency shapes issuer reporting obligations under GENIUS Act. For tax purposes, reserve composition affects regulatory treatment.", "规则解读型"),
    ("Supply growth without matching volume is misleading. Under CARF, tax authorities care about actual transaction data, not issuance. High supply, low usage means far fewer real taxable events than headlines suggest.", "反直觉观点型"),
    ("Stablecoins look neutral but use determines tax treatment: spending USDT is a disposal at FMV. Hold a yield-bearing stablecoin? That yield is ordinary income at receipt, not at redemption.", "规则解读型"),
    ("Miners pivoting to HPC need to reclassify now: mining income is ordinary income at FMV on receipt; HPC hosting is service revenue with different depreciation rules. Two revenue streams, two tax treatments.", "场景落地型"),
    ("On-chain finance scales — but compliance doesn't scale automatically. Every tokenized asset transfer across borders triggers CARF reporting. The infrastructure is ready; the compliance layer is still missing.", "反直觉观点型"),
    ("Tokenized assets bring efficiency but also CARF reporting obligations: brokers must report disposals to tax authorities in each holder's jurisdiction. The transparency cuts both ways — regulators see everything.", "规则解读型"),
    ("DTCC entering tokenization is a compliance signal too. Once tokenized securities settle through DTCC, CARF/DAC8 reporting applies to all participants — issuers, custodians, and brokers alike.", "规则解读型"),
    ("The 3-year amendment window is real: file Form 1040-X with corrected Form 8949 and document your basis adjustments. IRS cross-references original and amended returns — keep thorough records before amending.", "场景落地型"),
    ("1099-DA proceeds may differ from your records because exchanges use price oracle snapshots, not real-time FMV. Neither is automatically right. Form 8949 is where you assert the correct number with documentation.", "反直觉观点型"),
    ("Per-wallet tracking is mandatory from Jan 1, 2025 — IRS eliminated universal cost basis. Same token across multiple wallets can no longer be pooled. Organize your records by wallet address today.", "场景落地型"),
    ("GENIUS Act is live. Stablecoin issuers need: licensed status, 1:1 reserve backing, AML/CFT controls, and transaction reporting. Audit your current setup against these four requirements now — not after enforcement.", "场景落地型"),
    ("Regulatory velocity isn't slowing. CARF, DAC8, GENIUS Act, FIT21 all have 2026 implementation timelines. Any crypto business operating cross-border now has simultaneous reporting obligations across jurisdictions.", "规则解读型"),
    ("76% know their basis is wrong but only 35% fixed it — that gap isn't laziness, it's complexity. Cross-platform transfers break the cost basis chain. Knowing the problem doesn't help if the records don't exist.", "反直觉观点型"),
    ("Every institution exploring tokenization inherits a compliance problem: CARF reporting for cross-border tokenized asset holders isn't optional. Institutional adoption without compliance infrastructure is a liability.", "反直觉观点型"),
    ("New finance, old tax rules — tokenized securities still trigger capital gains on disposal, and yield triggers income tax at receipt. The token wrapper doesn't change the underlying tax treatment of the asset inside.", "反直觉观点型"),
    ("Washington is writing rules for tokenized assets. Core debate: existing securities tax law or new frameworks? Under current rules, capital gains treatment applies — that default won't change easily.", "规则解读型"),
    ("SAB 122 removed punitive capital treatment for bank-held stablecoins. Old rule: dollar-for-dollar capital against crypto liabilities. That's gone now. GENIUS Act AML reporting fills the oversight gap instead.", "规则解读型"),
    ("Traditional-digital convergence means traditional tax reporting extends into crypto. When tokenized assets settle through DTCC, the same broker reporting obligations that apply to equities will apply — CARF included.", "规则解读型"),
    ("The tax case for long-term holding is underrated: assets held over 12 months qualify for 0-20% long-term rates vs up to 37% short-term. Conviction holding has a real tax dividend — conviction alone doesn't.", "反直觉观点型"),
    ("Borrowing stablecoins against tokenized stocks looks tax-efficient — no disposal, no capital gains. But if collateral gets liquidated, that's a taxable sale at FMV. The structure defers tax; it doesn't eliminate it.", "规则解读型"),
    ("Before any 1099-DA webinar: export your full transaction history from every exchange and wallet, flag cross-platform transfers, and identify where basis is missing. Those gaps are what Form 8949 corrections address.", "场景落地型"),
    ("Borrowing against crypto triggers no tax — but if liquidated, that forced sale is a taxable disposal at FMV. The loan delays the tax bill on appreciation; it doesn't cancel it. Structure the collateral carefully.", "反直觉观点型"),
    ("CARF goes live in 2026. For crypto businesses: step 1 is identifying reportable transactions, step 2 is building the data pipeline to your local tax authority. Webinars help — the deadline doesn't move.", "场景落地型"),
    ("Cross-border trade in stablecoins creates layered tax exposure: VAT/GST on goods, FX gain/loss on the stablecoin payment, and CARF reporting for cross-border flows. Each transaction needs to be decomposed.", "规则解读型"),
    ("Crypto ETF options on commodity-based products introduce the 60/40 rule: 60% of gains taxed as long-term, 40% short-term — regardless of holding period. That's structurally lower than pure short-term equity options.", "规则解读型"),
    ("Tokenized stocks are a big opportunity — but they don't inherit traditional tax treatment. Cross-border holders face CARF obligations standard ETFs don't trigger. The wrapper creates new compliance obligations.", "反直觉观点型"),
    ("Franklin Templeton's tokenized ETF is a milestone — but under CARF, brokers must report every disposal to tax authorities in each holder's jurisdiction. Compliance infrastructure has to match the innovation speed.", "规则解读型"),
    ("RWA vault structures face a tax classification question: is yield ordinary income (like bond interest) or capital gain? The legal structure of the vault determines the answer — and the applicable tax rate.", "规则解读型"),
    ("60% B2B stablecoin growth means compliance must scale at the same pace. Under CARF, cross-border stablecoin payments are reportable from 2026. Businesses using stablecoins for international invoices need records now.", "场景落地型"),
    ("Moving from experimentation to production means compliance can't be deferred. Production-scale tokenized securities require CARF reporting by design — not as an add-on. Build it in or lose institutional mandates.", "规则解读型"),
    ("Cross-chain fragmentation is the compliance nightmare nobody discusses: tokenized securities spanning multiple chains means CARF reporting requires aggregated cross-chain data per holder. That's a hard technical problem.", "规则解读型"),
    ("Real-world digital asset use creates real tax obligations — and compliance infrastructure hasn't kept pace. Every cross-border payment, tokenized disposal, and staking reward is reportable. Scale exposes every gap.", "反直觉观点型"),
    ("Ripple's Australian AFSL means clients transact through a licensed provider. Australia's Travel Rule goes live March 2026 — all cross-border crypto transactions require originator and beneficiary data. Prepare now.", "场景落地型"),
    ("Blockchain settlement changes the rails, not the rules: Nasdaq blockchain settlement still triggers the same capital gains reporting as traditional settlement. The technology is new; the tax obligation is not.", "规则解读型"),
    ("$600 is an exchange's 1099-MISC reporting trigger — not your filing threshold. Every dollar of crypto interest, staking income, or yield is taxable regardless of whether you receive a form. Self-reporting is mandatory.", "反直觉观点型"),
    ("Per-wallet cost basis is mandatory from Jan 1, 2025. If you've been using universal HIFO across wallets, those selections are invalid for 2025 disposals. Audit your tracking method before your next sale.", "场景落地型"),
    ("PEPE → BONK without touching USD still triggers capital gains — IRS treats every crypto swap as a disposal at FMV. DeFi traders with 500 swaps/week have 500 taxable events. The dollar never needs to appear.", "反直觉观点型"),
    ("CARF is live in 2026. Before the webinar: confirm which transactions are cross-border, identify jurisdictions you operate in, and check if your data architecture produces the required reports. Deadline doesn't move.", "场景落地型"),
    ("If 75-95% of transfers are issuer operations, real user volume is a fraction of reported figures. Under CARF, authorities want user data — not issuance. Supply-side volume overstates the real compliance burden.", "反直觉观点型"),
    ("GENIUS Act covers the US; MiCA covers the EU. If you operate in both, you're managing dual-reporting complexity. Map your transaction flows to both frameworks before Q3 2026 — the implementation window is short.", "场景落地型"),
    ("CARF requires automatic exchange of crypto user data between OECD authorities from 2026. Any crypto business with users in multiple countries must know which transactions are reportable. Act before enforcement.", "场景落地型"),
    ("FIT21's digital commodity classification for BTC/ETH has a concrete implication: CFTC jurisdiction may trigger Section 1256 treatment for certain derivatives — the 60/40 split that lowers rates for institutional traders.", "规则解读型"),
    ("This week's market moves create discrete tax events for anyone who rebalanced. Record FMV of every swap, note holding periods, and flag positions crossing the 12-month threshold — long-term rates are meaningfully lower.", "场景落地型"),
    ("LatAm's $730B flows through divergent tax regimes: Brazil taxes gains above R$35k/month, Argentina has stablecoin-specific rules, Mexico applies ISR. Cross-border stablecoin flows are exactly what CARF captures.", "规则解读型"),
    ("Belief in crypto needs a compliance foundation. India's 30% flat gains tax + 1% TDS on every transaction is one of the world's strictest regimes. High conviction doesn't offset undisclosed gains — eventually.", "反直觉观点型"),
    ("2026's regulatory layer: FIT21 (commodity classification) + GENIUS Act (stablecoins) + CARF (cross-border reporting). Any institutional crypto strategy ignoring this trinity has an incomplete risk model.", "规则解读型"),
    ("150 operators confirm tokenization is infrastructure — but the compliance gap is real. CARF reporting for cross-border tokenized holders isn't built into most platforms yet. That's the institutional adoption bottleneck.", "规则解读型"),
    ("90% market share in tokenized stocks means Backed's compliance decisions set sector standards. Under CARF, every tokenized stock disposal is reportable for cross-border holders — concentration amplifies the obligation.", "反直觉观点型"),
    ("The most defensible tokenization use case: securities with built-in CARF reporting. Tokenized bonds and equities that auto-generate regulatory data are institutional-grade — not just regulated in name only.", "规则解读型"),
    ("DTCC's RWA milestone means traditional infrastructure is production-ready for tokenized assets. Once settled via DTCC, existing broker rules apply directly — CARF obligations become unavoidable for all intermediaries.", "规则解读型"),
    ("Pilots-to-production means compliance must scale too. Institutions entering production-scale tokenized securities need automated CARF reporting now — manual reconciliation breaks at institutional transaction volumes.", "场景落地型"),
    ("Businesses paying suppliers in stablecoins: record FMV at payment date, classify as FX or crypto disposal per your accounting framework, and track for CARF from 2026. Every cross-border stablecoin payment is a tax event.", "场景落地型"),
    ("FATF's lifecycle tracking maps directly to CARF reporting. Travel Rule data flows are the foundation for cross-border crypto tax reporting — the two frameworks are converging operationally. Align your systems.", "场景落地型"),
    ("For the CARF/DAC8 webinar: know your reportable transaction types, identify users' tax jurisdictions, and confirm your data architecture can produce required reports. CARF enforcement makes preparation non-optional.", "场景落地型"),
    ("CARF and DAC8 are distinct instruments: CARF is the OECD global framework; DAC8 is EU law implementing CARF with binding enforcement. Both are live in 2026. Operating in Europe means compliance with both.", "规则解读型"),
    ("Yield-bearing stablecoins democratize access — and democratize tax obligations. Yield is ordinary income at receipt regardless of where you hold it. Financial inclusion doesn't exempt from reporting requirements.", "反直觉观点型"),
    ("Stablecoin adoption in emerging markets intersects with divergent local rules: some jurisdictions classify holdings as foreign currency; others as property. The tax treatment varies significantly by jurisdiction.", "规则解读型"),
    ("Wrapper-based tokenization dominates — but the wrapper creates a tax classification question. Does the wrapper token constitute the underlying asset? The answer affects cost basis, holding period, and applicable rates.", "规则解读型"),
    ("Smart contracts don't automate away tax obligations. IRS position: automated disposals are still disposals. Reporting sits with the asset holder — regardless of whether the trigger was human or code.", "规则解读型"),
    ("Speed and neutrality sound like technical goals — but institutional trust depends on compliance certainty. DTCC's value proposition only transfers to tokenized assets if CARF/DAC8 reporting is built in from day one.", "反直觉观点型"),
    ("MiCA and DAC8 have overlapping but distinct scopes: MiCA covers issuance regulation; DAC8 covers tax reporting. EU businesses need both. DAC8 reporting infrastructure must be live by January 2026.", "场景落地型"),
    ("Tokenized Treasuries have a specific tax wrinkle: US Treasury interest is exempt from state taxes — but that exemption applies to the underlying bonds, not necessarily to all wrapper token structures. Legal form matters.", "规则解读型"),
    ("NYSE-listed tokenized securities bring full US securities law: capital gains reporting, 1099-B issuance, and CARF cross-border obligations for international holders. This is existing compliance applied to new rails.", "规则解读型"),
    ("45% institutional large transfers means significant North American stablecoin volume crosses BSA thresholds. CTR filing at $10k+ and SAR obligations apply to stablecoin processors the same as traditional payment firms.", "规则解读型"),
    ("Using BTC/ETH/stablecoins for international payments: track FMV at each transaction date for income reporting and CARF compliance. From 2026, cross-border crypto B2B payments flow into automatic authority reporting.", "场景落地型"),
    ("82% of USDC transfers are issuer operations — actual user-driven taxable volume is far smaller than headlines suggest. Under CARF, what matters is user transactions. The real compliance burden is lower than it looks.", "反直觉观点型"),
    ("Crypto fraud and tax evasion share the same gap: incomplete records. Strong KYC/AML controls produce the transaction documentation that accurate tax reporting requires. Compliance infrastructure serves both purposes.", "场景落地型"),
    ("ETF vs direct BTC holding has a concrete tax difference: ETF gains flow through 1099-B with the fund as intermediary; direct BTC requires per-wallet cost basis tracking. Different operational compliance burdens.", "规则解读型"),
    ("Strategy's BTC looks like a treasury bet — but under ASC 350, unrealized gains flow through the P&L quarterly. Corporate crypto accounting ≠ personal tax. Completely different obligations, completely different structure.", "反直觉观点型"),
    ("Staking ETH in custody adds a specific tax layer: rewards are ordinary income at FMV on receipt; principal and accumulated rewards each have separate cost basis when disposed. Two distinct tax events, not one.", "规则解读型"),
    ("AI agents executing on-chain trades raise an unresolved question: who is the taxpayer? Current IRS guidance points to the controlling account holder. Automated agent activity creates your tax obligations either way.", "反直觉观点型"),
    ("BlackRock and Franklin Templeton in the same tokenization ecosystem brings institutional compliance expectations. CARF applies to every tokenized fund disposal for cross-border holders. Scale amplifies the obligation.", "规则解读型"),
    ("Tokenizing on Ethereum sounds transformative — but gas fees paid during tokenized security transfers are themselves taxable disposals. Infrastructure-level costs create reporting obligations at every layer.", "反直觉观点型"),
    ("On-chain direct ownership vs. street-name isn't just philosophical — it's a tax question. Direct token ownership makes you the holder of record, changing who bears CARF reporting obligations and when disposals trigger.", "反直觉观点型"),
    ("CLARITY Act separates passive balance yield from active DeFi yield. Passive yield resembles interest; active protocol yield may be ordinary income or capital gain. Classification determines both the rate and the form.", "规则解读型"),
    ("Financial institutions entering tokenization at production scale need CARF-compliant reporting infrastructure before launch. The build timeline for automated cross-border reporting is 6-12 months. Start now for 2026.", "场景落地型"),
    ("Supply of tokenized assets is scaling — institutional demand is bottlenecked by compliance uncertainty. The $300T market isn't blocked by technology; it's blocked by unresolved CARF frameworks for cross-border holders.", "反直觉观点型"),
    ("Hong Kong VASP licensing requires exchanges to retain AEOI/CARF-compatible transaction data. Institutional capital entering via Hong Kong faces both local VASP obligations and home-country CARF reporting simultaneously.", "规则解读型"),
    ("NYSE partnership brings full securities reporting to tokenized assets: 1099-B issuance, per-lot capital gains tracking, and CARF cross-border obligations for international holders. Existing compliance, new rails.", "规则解读型"),
    ("278% hashrate growth means mining income scales proportionally — all ordinary income at FMV on receipt. At this scale, MACRS 5-year depreciation and energy cost deductions are the material tax efficiency levers.", "场景落地型"),
    ("Australia Tranche 2 goes live July — 90,000 entities now have AML/CFT obligations. For crypto businesses: complete AUSTRAC registration, update your AML program, align monitoring with Travel Rule requirements.", "场景落地型"),
    ("Post-halving mining economics are brutal — but most miners ignore the tax lever. Mining income is ordinary income at FMV on receipt; depreciation and electricity deductions can significantly offset gross revenue.", "反直觉观点型"),
    ("The survey gap is actionable: export exchange transaction histories, add DeFi wallet records, identify missing basis. The 65% who haven't fixed their records have a limited window before CARF cross-referencing begins.", "场景落地型"),
    ("Privacy coins still create taxable events — ZEC disposals trigger capital gains the same as BTC. But IRS enhanced enforcement means exchanges are more likely to flag privacy coin 1099-DA transactions for scrutiny.", "规则解读型"),
    ("RWA composability creates a tax stack: collateral use may trigger disposition; yield adds ordinary income; reinvesting adds to basis. Each composability layer is a discrete tax question needing separate documentation.", "规则解读型"),
    ("Mining-to-AI conversion is a significant tax event: retired equipment triggers depreciation recapture; new equipment may qualify for Section 179 or bonus depreciation. Document the transition costs carefully.", "场景落地型"),
    ("Australia Travel Rule is mandatory from July 2026 — VASPs must pass originator and beneficiary information with every transfer. Practical step: implement TRISA or OpenVASP-compatible messaging before the deadline.", "场景落地型"),
    ("2026 compliance calendar: CARF goes live, GENIUS Act enforcement begins, per-wallet IRS rules fully in effect. Year-end loss harvesting and basis optimization are still actionable now — don't wait for Q1 filing pressure.", "场景落地型"),
    ("BTC ETF vs direct BTC: ETF flows through 1099-B with the fund as intermediary; direct BTC requires per-wallet cost basis tracking under IRS rules. The choice of exposure vehicle drives compliance complexity.", "规则解读型"),
    ("Self-custody gives asset sovereignty — not tax sovereignty. Transfers between your own wallets are non-taxable, but IRS expects cost basis records for every wallet you control. Sovereignty includes the record-keeping.", "反直觉观点型"),
    ("Institutional crypto research is shaped by three frameworks: FIT21 commodity classification, CARF cross-border reporting, and ASC 350 fair value accounting — together reshaping how institutions model crypto exposure.", "规则解读型"),
    ("Revolut's $10B stablecoin volume + Nubank's banking license signals payment processors are becoming regulated financial institutions. Under CARF, licensed processors have mandatory cross-border reporting obligations.", "规则解读型"),
    ("On-chain proof-of-asset verification creates a compliance byproduct: immutable records that satisfy CARF documentation. Reserve proof data and cross-border tax reporting data are the same underlying transaction records.", "规则解读型"),
    ("SEC/CFTC coordination resolves a key tax uncertainty: securities get capital gains + ordinary income treatment; commodities may qualify for Section 1256's 60/40 split. Classification determines forms and rates.", "规则解读型"),
    ("T-bill-backed RWA tokens generate Treasury interest — but tax treatment depends on structure. Pass-through structures preserve Treasury interest character; opaque wrappers may recharacterize it as ordinary income.", "规则解读型"),
    ("Three paths into mainstream crypto, three tax structures: ETF gains via 1099-B; merchant acceptance triggers income at receipt; spending is a disposal at FMV. Each path has different record-keeping requirements.", "场景落地型"),
    ("Mining and HPC at the same facility need separate tax accounting: mining income is ordinary income at FMV; HPC hosting is service revenue. Shared costs must be allocated between both streams — mixed-use rules apply.", "场景落地型"),
    ("Phase 1 data center build is a capital expenditure moment: mining equipment gets MACRS 5-year depreciation; data center infrastructure may qualify for Section 179 immediate expensing or 40% bonus depreciation for 2025.", "场景落地型"),
    ("Galaxy's institutional research leads market thinking — but the tax layer is where strategies get tested. ASC 350 fair value reporting, CARF compliance, and per-lot basis tracking are the operational realities now.", "规则解读型"),
    ("Ripple ruling: XRP sold on secondary markets is not a security — pointing toward commodity treatment under FIT21 and potentially Section 1256's 60/40 split. Classification determines which forms and rates apply.", "规则解读型"),
    ("March-end: review Q1 positions now. Identify short-term gains eligible for harvesting, confirm basis on positions near the 12-month threshold, and check if 1099-DA corrections are needed before the April deadline.", "场景落地型"),
    ("Spring market moves build short-term gains. If you're approaching the 12-month threshold on any holding, the gap between short-term (up to 37%) and long-term (0-20%) rates is material. Check your holding periods now.", "场景落地型"),
    ("Last week's volatility created discrete tax events for anyone who rebalanced or got liquidated. Document FMV at each transaction, note holding periods, flag losses — harvestable now with no wash-sale rule blocking you.", "场景落地型"),
    ("Wallet address authentication changes at a VASP directly affect cost basis records — the authenticated address is what your transaction history is tied to. Update records when addresses change or you create basis gaps.", "场景落地型"),
    ("Bank-grade crypto custody changes the reporting chain: banks custodying digital assets under SAB 122 become de facto brokers with 1099-DA issuance obligations. The custodian is now the first line of CARF compliance.", "规则解读型"),
    ("Strategy's BTC position looks like a treasury bet — but under ASC 350, unrealized gains flow through the income statement quarterly. Corporate crypto accumulation isn't tax-deferred. Every mark-to-market hits the P&L.", "反直觉观点型"),
    ("Broad macro selloff = ideal tax-loss harvesting: correlated losses can be captured simultaneously. Per-wallet tracking is now mandatory — systematic harvesting requires careful wallet-level execution to stay compliant.", "反直觉观点型"),
    ("As DLT becomes settlement infrastructure, CARF reporting becomes embedded in every transaction. When DLT is the settlement layer, the data for cross-border tax reporting can theoretically be generated automatically.", "规则解读型"),
    ("Fidelity's tax optimization applies to crypto: IRA defers gains entirely; donating appreciated crypto avoids capital gains while deducting FMV; per-wallet tracking enables direct indexing. All three are available now.", "场景落地型"),
    ("Institutional trading at inflection means compliance must be built for volume: per-lot basis tracking, 1099-DA reconciliation, CARF cross-border reporting. This is an automation problem, not just a compliance checkbox.", "规则解读型"),
    ("Fink's 1996 internet comparison is apt in one way nobody mentions: 1996 internet had no standardized tax reporting. CARF is the crypto equivalent of e-commerce tax standardization — arriving on a compressed timeline.", "反直觉观点型"),
    ("Tokenized stock composability in DeFi creates layered tax events: collateral use may trigger disposition; yield adds ordinary income; reinvesting adds to basis. Each composability layer is a separate tax question.", "规则解读型"),
    ("DTCC setting tokenization standards must include tax reporting standardization. DTCC's traditional role produces 1099-B data; for tokenized assets, the equivalent means CARF compliance built into the infrastructure spec.", "规则解读型"),
    ("Invisible payments means invisible compliance obligations — until they're not. Every cross-border crypto payment through embedded rails is CARF-reportable from 2026. The easier it is to miss, the costlier the catch-up.", "反直觉观点型"),
    ("European GPU conversion is a multi-jurisdiction tax event: Swedish asset disposal rules, depreciation recapture on retired mining equipment, VAT on hardware. Mining-to-AI pivots need coordinated cross-border planning.", "场景落地型"),
    ("2.1GW across US and Canada means two separate tax regimes for the same energy costs. Transfer pricing for shared infrastructure between jurisdictions must be documented — the IRS and CRA both scrutinize this.", "场景落地型"),
    ("CARF requires automated data pipelines from transaction systems to tax authorities. Manual reporting at institutional scale doesn't work — compliance infrastructure must be built before enforcement begins, not after.", "场景落地型"),
    ("Macro repricing gets headlines, but the regulatory layer advances regardless: CARF, GENIUS Act enforcement, per-wallet IRS tracking — all active in 2026. Compliance infrastructure doesn't pause for market cycles.", "规则解读型"),
]

def search_tweets(query, count=10):
    """Call TwitterAPI.io advanced search via curl subprocess"""
    import subprocess
    params = urllib.parse.urlencode({
        "query": query,
        "queryType": "Latest",
        "count": count
    })
    url = f"{BASE_URL}?{params}"
    try:
        result = subprocess.run(
            ["curl", "-s", "-X", "GET", url,
             "-H", f"X-API-Key: {API_KEY}",
             "-H", "User-Agent: curl/8.7.1",
             "--max-time", "30"],
            capture_output=True, text=True, timeout=35
        )
        if result.returncode != 0:
            print(f"  curl error: {result.stderr}")
            return []
        data = json.loads(result.stdout)
        return data.get("tweets", [])
    except Exception as e:
        print(f"  ERROR: {e}")
        return []

def is_competitor(username):
    return username.lower() in COMPETITOR_ACCOUNTS

def is_retweet(tweet):
    text = tweet.get("text", "")
    return text.startswith("RT @")

def is_english(tweet):
    return tweet.get("lang", "") == "en"

def is_ad_or_low_quality(tweet):
    text = tweet.get("text", "").lower()
    # 纯广告特征
    ad_patterns = ["win $", "giveaway", "airdrop", "100x", "pump", "buy now", "🚀🚀🚀", "dyor", "not financial advice"]
    for p in ad_patterns:
        if p in text:
            return True
    # 内容过短
    if len(tweet.get("text", "")) < 50:
        return True
    return False

def find_best_reply(tweet_text, query):
    """从130条回帖中找最匹配的"""
    tweet_lower = tweet_text.lower()

    # 关键词权重匹配
    best_idx = 0
    best_score = -1

    keyword_map = {
        "1099-da": [2, 7, 8, 11, 20, 32],
        "form 8949": [2, 7, 8, 19, 32],
        "cost basis": [0, 1, 7, 11, 21, 24, 47],
        "gas fee": [0, 4],
        "staking reward": [10, 81],
        "staking": [10, 81],
        "loss harvest": [9, 118],
        "wash sale": [9, 114, 118],
        "carf": [23, 34, 49, 52, 66, 128],
        "dac8": [34, 66, 72, 128],
        "genius act": [22, 51, 57],
        "stablecoin": [12, 13, 14, 22, 35, 40, 55, 63],
        "fit21": [5, 53, 57, 105, 111],
        "per-wallet": [21, 47],
        "tokenized": [17, 18, 25, 26, 37, 38, 41, 58],
        "defi": [48, 82, 86, 96, 123],
        "swap": [48, 54],
        "mining": [15, 91, 93, 97, 108, 109, 126, 127],
        "etf": [36, 79, 100, 107],
        "ordinary income": [6, 10, 46, 81],
        "capital gain": [9, 26, 30, 54, 112, 113, 114],
        "1099-misc": [10, 46],
        "mica": [51, 72],
        "travel rule": [44, 64, 98],
        "aml": [22, 78, 92, 98],
        "rwa": [39, 58, 96, 106],
        "blockchain settlement": [45],
        "btc etf": [79, 100],
        "privacy coin": [95],
        "long-term": [30, 54, 112, 113],
        "holding period": [30, 54, 112, 113, 114],
    }

    for keyword, indices in keyword_map.items():
        if keyword in tweet_lower:
            for idx in indices:
                if idx < len(ALL_REPLIES):
                    score = tweet_lower.count(keyword) * 2
                    if score > best_score:
                        best_score = score
                        best_idx = idx

    # 如果没有匹配关键词，根据query找
    if best_score <= 0:
        query_lower = query.lower()
        for keyword, indices in keyword_map.items():
            if keyword in query_lower and indices:
                best_idx = indices[0]
                break

    return best_idx

def get_match_reason(tweet_text, reply_text):
    """生成简短匹配理由"""
    tweet_lower = tweet_text.lower()

    reasons = {
        "1099-da": "同涉1099-DA申报问题",
        "form 8949": "同涉Form 8949纠错",
        "cost basis": "同谈成本基础计算",
        "gas fee": "同涉gas费处理",
        "staking": "同谈质押奖励税务",
        "loss harvest": "同讨论亏损收割策略",
        "wash sale": "同提无洗售规则优势",
        "carf": "同涉CARF合规要求",
        "dac8": "同涉DAC8欧盟框架",
        "genius act": "同谈GENIUS法案合规",
        "stablecoin": "同涉稳定币税务处理",
        "fit21": "同涉FIT21商品分类",
        "per-wallet": "同讨论钱包维度追踪",
        "tokenized": "同涉代币化资产合规",
        "defi": "同涉DeFi交易纳税",
        "swap": "同谈代币兑换纳税",
        "mining": "同涉挖矿收入税务",
        "etf": "同涉加密ETF税务",
        "ordinary income": "同讨论普通收入分类",
        "capital gain": "同涉资本利得税务",
        "long-term": "同提长持税率优势",
    }

    for keyword, reason in reasons.items():
        if keyword in tweet_lower:
            return reason

    return "话题高度相关"


def main():
    # 15个搜索查询
    queries = [
        "1099-DA Form 8949 crypto cost basis",
        "crypto cost basis gas fees IRS",
        "staking rewards ordinary income IRS tax",
        "crypto tax loss harvesting W2 income",
        "CARF DAC8 crypto reporting 2026",
        "GENIUS Act stablecoin compliance AML",
        "FIT21 digital commodity classification tax",
        "per-wallet cost basis IRS 2025 tracking",
        "stablecoin payment tax disposal FMV",
        "crypto wash sale rule loss harvest 2025",
        "DeFi swap taxable event IRS capital gains",
        "tokenized securities CARF reporting cross-border",
        "1099-DA missing cost basis phantom gains",
        "crypto ETF 1099-B tax treatment direct BTC",
        "crypto mining income depreciation tax deductions",
    ]

    results = []
    search_count = 0
    total_found = 0
    kept_count = 0
    seen_tweet_ids = set()

    for query in queries:
        print(f"\n搜索: {query}")
        tweets = search_tweets(query, count=10)
        search_count += 1
        total_found += len(tweets)

        kept_in_query = 0
        for tweet in tweets:
            tweet_id = tweet.get("id", "")
            if tweet_id in seen_tweet_ids:
                continue

            author = tweet.get("author", {})
            username = author.get("userName", "")

            # 过滤
            if is_competitor(username):
                print(f"  跳过友商: @{username}")
                continue
            if is_retweet(tweet):
                print(f"  跳过转推: @{username}")
                continue
            if not is_english(tweet):
                print(f"  跳过非英文: @{username} lang={tweet.get('lang')}")
                continue
            if is_ad_or_low_quality(tweet):
                print(f"  跳过低质/广告: @{username}")
                continue

            seen_tweet_ids.add(tweet_id)

            tweet_text = tweet.get("text", "")
            tweet_url = tweet.get("url", f"https://x.com/{username}/status/{tweet_id}")
            tweet_likes = tweet.get("likeCount", 0)

            # 找最匹配回帖
            best_idx = find_best_reply(tweet_text, query)
            matched_reply, angle = ALL_REPLIES[best_idx]
            match_reason = get_match_reason(tweet_text, matched_reply)

            results.append({
                "search_query": query,
                "tweet_url": tweet_url,
                "tweet_account": f"@{username}",
                "tweet_text": tweet_text,
                "tweet_likes": tweet_likes,
                "matched_reply": matched_reply,
                "reply_angle": angle,
                "match_reason": match_reason
            })

            kept_in_query += 1
            kept_count += 1
            print(f"  ✓ @{username} | likes={tweet_likes} | {tweet_text[:60]}...")

        print(f"  本次保留 {kept_in_query} 条")
        time.sleep(2)  # 速率控制

    # 保存结果
    output_path = "/Users/nightyoung/社媒运营工具/sector-radar/output/search_matches.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"搜索次数: {search_count}")
    print(f"找到推文总数: {total_found}")
    print(f"过滤后保留: {kept_count}")
    print(f"结果已保存到: {output_path}")

    return results

if __name__ == "__main__":
    main()
