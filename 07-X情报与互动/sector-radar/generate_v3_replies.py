#!/usr/bin/env python3
"""
Generate final_reply and final_angle for each tweet based on actual tweet content.
Rules:
- Angle logic: user misunderstanding -> 反直觉观点型; product/feature/event -> 规则解读型; regulation/new law -> 场景落地型
- Each reply: phenomenon + rule/reason + conclusion, in one sentence
- Under 220 characters
- No FinTax brand name
- Tone: industry peer, not salesy
"""

import json

# All replies manually crafted per tweet content
REPLIES = [
    # 1 - CryptoTaxSucks - multi-wallet Form 8949 process
    {
        "url": "https://x.com/CryptoTaxSucks/status/2035148112055136709",
        "final_reply": "Exchange-to-exchange transfers make 1099-DA basis almost always wrong — Exchange B can't know what you paid on Exchange A, so you supply correct basis on Form 8949 yourself.",
        "final_angle": "规则解读型"
    },
    # 2 - bintelsuhi - 1099-DA explains proceeds not gains
    {
        "url": "https://x.com/bintelsuhi/status/2033591152461611129",
        "final_reply": "1099-DA is gross proceeds only — it doesn't calculate your gain. That work happens on Form 8949 where you add basis, holding period, and gain/loss. Conflating the two leads to overpayment.",
        "final_angle": "反直觉观点型"
    },
    # 3 - summ_app - corrected numbers on 8949, provide own basis
    {
        "url": "https://x.com/summ_app/status/2029316494996250903",
        "final_reply": "Proceeds match 1099-DA: that's the IRS check in 2025. Basis is yours to document — if 1099-DA says 'unknown,' supply it on 8949 yourself. The IRS won't lower your gains for you.",
        "final_angle": "规则解读型"
    },
    # 4 - TheCryptoCPA - 2025 IRS matching checks proceeds not basis
    {
        "url": "https://x.com/TheCryptoCPA/status/2028198918966632770",
        "final_reply": "IRS 2025 matching targets proceeds on 8949 vs. 1099-DA — cost basis mismatches skip automated notices this year. But deferred basis fixes compound: future audits reconstruct from scratch.",
        "final_angle": "反直觉观点型"
    },
    # 5 - TheCryptoCPA - unknown cost basis from cross-platform transfer
    {
        "url": "https://x.com/TheCryptoCPA/status/2026756889187594249",
        "final_reply": "'Unknown' basis on 1099-DA is fixable: override it on Form 8949 with documented purchase records. Silence isn't taxed at full proceeds — but only if you file the correction yourself.",
        "final_angle": "规则解读型"
    },
    # 6 - theweb3wizard00 - blank cost basis Box 1g, IRS assumes $0
    {
        "url": "https://x.com/theweb3wizard00/status/2026393306247147686",
        "final_reply": "IRS assuming $0 basis when Box 1g is blank isn't law — it's the default if you don't file Form 8949 with documented basis. The risk is inaction, not the blank box itself.",
        "final_angle": "反直觉观点型"
    },
    # 7 - TheReviken - manually input trades on 8949
    {
        "url": "https://x.com/TheReviken/status/2025087457075888629",
        "final_reply": "Manual entry works, but watch for double-counted wash sale adjustments or missed transfers across exchanges on 1099-DA — verify every line before carrying to Schedule D.",
        "final_angle": "规则解读型"
    },
    # 8 - richbycoin_news - Coinbase says 1099-DA over-reports stablecoin trades and gas fees
    {
        "url": "https://x.com/richbycoin_news/status/2030669746161557785",
        "final_reply": "Stablecoin swap over-reporting is a real issue, but a zero-gain trade must still be proven zero — you still need records of every swap even when no tax is owed.",
        "final_angle": "反直觉观点型"
    },
    # 9 - SKuzminskiy - gas fees in 8949 is compliance overkill
    {
        "url": "https://x.com/SKuzminskiy/status/2030405619027456043",
        "final_reply": "The compliance burden on gas fees is real, but current law has no materiality threshold — every swap is reportable regardless of size until Congress clarifies otherwise.",
        "final_angle": "规则解读型"
    },
    # 10 - MoonscapeHQ - include fees in cost basis
    {
        "url": "https://x.com/MoonscapeHQ/status/1909305998969651644",
        "final_reply": "Gas fees belong in cost basis under IRS Pub. 551 — buy ETH at $3,000 + $20 gas = $3,020 basis. Every fee you miss overstates your taxable gain. Track at the transaction level from now.",
        "final_angle": "场景落地型"
    },
    # 11 - futurenftmints - gas fees add to transaction cost per Pub 551
    {
        "url": "https://x.com/futurenftmints/status/1481657332782096389",
        "final_reply": "Pub. 551 cost basis rules apply to gas by analogy — no explicit IRS crypto ruling, but the position that gas adds to basis is broadly accepted. Excluding it overstates every gain.",
        "final_angle": "规则解读型"
    },
    # 12 - heranishi - ETH staking taxed as ordinary income at FMV at receipt, then cap gains on sale
    {
        "url": "https://x.com/heranishi/status/2039096244006441054",
        "final_reply": "Correct on the mechanics — but missed planning angle: if ETH drops below your $2,000 receipt price before you sell, you realize a capital loss that offsets other gains.",
        "final_angle": "场景落地型"
    },
    # 13 - CryptofolioApp - tracker shows staking rewards as capital gain, IRS says ordinary income
    {
        "url": "https://x.com/CryptofolioApp/status/2037525468262363279",
        "final_reply": "Misclassifying staking rewards as capital gains also sets wrong basis lots — software errors here ripple into incorrect holding periods and doubled gains at sale.",
        "final_angle": "反直觉观点型"
    },
    # 14 - CryptoTaxG - US taxes staking as ordinary income up to 37%, then capital gains on sale
    {
        "url": "https://x.com/CryptoTaxG/status/2036431137216647470",
        "final_reply": "The 'double hit' can reverse: ordinary income at receipt becomes your cost basis. If price drops before you sell, the second event creates a capital loss that partially offsets the first.",
        "final_angle": "反直觉观点型"
    },
    # 15 - ArbazCryptoTax - Jarrett case, client earned $85K staking rewards, didn't report
    {
        "url": "https://x.com/ArbazCryptoTax/status/2036422388636917985",
        "final_reply": "IRS chose refund over litigation in Jarrett — an open question, not settled law. Until a court rules, file staking rewards as ordinary income at receipt. The $85k scenario is the real-world risk for non-reporters.",
        "final_angle": "反直觉观点型"
    },
    # 16 - Brooke38868346 - ATOM staking 12% APY taxable at marginal rate at receipt
    {
        "url": "https://x.com/Brooke38868346/status/2029696349332234414",
        "final_reply": "Blindsided tax bills come from earning 12% APY but owing 32-37% on rewards at receipt. Liquidity planning for staking taxes — setting aside fiat proportionally — matters as much as the yield itself.",
        "final_angle": "场景落地型"
    },
    # 17 - SoCalCryptoTax - California staking reminder
    {
        "url": "https://x.com/SoCalCryptoTax/status/2012512777118888446",
        "final_reply": "California has no preferential long-term rate — staking rewards taxed as ordinary income at receipt AND again on appreciation. High earners in CA face combined rates exceeding 50%.",
        "final_angle": "场景落地型"
    },
    # 18 - RealDealCPA - staking income taxable when you control it
    {
        "url": "https://x.com/RealDealCPA/status/1993828425803681814",
        "final_reply": "Dominion-and-control test drives timing. Locked validators may differ from liquid staking — stETH accrues rewards continuously, locked positions may defer. No clear IRS guidance yet on the distinction.",
        "final_angle": "规则解读型"
    },
    # 19 - Canes43oU - asking if crypto staking is taxed like dividends
    {
        "url": "https://x.com/Canes43oU/status/1992367788934214023",
        "final_reply": "Not like qualified dividends. Rev. Proc. 2025-31 treats crypto staking income as ordinary income — same rate as wages. Dividends can qualify for 0-20% preferential rates; staking cannot.",
        "final_angle": "规则解读型"
    },
    # 20 - JulianoFinance - will staking be treated like equity dividends
    {
        "url": "https://x.com/JulianoFinance/status/1953263147130753530",
        "final_reply": "Not yet. Rev. Rul. 2023-14 and Rev. Proc. 2025-31 both treat staking as ordinary income. Deferral proposals exist in Congress but nothing is enacted — plan around current rules.",
        "final_angle": "规则解读型"
    },
    # 21 - donemilioos - staking income goes to Gross Income, LQ/farming same
    {
        "url": "https://x.com/donemilioos/status/1946334859766776153",
        "final_reply": "Each staking reward receipt creates a separate tax lot. 100 daily rewards = 100 separate basis lots to track at sale. Most tracking software mishandles this — verify lot-level accuracy.",
        "final_angle": "场景落地型"
    },
    # 22 - WatcherGuru - SEC says staking on PoS is not a security
    {
        "url": "https://x.com/WatcherGuru/status/1928256793399931048",
        "final_reply": "SEC saying staking isn't a security doesn't change the IRS rule — Rev. Rul. 2023-14 still taxes staking rewards as ordinary income at receipt. Two agencies, two separate determinations.",
        "final_angle": "反直觉观点型"
    },
    # 23 - MoonscapeHQ - two main treatments: ordinary income vs capital gains
    {
        "url": "https://x.com/MoonscapeHQ/status/1909305938840109267",
        "final_reply": "Same ETH can have different treatments depending on how you got it — bought on exchange is a capital asset, earned from staking creates an ordinary income lot. Classification drives the rate at sale.",
        "final_angle": "场景落地型"
    },
    # 24 - MrEeyoreEsq - wants IRS to rescind staking rewards ordinary income guidance
    {
        "url": "https://x.com/MrEeyoreEsq/status/1898129448815276290",
        "final_reply": "Rescinding requires new rulemaking or a court ruling — neither is imminent. The realistic reform is at-sale deferral, which bipartisan bills are advancing. File as ordinary income until that changes.",
        "final_angle": "规则解读型"
    },
    # 25 - TazCoLab - DAC8 and CARF in full effect 2026, data collection already happening
    {
        "url": "https://x.com/TazCoLab/status/2036796616330338401",
        "final_reply": "Data collection is live, but first exchange-to-authority reporting hits in 2027. Use 2026 now: register TINs, audit historical exchange records. Penalties attach when reporting deadlines arrive.",
        "final_angle": "场景落地型"
    },
    # 26 - cryptaxpt - SEMP carve-out from CARF scope, stablecoins under CRS instead
    {
        "url": "https://x.com/cryptaxpt/status/2029542450898055277",
        "final_reply": "SEMP carve-out matters for regulated e-money tokens — they move to CRS, not CARF. Misclassifying a non-qualifying stablecoin as SEMP triggers unexpected CARF obligations and audit exposure.",
        "final_angle": "规则解读型"
    },
    # 27 - ThePaypers - EU/UK CARF mandatory from Jan 2026, DAC8 across 27 states
    {
        "url": "https://x.com/ThePaypers/status/2018157471718682728",
        "final_reply": "CARF compliance for platforms means collecting customer TINs — often missing — and resolving 'reportable jurisdiction' for multi-national users. Clean data pipelines are harder to build than they look.",
        "final_angle": "场景落地型"
    },
    # 28 - quantfinance_ie - DAC8/CARF active in Ireland
    {
        "url": "https://x.com/quantfinance_ie/status/2017630342706860437",
        "final_reply": "Ireland under DAC8: Revenue receives your crypto data from 2027. Action now: confirm your Irish TIN is correctly registered with all exchanges — errors in self-certification create compliance gaps that compound.",
        "final_angle": "场景落地型"
    },
    # 29 - bradarska1 - OECD CARF and DAC8 in force Jan 1 2026
    {
        "url": "https://x.com/bradarska1/status/2012865157962105267",
        "final_reply": "CARF and DAC8 align on most assets but diverge on DeFi and NFTs — CARF scope is narrower, DAC8 broader. Multi-jurisdictional operators may face asymmetric obligations on identical transactions.",
        "final_angle": "规则解读型"
    },
    # 30 - CryptoTaxFixer - DAC8 is EU version of CARF, US not signed on yet
    {
        "url": "https://x.com/CryptoTaxFixer/status/2011082557165899800",
        "final_reply": "DAC8 isn't identical to CARF — it adapts the framework with EU-specific fields and a broader reach. CARF compliance doesn't guarantee DAC8 compliance for non-EU platforms with EU users.",
        "final_angle": "反直觉观点型"
    },
    # 31 - cryptocoinatlas - EU DAC8 standardized crypto reporting for CASPs
    {
        "url": "https://x.com/cryptocoinatlas/status/2010685532989276203",
        "final_reply": "'Standardized' means per-transaction: asset type, FMV, disposal/income classification, verified user identity. The data quality problem at scale is non-trivial for most CASPs to solve by year-end.",
        "final_angle": "场景落地型"
    },
    # 32 - ibetoncrypto - bank-style crypto reporting in 2026 with DAC8 + CARF
    {
        "url": "https://x.com/ibetoncrypto/status/2009553983518466482",
        "final_reply": "Banks report balances and interest. CARF requires per-transaction reporting with asset classification, FMV at disposal, and income/capital distinction. Significantly more complex than bank-style reporting.",
        "final_angle": "反直觉观点型"
    },
    # 33 - nextinweb3 - crypto privacy faces toughest test with CARF and DAC8
    {
        "url": "https://x.com/nextinweb3/status/2009170069960429997",
        "final_reply": "Self-custody wallets aren't directly in CARF/DAC8 scope — exchanges report user activity, not wallet holdings. What's gone is using regulated exchanges without a tax trail.",
        "final_angle": "规则解读型"
    },
    # 34 - Marsses_Crypto - EU tracking crypto transactions from Jan 1 2026
    {
        "url": "https://x.com/Marsses_Crypto/status/2008866468050632842",
        "final_reply": "The real compliance risk is the gap between what exchanges report and what you filed. Any mismatch triggers inquiry. Closing that gap before filing is the operational priority now.",
        "final_angle": "规则解读型"
    },
    # 35 - RemiDAoust - Treasury GENIUS Act requires BSA/AML/SAR/KYC for stablecoin issuers
    {
        "url": "https://x.com/RemiDAoust/status/2036795313084567702",
        "final_reply": "GENIUS Act makes stablecoin issuers full BSA financial institutions — AML programs, SAR filings, KYC, technical controls — without granting bank charter privileges. That gap is the implementation challenge.",
        "final_angle": "规则解读型"
    },
    # 36 - Cointelegraph - Delaware bipartisan stablecoin bill: 1:1 reserves, monthly audits, AML/KYC
    {
        "url": "https://x.com/Cointelegraph/status/2036299566509645944",
        "final_reply": "State-chartered bank issuing GENIUS-compliant stablecoins bypasses the federal licensing track. State bank + stablecoin issuance could create regulatory arbitrage federal regulators didn't intend.",
        "final_angle": "反直觉观点型"
    },
    # 37 - JeanClawd99 - GENIUS Act 1:1 reserves, audits, AML means payment layer runs on bank-like entities
    {
        "url": "https://x.com/JeanClawd99/status/2034662725264003563",
        "final_reply": "1:1 reserves + monthly audits + AML programs + federal oversight: the compliance stack only well-capitalized entities can maintain. GENIUS Act effectively concentrates stablecoin issuance among bank-like institutions.",
        "final_angle": "反直觉观点型"
    },
    # 38 - ChainLabo - OCC GENIUS Act: 1:1 reserves, audits, AML/BSA for enterprise nodes
    {
        "url": "https://x.com/ChainLabo/status/2032385124839334149",
        "final_reply": "Which assets qualify as 1:1 backing under OCC rules? T-bills: yes. Overnight repos: likely. Bank deposits: yes but with counterparty risk. Reserve asset composition rules will drive issuer strategy.",
        "final_angle": "规则解读型"
    },
    # 39 - TFTC21 - Florida passes first state stablecoin bill, GENIUS Act alignment
    {
        "url": "https://x.com/TFTC21/status/2030018600833274162",
        "final_reply": "Florida's state licensing creates a head start. Whether federal preemption applies when GENIUS enforcement begins in 2027 is open — state-first strategy could be an advantage or create conflicting obligations.",
        "final_angle": "场景落地型"
    },
    # 40 - FreeThinkerInc - GENIUS + Clarity Act: stablecoins as commodities, FinCEN/BSA compliance still applies
    {
        "url": "https://x.com/FreeThinkerInc/status/2029551152032084117",
        "final_reply": "Clarity Act shifts oversight to CFTC, GENIUS Act covers issuers under OCC/federal framework — different regulators for issuer licensing vs. DeFi stablecoin use. Two separate compliance tracks.",
        "final_angle": "规则解读型"
    },
    # 41 - OptionsLabApp - asking about stablecoin regulation advancing in Congress
    {
        "url": "https://x.com/OptionsLabApp/status/2029314882042998796",
        "final_reply": "Three active tracks: GENIUS Act federal issuer licensing, state bills like Florida SB 314, and OCC implementation rules. Each has different timelines — operators must track which obligations apply first.",
        "final_angle": "规则解读型"
    },
    # 42 - nifty0x - BitGo FYUSD GENIUS-compliant stablecoin for Asian institutions
    {
        "url": "https://x.com/nifty0x/status/2025677613541274033",
        "final_reply": "Bank-issued stablecoins under GENIUS Act carry FDIC implications and compete directly with payment networks. BitGo's FYUSD is an early test case for whether bank-charter issuers command a meaningful trust moat.",
        "final_angle": "场景落地型"
    },
    # 43 - edgeandnode - GENIUS Act monthly reserve disclosure, AML audit trails, MiCA parallel
    {
        "url": "https://x.com/edgeandnode/status/2021733884145328539",
        "final_reply": "Monthly reserve disclosure + AML audit trails that hold up to regulatory scrutiny: any gap between disclosed and actual reserves becomes a federal matter, not just a PR problem.",
        "final_angle": "规则解读型"
    },
    # 44 - HyperXAware - GENIUS Act CFTC oversight, built-in KYC/AML for stablecoin compliance
    {
        "url": "https://x.com/HyperXAware/status/2021624235387465855",
        "final_reply": "GENIUS Act treats stablecoins closer to money market instruments — implications for DeFi protocols using them as settlement: leverage, custody rules, and compliance obligations may apply differently.",
        "final_angle": "规则解读型"
    },
    # 45 - pennycheck - watching GENIUS Act vote, bullish for GLXY, FIT21 clarity on securities vs commodities
    {
        "url": "https://x.com/pennycheck/status/1924497668623024633",
        "final_reply": "GENIUS Act clarity lets institutional capital deploy into stablecoins without legal opinion risk — that's the product Galaxy is buying. Regulatory certainty reduces compliance cost for every operator.",
        "final_angle": "场景落地型"
    },
    # 46 - BitAngels - per Rev Proc 2024-28, universal cost basis eliminated, wallet-by-wallet now required
    {
        "url": "https://x.com/BitAngels/status/2034730999528267820",
        "final_reply": "Per-wallet basis is mandatory from Jan 1, 2025 under Rev. Proc. 2024-28. If you used universal basis for 2024 and missed the transition election window, your 2024 filing may conflict with 2025 rules.",
        "final_angle": "反直觉观点型"
    },
    # 47 - summ_app - per-wallet basis new in 2025, can't pool across exchanges
    {
        "url": "https://x.com/summ_app/status/2026764686650163399",
        "final_reply": "Per-wallet removes cross-exchange HIFO optimization. Previously you could pick the highest basis lot from any wallet globally — now HIFO/FIFO applies only within the wallet where the sale occurs.",
        "final_angle": "规则解读型"
    },
    # 48 - TimBR_X - links to IRS guidance, Rev Proc 2024-28 per-wallet, 1099-DA
    {
        "url": "https://x.com/TimBR_X/status/1954625969005744353",
        "final_reply": "Rev. Proc. 2024-28 transition guidance tells you how to convert prior universal basis allocations to per-wallet before your first 2025 disposal. Read it before filing — the mechanics are in the procedure.",
        "final_angle": "规则解读型"
    },
    # 49 - SaitoshiAgent - per-wallet cost basis mandatory from Jan 1 2025 per Rev Proc 2024-28
    {
        "url": "https://x.com/SaitoshiAgent/status/1938378692151152981",
        "final_reply": "Per-wallet forces wallet-level lot tracking. Complexity: wallets with mixed sources — purchases, transfers, staking rewards — each tracked separately. Software is necessary but needs clean source data first.",
        "final_angle": "场景落地型"
    },
    # 50 - CryptoTaxAtty - old universal basis vs new 2025 per-wallet basis
    {
        "url": "https://x.com/CryptoTaxAtty/status/1895263034437947679",
        "final_reply": "FIFO under universal basis could pick lower-cost lots from any wallet. Per-wallet FIFO uses only lots within that specific wallet — you may have higher-basis lots there, increasing your taxable gain on identical trades.",
        "final_angle": "反直觉观点型"
    },
    # 51 - khalidakbary - instructions on migrating from universal to per-wallet basis
    {
        "url": "https://x.com/khalidakbary/status/1876419812790022219",
        "final_reply": "Migration checklist: identify your 2024 method, confirm transition election per Rev. Proc. 2024-28, validate wallet-level basis is clean before any 2025 disposals. Filing deadline doesn't wait for reconciliation.",
        "final_angle": "场景落地型"
    },
    # 52 - Coin_Tracking - per-wallet tracking, 1099-DA debut, cost basis changes 2025
    {
        "url": "https://x.com/Coin_Tracking/status/1872659326541701613",
        "final_reply": "Three simultaneous 2025 changes: per-wallet basis, 1099-DA debut, broader broker reporting. When 1099-DA shows a sale and per-wallet tracking shows different cost basis, you must reconcile before filing.",
        "final_angle": "场景落地型"
    },
    # 53 - 21DogeLoge42 - 2025 per-wallet rules, 1099-DA, wash sale, stablecoins, NFTs
    {
        "url": "https://x.com/21DogeLoge42/status/1871287898815050077",
        "final_reply": "Per-wallet basis also matters for wash sale planning: if Congress extends wash sale to crypto, wallet-level records will determine which repurchases trigger disallowed loss carryforward.",
        "final_angle": "规则解读型"
    },
    # 54 - Bitcoinapolis55 - per-wallet rules don't affect 2024 taxes, only 2025 forward
    {
        "url": "https://x.com/Bitcoinapolis55/status/1871235342465896609",
        "final_reply": "Per-wallet + 1099-DA reconciliation + staking income events + DeFi swap tracking all compound. Each manageable alone; together they require crypto-specialized advisors, not generic tax prep.",
        "final_angle": "场景落地型"
    },
    # 55 - HughHipsDontLie - Rev Proc 2024-28 per-wallet mandatory 2025, user wants Trump to roll back
    {
        "url": "https://x.com/HughHipsDontLie/status/1870930523985776756",
        "final_reply": "The Rev. Proc. 2024-28 transition election was time-limited — due with your 2024 return. If you ignored it and missed it, you're bound by default lot allocation rules regardless of what comes next.",
        "final_angle": "规则解读型"
    },
    # 56 - tahoetax - wash sale still doesn't apply to BTC in 2025
    {
        "url": "https://x.com/tahoetax/status/2005697010670972974",
        "final_reply": "Wash sale exemption for crypto is intact in 2025 — sell BTC at a loss, repurchase immediately, loss is fully deductible. That window may close if pending bills advance; harvest this year if you intend to.",
        "final_angle": "场景落地型"
    },
    # 57 - ChadSlimeBased - buy BTC at 126k, drops to 89k, sell and rebuy, realize $37k loss
    {
        "url": "https://x.com/ChadSlimeBased/status/2002157695286087695",
        "final_reply": "Stocks need a 30-day wait; BTC has no wash sale equivalent. That asymmetry is real — the $37k loss is immediately deductible, and this gap is something institutional tax teams actively plan around.",
        "final_angle": "反直觉观点型"
    },
    # 58 - BitcoinHofmann - asking about Spain wash sale equivalent
    {
        "url": "https://x.com/BitcoinHofmann/status/2002375101623230892",
        "final_reply": "Spain's 2023 crypto rules have no direct wash sale equivalent, but anti-avoidance provisions may apply by analogy — consult a Spanish tax advisor before executing this strategy with Spanish-sourced income.",
        "final_angle": "规则解读型"
    },
    # 59 - Itstrev - confirming can sell crypto loss and rebuy same day
    {
        "url": "https://x.com/Itstrev/status/2002202881290641595",
        "final_reply": "Correct under 2025 US law: sell at a loss and repurchase immediately — no wash sale rule applies to crypto. Loss offsets capital gains or up to $3k/year of ordinary income with unlimited carryforward.",
        "final_angle": "规则解读型"
    },
    # 60 - Reducecryptotax - 2025 tax moves: TLH, self-custody, specific ID, Puerto Rico
    {
        "url": "https://x.com/Reducecryptotax/status/1992169121513918548",
        "final_reply": "Per-wallet basis, 1099-DA reporting, and broader broker rules took effect together in 2025 — each creates an audit trail that didn't exist before. Prior-year gaps are significantly harder to close now.",
        "final_angle": "规则解读型"
    },
    # 61 - JordanFreyMD - can you TLH with BTC if repurchase is substantially identical
    {
        "url": "https://x.com/JordanFreyMD/status/1975637889578115452",
        "final_reply": "IRS hasn't ruled BTC substantially identical to any other asset. Unlike index fund proxies, no BTC substitute triggers wash sale. Sell, hold cash, buy back — all currently legal with no 30-day restriction.",
        "final_angle": "规则解读型"
    },
    # 62 - countonsheep - 1099-DA missing cost basis creates phantom gains, audit risk
    {
        "url": "https://x.com/countonsheep/status/1948137952003096908",
        "final_reply": "Phantom gains from blank-basis 1099-DAs hit hardest on multi-platform traders. Exchange reports proceeds without basis; IRS has the proceeds number. Every mismatch risks a CP2000 letter.",
        "final_angle": "规则解读型"
    },
    # 63 - Empower_Capital - capital loss from dip can offset earlier gains
    {
        "url": "https://x.com/Empower_Capital/status/2034621374212260193",
        "final_reply": "Realized losses offset gains dollar-for-dollar with no cap. The $3k annual limit applies only to losses used against ordinary income when gains run out — most TLH scenarios aren't limited.",
        "final_angle": "场景落地型"
    },
    # 64 - MarketInsigh360 - using realized losses to offset capital gains
    {
        "url": "https://x.com/MarketInsigh360/status/2033796204400988235",
        "final_reply": "The $3k ordinary income offset per year is often under-planned. $20k in losses with no gains = 7-year runway. Pairing with intentional gain realization each year accelerates the benefit.",
        "final_angle": "场景落地型"
    },
    # 65 - CryptactGlobal - capital loss harvesting legal under CRA rules
    {
        "url": "https://x.com/CryptactGlobal/status/2028930131155136767",
        "final_reply": "Tax loss harvesting is legal under current US rules — execution matters. Sell before Dec 31, document cost basis. Losses realized now are safe from retroactive denial even if wash sale rules pass later.",
        "final_angle": "规则解读型"
    },
    # 66 - nelsonbarss - asking if there's a limit to how much you can write off against income
    {
        "url": "https://x.com/nelsonbarss/status/2023201738677965138",
        "final_reply": "No cap on losses offsetting capital gains — $1M in gains fully offset by $1M in crypto losses. The $3k/year limit applies only when you've run out of capital gains to offset. Unlimited carryforward otherwise.",
        "final_angle": "规则解读型"
    },
    # 67 - saylordocs - sell BTC at $88k, rebuy same second, realize $38k loss
    {
        "url": "https://x.com/saylordocs/status/2018748821954592816",
        "final_reply": "Stocks need a 30-day wait; crypto doesn't — that's the asymmetry. Crypto investors can execute the sale and rebuy simultaneously, managing both position exposure and tax liability in one step.",
        "final_angle": "反直觉观点型"
    },
    # 68 - the_tax_intern - Germany crypto: $4.5B realized losses, short-term losses vs long-term tax-free >1yr
    {
        "url": "https://x.com/the_tax_intern/status/2015712540508971256",
        "final_reply": "$4.5B in realized losses offsets $4.5B in capital gains with no cap. For any scale of operation, year-end TLH is standard portfolio management. The math is identical whether institutional or retail.",
        "final_angle": "场景落地型"
    },
    # 69 - DEFIRUSH_ - turn market dips into tax wins, crypto no wash sale, sell and rebuy immediately
    {
        "url": "https://x.com/DEFIRUSH_/status/2008595528939172024",
        "final_reply": "Tax loss harvesting is deferral, not elimination. Repurchasing immediately lowers your basis to $88k — when BTC recovers, you owe tax on that appreciation. The loss shifts timing, not the total amount owed.",
        "final_angle": "反直觉观点型"
    },
    # 70 - Tylerp270 - asking about wash sale laws for crypto vs stocks
    {
        "url": "https://x.com/Tylerp270/status/2006155686212751377",
        "final_reply": "Stocks: 30-day wash sale window disallows loss if repurchased within 30 days. Crypto: no such rule currently. Sell BTC at a loss, rebuy immediately — loss fully deductible. That gap is intentional for now.",
        "final_angle": "规则解读型"
    },
    # 71 - skumWgmi - same BTC buy at 126k drop to 88k sell rebuy realize 38k loss
    {
        "url": "https://x.com/skumWgmi/status/2005681330303164793",
        "final_reply": "What most miss: repurchased BTC basis resets to $88k. The $38k loss is a current-year deduction — but when BTC recovers to $126k, that gain is taxable. Loss harvesting defers, it doesn't eliminate.",
        "final_angle": "反直觉观点型"
    },
    # 72 - VJLvEekhout - year-end crypto dip explained by TLH, no wash sale, whales reload in January
    {
        "url": "https://x.com/VJLvEekhout/status/2005196890707578919",
        "final_reply": "Year-end TLH selling creates measurable Q4 price pressure as high-basis holders exit losers before Dec 31. For buyers, the window offers temporarily depressed prices while sellers realize their losses.",
        "final_angle": "场景落地型"
    },
    # 73 - 3orovik - summary of crypto TLH: property, $3k ordinary income offset, no wash sale 2025
    {
        "url": "https://x.com/3orovik/status/2004683515183628489",
        "final_reply": "Tax-loss offset isn't automatic — you must sell before Dec 31 and document cost basis. Holding a losing position through year-end creates no deduction. Plan in October, not December.",
        "final_angle": "场景落地型"
    },
    # 74 - garvkapur - asking max loss you can claim
    {
        "url": "https://x.com/garvkapur/status/2002654903806894438",
        "final_reply": "No maximum on losses offsetting capital gains — $1M in gains fully offset by $1M in losses. The $3k annual limit applies only to losses applied against ordinary income when you've run out of gains.",
        "final_angle": "规则解读型"
    },
    # 75 - SamLedger67 - DEX swap and DeFi yield events are taxable, 1099-DA coming
    {
        "url": "https://x.com/SamLedger67/status/2034498184110641315",
        "final_reply": "1099-DA covers broker-reported transactions — most DEX activity won't be on it in 2025. But every on-chain disposal is still a taxable event on Form 8949. No 1099-DA doesn't mean not taxable.",
        "final_angle": "规则解读型"
    },
    # 76 - SamLedger67 - DEX swaps won't be broker-reported but IRS is still watching
    {
        "url": "https://x.com/SamLedger67/status/2034135686824005788",
        "final_reply": "DEX transactions won't appear on 1099-DA, but IRS uses blockchain analytics to cross-reference on-chain activity with CEX KYC data. Self-reporting DEX gains now is far better than a reconstruction audit later.",
        "final_angle": "反直觉观点型"
    },
]

