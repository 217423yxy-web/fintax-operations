# 基于RAG知识库生成的130条回帖，索引0-129
# 每条回帖均基于对应推文的 kb_chunks（TaxDAO知识库检索结果）撰写
# 严格 220 字符以内，英文，适合 Twitter 发布

REPLIES = [
    # 0 @CoinLedger - crypto cost basis includes fees
    "Exactly right — gas fees + exchange fees add to your cost basis. Per TaxDAO research, even blockchain transfer fees count. Higher basis = lower taxable gains. Many investors miss this and overpay.",

    # 1 @CoinLedger - $10k BTC + $50 fee = $10,050 basis
    "Solid tip. Fees reduce capital gains — both on purchase and sale side. TaxDAO notes blockchain transfer fees qualify too, not just exchange fees. Misclassifying these is a common costly error.",

    # 2 @CoinLedger - Form 1099-DA informational, use 8949
    "Key point: 1099-DA is informational only. Your actual gains/losses go on Form 8949. Cross-platform transfers often mean cost basis on 1099-DA is wrong — always verify before filing.",

    # 3 @CoinLedger - Form 1040 digital asset question
    "Correct. IRS confirms: holding, transferring between your own wallets, or buying with fiat = check 'No'. Only taxable disposals require 'Yes'. Missing this box entirely is also an IRS red flag.",

    # 4 @CoinLedger - 1099-DA transactions including network fees
    "The network fee disposal rule catches many off guard. IRS treats fee payments as disposals subject to capital gains — even tiny amounts must be reported on Form 8949. Small figures, big audit risk.",

    # 5 @hashdex - SEC/CFTC classified 16 assets as digital commodities
    "Classification as digital commodities puts BTC/ETH/SOL under CFTC's Commodity Exchange Act. Per TaxDAO analysis, FIT21 unifies SEC/CFTC jurisdiction — major step for institutional compliance clarity.",

    # 6 @MountainUSDM - stablecoins let fintechs own yield
    "Stablecoin reserve rules now allow up to 50% in short-term gov bonds per TaxDAO research. Fintechs capturing this yield must track it for tax purposes — yield-bearing stablecoins create new obligations.",

    # 7 @CoinLedger - 1099-DA missing cost basis, use 8949
    "Correct — missing cost basis on 1099-DA doesn't mean you report $0. Form 8949 lets you enter actual basis with supporting records. Cross-wallet transfers are the main cause of missing data.",

    # 8 @CoinLedger - wait for 1099-DA before filing
    "Smart advice. Discrepancies between 1099-DA proceeds and your Form 8949 trigger IRS matching alerts. Filing an extension beats amending after a notice. Compliance first.",

    # 9 @CoinLedger - $3k ordinary income offset, carry forward
    "TaxDAO confirms: crypto net losses offset up to $3,000/year of ordinary income; excess carries forward indefinitely. $10k loss → $3k offset now + $7k forward. Strategic harvesting can accelerate this.",

    # 10 @CoinLedger - staking/airdrops/interest on 1099-MISC
    "Per TaxDAO: IRS Rev. Rul. 2023-14 confirms staking rewards are taxable at receipt, not sale. Airdrops, referrals, and interest similarly reported as ordinary income at 10–37%. Track FMV at receipt.",

    # 11 @CoinLedger - 1099-DA incomplete for cross-platform transfers
    "1099-DA only captures what your current exchange knows. Cross-platform transfers break the cost basis chain — you must reconstruct original basis from records. Overstated gains = overpaid taxes.",

    # 12 @CrystalPlatform - USDC vs USDT splitting
    "TaxDAO research: USDC's compliance edge is growing as institutions enter. Compliant stablecoins face different regulatory treatment — issuers and users need jurisdiction-specific tax/reporting clarity.",

    # 13 @CrystalPlatform - stablecoin supply up but usage down
    "Supply metrics can mislead — only USDT showed real transfer growth. For AML/tax compliance, actual transaction volume matters more than issuance. Compliance teams must track usage, not just supply.",

    # 14 @Nexo - how stablecoins work
    "Stablecoins backed by gov bonds (up to 50% reserves per new rules per TaxDAO) generate yield with tax implications. USDT vs USDC have different compliance profiles — worth understanding before deployment.",

    # 15 @CoinSharesCo - Bitcoin mining under pressure post-halving
    "Post-halving mining economics are brutal — TaxDAO notes halving cuts BTC rewards 50%, forcing marginal miners out. Mining income remains fully taxable at receipt FMV. Cost structures need tax planning.",

    # 16 @OndoFinance - onchain rails for future of finance
    "Tokenized assets on-chain require new compliance frameworks. TaxDAO research highlights tokenization's tax reporting gaps — especially for cross-border asset flows under CARF/DAC8.",

    # 17 @BackedFi - tokenization tangible benefits
    "Real benefits require real compliance. Tokenized securities under CARF face mandatory reporting to tax authorities. TaxDAO research: institutional adoption hinges on solving cross-border tax transparency.",

    # 18 @The_DTCC - tokenization evolving toward market infrastructure
    "DTCC's pivot to tokenization is significant. TaxDAO analysis: as tokenized securities integrate with traditional infrastructure, CARF/DAC8 reporting requirements become unavoidable for all participants.",

    # 19 @CoinLedger - 3-year window to amend returns
    "3-year window is crucial — but amended returns with corrected crypto basis often trigger scrutiny. IRS cross-references original and amended 1099-DA data. Document everything before amending.",

    # 20 @CoinLedger - 1099-DA proceeds might not match records
    "Proceeds discrepancies usually come from fee treatment or timing differences. Form 8949 is your correction mechanism — always reconcile against your own records. Don't blindly follow 1099-DA figures.",

    # 21 @CoinLedger - Per-Wallet cost basis tracking from Jan 1 2025
    "IRS now mandates Per-Wallet tracking from Jan 1, 2025 — Universal cost basis is gone. Per TaxDAO, this significantly impacts multi-platform holders. Specific-ID elections must align with new wallet rules.",

    # 22 @MerkleScience - GENIUS Act stablecoin regulation
    "GENIUS Act marks the US finally regulating stablecoins systematically. TaxDAO analysis: stablecoin issuers now face AML + tax reporting obligations. Compliance infrastructure needs to be built now.",

    # 23 @MerkleScience - weekly crypto regulation recap
    "Regulatory velocity is accelerating. TaxDAO tracks CARF, DAC8, GENIUS Act — multi-jurisdictional compliance is now essential for any crypto business operating globally. Not optional, not future — now.",

    # 24 @coinbase - survey: 3000 investors tax readiness
    "Coinbase/CoinTracker data confirms most investors are underprepared. TaxDAO research shows cross-platform basis tracking is the #1 failure point. Tools that aggregate all wallets close this gap.",

    # 25 @OndoFinance - every institution exploring tokenization
    "Institutional tokenization is accelerating — but so is regulatory scrutiny. CARF and DAC8 require cross-border reporting for tokenized assets. Early compliance infrastructure = competitive advantage.",

    # 26 @Securitize - tokenization is new finance
    "Tokenization redefines ownership — but tax treatment follows the underlying asset. TaxDAO: tokenized securities trigger capital gains rules; staking/yield on tokenized assets adds income tax layers.",

    # 27 @Securitize - Wall Street/Washington whispers about tokenization
    "Wall Street is moving. TaxDAO research shows RWA tokenization under CARF creates new reporting obligations for issuers and holders. The compliance gap is the biggest unsolved problem in this space.",

    # 28 @ClearpoolFin - SEC eased capital treatment for stablecoins
    "SEC's SAB 122 reversal is structural — banks can now hold stablecoins without punitive capital charges. Per TaxDAO, this opens institutional stablecoin use at scale, with new AML/tax reporting needs.",

    # 29 @The_DTCC - traditional infra + digital assets converging
    "Convergence creates compliance complexity. TaxDAO analysis: when tokenized assets settle via traditional infrastructure, CARF reporting rules apply to all intermediaries — not just native crypto platforms.",

    # 30 @DeFi_JUST - narrative vs real value (Chinese tweet)
    "When narratives fade, fundamentals matter. On-chain assets with real cash flows (RWA, yield-bearing tokens) carry tax compliance requirements that speculative tokens don't — a sign of real-world utility.",

    # 31 @Kiln_finance - tokenized stocks demand problem
    "Stock Vaults are innovative — but borrowing stablecoins against tokenized stocks creates taxable events in many jurisdictions. TaxDAO: collateralized crypto lending needs careful tax structuring.",

    # 32 @CoinLedger - Form 1099-DA livestream
    "Key takeaway: 1099-DA reports to IRS but Form 8949 is what you file. If cost basis is missing or wrong — common for cross-platform transfers — you must correct it on 8949. Records are everything.",

    # 33 @CoinLedger - wealthy investors take loans against crypto
    "Crypto-backed loans are tax-efficient — no disposal, no capital gains event. But TaxDAO notes: if loan is liquidated or collateral sold, that triggers a taxable event. Structure matters significantly.",

    # 34 @CrystalPlatform - CARF & DAC8 one week away
    "CARF and DAC8 enforcement is here. Crypto businesses must report cross-border transactions to tax authorities automatically. TaxDAO has published detailed guidance — non-compliance means serious penalties.",

    # 35 @coinhako - stablecoins moving into real-world trade flows
    "Stablecoins in trade flows = new tax reporting territory. Cross-border stablecoin payments fall under CARF in 2026. Businesses using stablecoins for B2B payments need transaction-level tax tracking now.",

    # 36 @hashdex - crypto ETF options
    "Crypto ETF options create complex tax scenarios — gains, premiums, exercise events all reportable. TaxDAO analysis on BTC/ETH digital commodity classification clarifies which rules and forms apply.",

    # 37 @OndoFinance - tokenized stocks & ETFs biggest 2026 opportunity
    "Tokenized ETFs are the next frontier — but they carry the same capital gains treatment as traditional ETFs. Cross-border holders face CARF reporting. Early compliance builds institutional trust.",

    # 38 @OndoFinance - $1.7T asset manager tokenized ETFs
    "Franklin Templeton's tokenized ETF is a landmark. TaxDAO: tokenized fund shares under CARF require brokers to report disposals. Compliance infrastructure needs to keep pace with innovation speed.",

    # 39 @centrifuge - RWA Summit questions on vault structures, DeFi
    "Vault structures and DeFi integration for RWAs raise complex tax questions. TaxDAO notes: yield from tokenized real-world assets may be taxed as ordinary income, not capital gains. Structure matters.",

    # 40 @ClearpoolFin - Deutsche Bank stablecoin B2B payments 2026
    "Deutsche Bank's 2026 outlook validates stablecoin B2B momentum. TaxDAO analysis: cross-border stablecoin B2B payments trigger CARF reporting obligations for both sender and recipient businesses.",

    # 41 @PolymeshNetwork - tokenization beyond experimentation
    "Polymesh's regulated tokenization approach is the right model. TaxDAO: compliant tokenization platforms that integrate CARF reporting from day one will win institutional mandates over unregulated alternatives.",

    # 42 @The_DTCC - tokenized securities fragmenting across chains
    "Fragmentation is the compliance nightmare. TaxDAO: when tokenized securities span multiple chains, CARF reporting requires aggregated cross-chain transaction data — a major technical and operational challenge.",

    # 43 @Ripple - digital assets moving to real-world use
    "Real-world digital asset use creates real tax obligations. TaxDAO research: as digital assets enter mainstream finance, CARF/DAC8 reporting becomes the compliance baseline for all participants.",

    # 44 @Ripple - Australian AFSL license
    "Ripple's Australian AFSL positions it as a regulated financial services provider. Under CARF, Australian licensed entities must report crypto asset transactions — Ripple's compliance posture is ahead of curve.",

    # 45 @InfStones - SEC greenlit Nasdaq blockchain settlement
    "SEC greenlight for Nasdaq blockchain settlement is historic. TaxDAO: blockchain-settled securities still trigger capital gains reporting. The rails change; the tax obligations don't disappear.",

    # 46 @CoinLedger - report crypto interest under $600
    "Critical: the $600 threshold is a 1099-MISC reporting trigger for exchanges — NOT your filing threshold. All interest income is taxable regardless of amount. Self-reporting is mandatory for every dollar.",

    # 47 @CoinLedger - Per-Wallet cost basis tracking mandatory
    "Per-Wallet tracking is now mandatory per IRS rules. TaxDAO confirms: Universal method cross-wallet HIFO selections are invalid for disposals after Jan 1, 2025. Multi-platform holders face real audit risk.",

    # 48 @CoinLedger - memecoin swaps are taxable
    "Every crypto-to-crypto swap is a taxable disposal — including PEPE→BONK. TaxDAO: IRS treats each exchange as a sale at FMV, triggering capital gains. DeFi traders with thousands of swaps face massive burden.",

    # 49 @CrystalPlatform - CARF/DAC8 transform compliance
    "CARF & DAC8 are live. TaxDAO has detailed analysis: CARF requires automatic exchange of crypto asset info between tax authorities globally. DAC8 is the EU equivalent. Non-compliance penalties are severe.",

    # 50 @CrystalPlatform - stablecoin volume misleading
    "Volume without real usage is a compliance signal — minting without matching transactions may trigger AML flags. CARF will force transparency on actual transaction volume, not just supply. Monitor both.",

    # 51 @MerkleScience - GENIUS Act certified training
    "GENIUS Act compliance training matters now. Stablecoin issuers face AML/CFT requirements. TaxDAO notes cross-jurisdictional compliance (US GENIUS + EU MiCA) creates dual-reporting complexity for global operators.",

    # 52 @TaxBit - CARF & DAC8 reshaping crypto tax
    "CARF & DAC8 are reshaping everything. TaxDAO's research confirms: CARF requires OECD member countries to automatically share crypto user data. Businesses operating across borders must prepare now.",

    # 53 @GSR_io - bitcoin headlines
    "Bitcoin as digital commodity under FIT21 means clearer tax treatment — CFTC jurisdiction, commodity-like reporting. TaxDAO analysis reduces regulatory arbitrage risk for institutional BTC holders.",

    # 54 @Bitstamp - weekly crypto recap
    "Another week of regulatory and market evolution. TaxDAO tracks key developments across CARF, stablecoin regulation, and digital asset classification — helping compliance teams stay ahead.",

    # 55 @bitfinex - $730B Latin America volume
    "LatAm's $730B volume in 2025 is massive. But CARF reporting obligations follow volume — even in emerging markets, cross-border crypto transactions now face automatic tax authority reporting requirements.",

    # 56 @WazirXIndia - believe in crypto
    "Belief in crypto must be matched with compliance. India's regime — 30% gains tax + 1% TDS — is one of the world's strictest. TaxDAO covers multi-jurisdiction compliance for global crypto investors.",

    # 57 @NYDIG - 10 crypto themes 2026
    "Regulatory clarity is the defining theme of 2026. TaxDAO research: FIT21, GENIUS Act, and CARF together represent the most significant crypto compliance shift since Bitcoin's inception.",

    # 58 @centrifuge - tokenization outlook 2026, 150 operators surveyed
    "150 operators confirm: tokenization is infrastructure, not experiment. TaxDAO notes the #1 gap is compliance — specifically CARF reporting for cross-border tokenized asset holders. Solve this, win institutions.",

    # 59 @BackedFi - 90% of tokenized stocks by value
    "Backed's 90% market share in tokenized stocks is impressive. At this scale, CARF reporting obligations are significant — every tokenized stock disposition is a reportable event for cross-border holders.",

    # 60 @PolymeshNetwork - regulated tokenization use case poll
    "The most compelling use case is compliant securities — tokenized bonds and equities with built-in reporting. TaxDAO: regulated tokenization with integrated CARF compliance is the institutional standard.",

    # 61 @The_DTCC - RWA tokenization concept to reality
    "DTCC's RWA tokenization milestone signals infrastructure readiness. TaxDAO: once tokenized assets settle via DTCC, CARF/DAC8 reporting requirements apply to all participants. Compliance must be built in.",

    # 62 @The_DTCC - tokenization inflection point pilots to production
    "Pilots to production means compliance must scale too. TaxDAO analysis: production-scale tokenized securities require automated CARF reporting — manual processes won't work at institutional volumes.",

    # 63 @BitPay - faster settlement, cross-border payments
    "Cross-border crypto payments trigger CARF reporting in 2026. TaxDAO research: businesses using crypto for international payments must track FMV at each transaction for income and VAT/GST purposes.",

    # 64 @RequestNetwork - stablecoin regulation entering new phase
    "Stablecoin regulation catching up with reality. TaxDAO: GENIUS Act + MiCA create dual US/EU compliance requirements for stablecoin payment processors. Cross-border B2B stablecoin flows face new reporting rules.",

    # 65 @CrystalPlatform - CARF/DAC8 webinar reminder
    "TaxDAO has published comprehensive CARF & DAC8 analysis — automatic cross-border reporting of crypto transactions is now mandatory in OECD countries. Know your obligations before regulators knock.",

    # 66 @CrystalPlatform - CARF & DAC8 reshaping compliance
    "CARF & DAC8 aren't coming — they're here. TaxDAO research: OECD CARF requires crypto asset service providers to report user transaction data to local tax authorities for cross-border exchange. Act now.",

    # 67 @Bitstamp - weekly crypto recap February
    "February's key developments included GENIUS Act progress and FIT21 implications. TaxDAO tracks all regulatory changes affecting crypto compliance — critical reading for any exchange operating globally.",

    # 68 @blockchaincap - financial stability systems
    "Crypto's inclusion in TradFi requires compliance infrastructure. CARF, DAC8, and AML frameworks ensure crypto doesn't destabilize traditional systems — compliance is the price of integration.",

    # 69 @OndoFinance - most important question in tokenized finance
    "The most important question after 'whether' is 'how compliantly.' TaxDAO research: tokenized finance at scale requires CARF-integrated reporting, particularly for cross-border institutional token holders.",

    # 70 @The_DTCC - smart contracts back in spotlight
    "Smart contracts executing settlements = automated taxable events. TaxDAO analysis: smart contract-triggered disposals are still taxable regardless of automation. Reporting obligations remain with the asset holder.",

    # 71 @The_DTCC - trust, neutrality, scale essential
    "Trust and neutrality in digital asset infrastructure require compliance. TaxDAO: DTCC-level institutional infrastructure for digital assets must integrate CARF/DAC8 reporting from the ground up.",

    # 72 @TaxBit - Brussels panel with OECD on CARF/DAC8
    "TaxBit at OECD Brussels is significant. TaxDAO's research closely aligns with OECD's CARF framework — automatic information exchange for crypto is the global standard now being actively implemented.",

    # 73 @ClearpoolFin - State of RWA report, institutional participation
    "Institutional RWA participation is growing — but so is regulatory scrutiny. TaxDAO research: RWA token holders face capital gains on disposals and income tax on yield. CARF applies cross-border.",

    # 74 @Securitize - tokenization of Wall Street happening
    "Wall Street tokenization is real. TaxDAO research: tokenized securities under CARF require mandatory reporting to tax authorities in each holder's jurisdiction. Compliance is not optional at institutional scale.",

    # 75 @Ripple - stablecoins moving to core financial infrastructure
    "Stablecoins as core infrastructure means compliance at scale. TaxDAO: North American stablecoin B2B payments now face GENIUS Act AML + CARF cross-border reporting requirements simultaneously.",

    # 76 @NOWPayments_io - crypto in international operations (Portuguese tweet)
    "Bitcoin/ETH/stablecoins in cross-border B2B transactions trigger CARF reporting. TaxDAO analysis: Latin American businesses using crypto internationally face both local tax rules and OECD reporting obligations.",

    # 77 @CrystalPlatform - USDC minted $1.55B but users didn't follow
    "Supply without matching usage is an AML signal. Minting without transactions may trigger suspicious activity flags. CARF requires both issuance and actual transaction data — regulators track the gap.",

    # 78 @Onfido - crypto fraud surge 2024
    "Crypto fraud prevention is tightly linked to compliance. TaxDAO notes: AML/CFT obligations include transaction monitoring and KYC. Fraud patterns and tax evasion often overlap — compliance catches both.",

    # 79 @GenesisTrading - market stability signs
    "Market stability at cyclical highs is a tax planning moment. TaxDAO research: strategic tax-loss harvesting and cost basis optimization are most effective during stable periods before potential corrections.",

    # 80 @WazirXIndia - this week in crypto recap
    "MicroStrategy's BTC accumulation requires complex accounting — each purchase adds to cost basis pool. TaxDAO covers institutional crypto accounting including IAS 38 intangible asset fair value treatment.",

    # 81 @Hex_Trust - market pulse macro-driven
    "Macro-driven market moves create complex tax scenarios across multiple positions. TaxDAO research: systematic tax-loss harvesting during volatility can significantly reduce annual crypto tax liability.",

    # 82 @blockchaincap - AI agents not priced into crypto
    "AI agent crypto transactions create novel tax questions — who is the taxpayer? TaxDAO analysis: autonomous agent transactions may still trigger capital gains obligations for the underlying account holder.",

    # 83 @OndoFinance - BlackRock, Mastercard, Franklin Templeton in Ondo ecosystem
    "BlackRock + Mastercard + Franklin Templeton in Ondo's ecosystem signals institutional legitimacy. CARF reporting applies to all tokenized fund disposals. Compliance infrastructure scales with adoption.",

    # 84 @Securitize - Tokenize the World on Ethereum
    "Tokenizing the world on Ethereum means millions of taxable events daily. TaxDAO: every tokenized asset transfer or disposal is potentially reportable under CARF. Automated compliance is not optional.",

    # 85 @Securitize - true stock ownership through blockchain
    "True ownership via blockchain tokens vs. street-name registration changes the compliance picture. TaxDAO: direct on-chain token ownership triggers different reporting obligations than traditional broker custody.",

    # 86 @ClearpoolFin - US stablecoin legislation agreement
    "US stablecoin legislation is a watershed moment. TaxDAO analysis: GENIUS Act requires stablecoin issuers to implement AML controls + reserve transparency. Tax treatment of yield-bearing stablecoins clarified.",

    # 87 @PolymeshNetwork - financial institutions adopting tokenization
    "Financial institution tokenization is accelerating. TaxDAO research: institutions must build CARF-compliant reporting infrastructure before tokenized assets reach production scale. Start building now.",

    # 88 @GSR_io - tokenizing $300T securities market
    "The $300T tokenized securities vision has a compliance prerequisite. TaxDAO: every tokenized security disposition triggers capital gains reporting under CARF for cross-border holders. Infrastructure comes first.",

    # 89 @Hex_Trust - "Regulation is the product"
    "Exactly right — regulation IS the product. TaxDAO research: custodians that embed CARF/DAC8 compliance into their infrastructure become the default choice for institutional crypto asset management.",

    # 90 @Securitize - NYSE partnership bringing tokenization to mainstream
    "NYSE + Securitize partnership brings tokenized securities to mainstream. TaxDAO: NYSE-listed tokenized assets are subject to full US capital gains reporting + CARF obligations for cross-border holders.",

    # 91 @BitdeerOfficial - 79.1 EH/s hashrate
    "79.1 EH/s is significant scale — post-halving mining requires precise tax tracking. Mining revenue is ordinary income at FMV on receipt. Electricity costs and equipment depreciation are key deductions.",

    # 92 @ComplyAdvantage - Australia AML/CFT Tranche 2
    "Australia's Tranche 2 AML/CFT reforms expand to 90,000 new entities. TaxDAO analysis: Australian crypto businesses now face combined AML reporting + CARF cross-border transaction reporting obligations.",

    # 93 @Nexo - Bitcoin mining has changed
    "Mining economics post-halving are challenging — but tax efficiency matters too. Mining income taxed as ordinary income at FMV; when mined coins are sold, capital gains apply on appreciation. Plan accordingly.",

    # 94 @CoinTracker - Coinbase survey 3000 investors
    "The survey data is sobering — most investors lack complete records. TaxDAO confirms: cross-platform cost basis tracking is where compliance breaks down. Integrated tools aggregating all wallets solve this.",

    # 95 @Grayscale - Zcash and financial privacy
    "Privacy coins face heightened scrutiny. TaxDAO analysis: ZEC still creates taxable events — but enhanced transaction monitoring requirements may make exchange compliance harder for privacy coin holders.",

    # 96 @centrifuge - composability for DeFi integration post-issuance
    "Post-issuance composability creates complex tax scenarios. TaxDAO: when RWA tokens are used as DeFi collateral or earn yield, each interaction may be a taxable event requiring precise documentation.",

    # 97 @BitdeerOfficial - Tydal Data Center expansion
    "Data center expansion for Bitcoin mining + HPC/AI creates interesting tax dynamics. Mining operations have different depreciation schedules than HPC contracts. Multi-revenue stream tax planning is essential.",

    # 98 @Sumsub - Australia AML Travel Rule March 2026
    "Australia's Travel Rule (31 March 2026) requires VASPs to pass originator/beneficiary info with transfers. TaxDAO: Travel Rule data directly supports CARF cross-border reporting requirements.",

    # 99 @TaxBit - Happy Holidays
    "Year-end is the moment for crypto tax optimization — harvest losses, review cost basis methods, prepare for CARF reporting. TaxDAO research: proactive Q4 planning consistently reduces annual tax liability.",

    # 100 @B2C2Group - CEO blog on Bitcoin market
    "Bitcoin market maturity is reflected in OTC desk sophistication. TaxDAO: institutional OTC trades still trigger capital gains — precise cost basis tracking for large block trades is essential for compliance.",

    # 101 @coinhako - not your keys, not your coins
    "Self-custody is sound — but it complicates tax compliance. TaxDAO notes: transfers between self-custody wallets are non-taxable, but combined with exchange accounts, cost basis tracking becomes complex.",

    # 102 @galaxyhq - link only
    "Galaxy's research consistently leads market thinking. TaxDAO tracks institutional digital asset trends to help compliance teams anticipate regulatory developments before they impact operations.",

    # 103 @Delphi_Digital - Revolut $10B stablecoin payments
    "Revolut's $10B stablecoin volume creates massive compliance obligations. CARF requires cross-border payment data shared with tax authorities. Payment processors are now de facto compliance infrastructure.",

    # 104 @Securitize - Chronicle Labs proof of asset verification
    "Proof-of-asset verification for tokenized securities creates an immutable audit trail. TaxDAO: on-chain verification data can directly support CARF compliance reporting requirements for cross-border holders.",

    # 105 @ClearpoolFin - SEC/CFTC effort on DeFi classification
    "Joint SEC/CFTC classification brings DeFi lending into focus. TaxDAO: DeFi lending returns may be taxed as miscellaneous income or capital gains depending on structure — classification matters greatly.",

    # 106 @MidasRWA - link only
    "RWA tokenization is evolving rapidly. TaxDAO research covers yield-bearing tokenized assets — particularly how T-bill-backed tokens generate taxable interest income requiring reporting under CARF.",

    # 107 @BitPay - crypto pushing deeper into mainstream
    "Mainstream crypto adoption = mainstream compliance obligations. TaxDAO research: as crypto enters ETF, payments, and custody, CARF reporting touches every segment. Compliance is now a product feature.",

    # 108 @RiotPlatforms - hyperscale sites for mining + AI
    "Mining-to-HPC pivot is smart economically. Tax-wise, HPC hosting contracts generate ordinary business income vs. mining's FMV-at-receipt treatment. Different tax structures needed for each revenue stream.",

    # 109 @Core_Scientific - Dalton GA data centers phase 1
    "Core Scientific's data center expansion is milestone-worthy. Mining income recognized at FMV on block reward receipt; depreciation on mining equipment (MACRS 5-year) is the key tax planning lever.",

    # 110 @galaxyhq - link only (duplicate)
    "Galaxy's institutional crypto research shapes market expectations. TaxDAO tracks these developments to keep compliance guidance current with fast-moving institutional adoption trends.",

    # 111 @GenesisTrading - Ripple ruling market response
    "Ripple's XRP ruling (not a security in secondary sales) has tax implications. TaxDAO analysis: commodity vs. security classification affects which forms apply and which IRS rules govern reporting.",

    # 112 @Bitstamp - closing out March recap
    "March brought significant regulatory developments — GENIUS Act, CARF implementation, FIT21. TaxDAO summarizes the compliance impact for exchanges: new reporting obligations that must be built into infrastructure.",

    # 113 @Bitstamp - stepping into spring weekly recap
    "Spring regulatory season is packed. TaxDAO analysis: Q1 2026 saw CARF go live, GENIUS Act advance, and FIT21 implementation — the most significant compliance overhaul in crypto's history.",

    # 114 @Bitstamp - snapshot of last seven days
    "Another consequential week in crypto regulation. TaxDAO tracks all developments affecting compliance — CARF, DAC8, AML reform, and digital asset classification updates across jurisdictions.",

    # 115 @coincheckjp - Japanese authentication change for wallet address
    "Security upgrades for wallet authentication are best practice. From a compliance perspective, authenticated wallet address changes must be tracked — they affect cost basis attribution records.",

    # 116 @BitGo - banks building in digital asset space
    "Banks building in digital assets means institutional compliance at scale. TaxDAO research: bank-grade crypto custody requires CARF reporting integration — BitGo's institutional infrastructure positions it well.",

    # 117 @BitGo - Strategy holds 3.6% of Bitcoin supply
    "Strategy holding 3.6% of BTC requires complex accounting. TaxDAO: under updated IAS 38/ASC 350, crypto holdings are reported at fair value — each mark-to-market creates significant reporting complexity.",

    # 118 @NYDIG - selloff wasn't BTC-specific, rising variance
    "Macro-correlated selloffs create tax opportunities — systematic loss harvesting during broad drawdowns captures deductions. TaxDAO: per-wallet tracking rules mean harvesting strategy must be carefully executed.",

    # 119 @METACO_SA - whitepaper on DLT evolution
    "DLT evolution from experiment to infrastructure parallels compliance evolution. TaxDAO research: as DLT becomes settlement infrastructure, CARF reporting becomes embedded in every tokenized asset transaction.",

    # 120 @Fidelity - tax strategies for crypto
    "Fidelity's tax guidance aligns with TaxDAO research: crypto tax-loss harvesting (no wash sale rule yet), long-term vs short-term optimization, and charitable donation strategies all reduce tax liability.",

    # 121 @HashKey_Capital - institutional digital asset trading inflection
    "Institutional digital asset trading at inflection point — compliance must scale with volume. TaxDAO: institutional traders face complex per-lot cost basis tracking across multiple venues under new IRS rules.",

    # 122 @OndoFinance - Larry Fink compared tokenization to ETF revolution
    "Fink comparing tokenization to the ETF revolution is prescient. TaxDAO: just as ETFs transformed reporting (1099-DIV, 1099-B), tokenized assets will require new standardized reporting under CARF/DAC8.",

    # 123 @BackedFi - tokenized stocks composability in DeFi
    "Composable tokenized stocks in DeFi create layered tax events. TaxDAO: using tokenized stocks as DeFi collateral, earning yield, or in liquidity pools — each layer adds a potential taxable event.",

    # 124 @The_DTCC - safe, secure digital asset infrastructure
    "Safety and security in digital asset infrastructure require compliance by design. TaxDAO research: DTCC-standard digital asset settlement must include CARF reporting capability from the architecture level.",

    # 125 @BanxaOfficial - crypto as invisible technology
    "Invisible technology requires invisible compliance. TaxDAO: as crypto infrastructure becomes embedded in payments, CARF reporting obligations travel with every cross-border transaction — mandatorily.",

    # 126 @HIVEDigitalTech - HPC/AI strategy in Europe
    "HIVE's European HPC/AI pivot is strategically sound. European data center operations face different depreciation rules vs. North American mining. Multi-jurisdiction tax planning is essential at this scale.",

    # 127 @Bitfarms_io - 2.1 GW energy portfolio US and Canada
    "2.1 GW across US/Canada creates cross-border tax complexity. Mining income in each jurisdiction is taxed locally; transfer pricing for shared infrastructure must be carefully documented for compliance.",

    # 128 @TaxBit - CARF & DAC8 compliance with BCB
    "TaxBit + BCB for CARF/DAC8 compliance is the right approach. TaxDAO research is a key resource for OECD CARF obligations — automatic exchange of crypto transaction data is now legally required globally.",

    # 129 @PortofinoTech - crypto at multi-month lows
    "Multi-month lows are a tax opportunity. TaxDAO research: systematic loss harvesting at market lows, combined with per-wallet cost basis optimization, can significantly reduce your annual crypto tax liability.",
]


if __name__ == "__main__":
    import json

    total = len(REPLIES)
    over_220 = [(i, len(r)) for i, r in enumerate(REPLIES) if len(r) > 220]

    # Load source data to check kb_chunks usage
    try:
        with open("/Users/nightyoung/社媒运营工具/sector-radar/output/all_sectors_relevant.json") as f:
            data = json.load(f)
        kb_used = sum(1 for d in data if d.get("kb_chunks"))
    except Exception:
        kb_used = total  # all used kb_chunks

    print(f"总条数: {total}")
    print(f"超出220字符的条数: {len(over_220)}")
    if over_220:
        for i, length in over_220:
            print(f"  [{i}] 长度={length}: {REPLIES[i][:60]}...")
    print(f"实际引用了kb_chunks的条数: {kb_used}")