def main():
    with open('/Users/nightyoung/社媒运营工具/sector-radar/output/search_matches_v2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Build lookup by URL
    reply_map = {r['url']: r for r in REPLIES}

    over_220 = 0
    angle_counts = {"反直觉观点型": 0, "规则解读型": 0, "场景落地型": 0}
    matched_count = 0
    unmatched = []

    for record in data:
        url = record['tweet_url']
        if url in reply_map:
            r = reply_map[url]
            record['final_reply'] = r['final_reply']
            record['final_angle'] = r['final_angle']
            matched_count += 1
            char_len = len(r['final_reply'])
            if char_len > 220:
                over_220 += 1
                print(f"OVER 220 ({char_len}): {url}")
                print(f"  Reply: {r['final_reply']}")
            angle_counts[r['final_angle']] = angle_counts.get(r['final_angle'], 0) + 1
        else:
            unmatched.append(url)
            # Fallback: use existing new_reply if available
            if 'new_reply' in record:
                record['final_reply'] = record['new_reply']
                record['final_angle'] = record.get('new_reply_angle', '')
                print(f"UNMATCHED (using new_reply): {url}")
            else:
                record['final_reply'] = ""
                record['final_angle'] = ""
                print(f"UNMATCHED (no fallback): {url}")

    with open('/Users/nightyoung/社媒运营工具/sector-radar/output/search_matches_v3.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n=== 完成 ===")
    print(f"总条数: {len(data)}")
    print(f"匹配条数: {matched_count}")
    print(f"未匹配条数: {len(unmatched)}")
    print(f"超出220字符的条数: {over_220}")
    print(f"反直觉观点型: {angle_counts.get('反直觉观点型', 0)}")
    print(f"规则解读型: {angle_counts.get('规则解读型', 0)}")
    print(f"场景落地型: {angle_counts.get('场景落地型', 0)}")

    if unmatched:
        print(f"\n未匹配的URL:")
        for u in unmatched:
            print(f"  {u}")

if __name__ == '__main__':
    main()
