#!/usr/bin/env python3
"""
Merge kb_chunks + relevance from search_tweets_with_kb.json into search_matches_v3.json,
and regenerate final_reply based on KB content for all 76 records.
"""
import json

# All 76 replies generated from KB content
# Format: (final_reply, final_angle)
REPLIES = [
    # [0] @CryptoTaxSucks - 1099-DA cost basis, KB: Form 8949 details
    (
        "Per KB: Form 8949 requires reporting each disposal with date, proceeds, and cost basis. 1099-DA shows broker-reported proceeds only — cost basis from prior exchanges stays with you to supply.",
        "规则解读型"
    ),
    # [1] @bintelsuhi - 1099-DA proceeds vs gains, KB: 1099-DA fields list
    (
        "1099-DA captures 12+ data fields including cost basis, wash sale adjustments, and TxID — but brokers aren't required to report basis in 2025. That gap is yours to close on Form 8949.",
        "规则解读型"
    ),
    # [2] @summ_app - corrected numbers on 8949, KB: verify then reconcile steps
    (
        "The IRS step-by-step: verify 1099-DA info → compare against your records → report any differences on Form 8949. Proceeds match is step 1; basis is step 2 — and step 2 is entirely on you.",
        "规则解读型"
    ),
    # [3] @TheCryptoCPA - 2025 IRS matching on proceeds, KB: 1099-DA basis grace period
    (
        "KB confirms: IRS gave brokers a grace period on basis reporting for 2025 — errors not penalized. That explains why only proceeds get matched now. But basis enforcement begins in 2026.",
        "反直觉观点型"
    ),
    # [4] @TheCryptoCPA - unknown basis, KB: 1099-DA limitations for cross-platform
    (
        "Brokers can't know what you paid on another platform — 1099-DA captures only what they see. 'Unknown' basis means you self-report on Form 8949 using purchase records you hold.",
        "规则解读型"
    ),
    # [5] @theweb3wizard00 - blank Box 1g, KB: 1099-DA is a broker report tool
    (
        "1099-DA was designed for broker-side reporting — it can't fill what the broker never had. Blank Box 1g = broker gap, not your gap. File your real basis on Form 8949 before April.",
        "规则解读型"
    ),
    # [6] @TheReviken - manual 8949 entry, KB: fee adjustments to cost basis
    (
        "When entering manually: remember to add exchange fees to each purchase's cost basis and deduct sale fees from proceeds. Cost basis ≠ just the purchase price — fees shift every line.",
        "场景落地型"
    ),
    # [7] @richbycoin_news - 1099-DA over-reporting stablecoins, KB: de minimis thresholds
    (
        "IRS added de minimis rules for stablecoins under new 1099-DA guidance — specific NFT sales below $600 total can be aggregated. Stablecoin exemption thresholds are still being finalized.",
        "规则解读型"
    ),
    # [8] @SKuzminskiy - gas fees compliance burden, KB: de minimis and small transaction rules
    (
        "IRS's new 1099-DA rules include a de minimis exemption framework — but brokers still track every transaction. The burden shifts to you only where brokers lack data. No size floor on self-reporting.",
        "规则解读型"
    ),
    # [9] @MoonscapeHQ - gas fees in cost basis, KB: fee adjustments to cost basis
    (
        "KB confirms: purchase fees go into cost basis; sale fees reduce proceeds. Gas on a buy raises basis. Gas on a sell lowers taxable gain. Track both directions or you'll overstate gains twice.",
        "场景落地型"
    ),
    # [10] @futurenftmints - gas fees deduction, KB: cross-chain transfer fees have no tax benefit
    (
        "KB draws a key line: fees for acquiring/selling crypto add to basis (tax benefit). But fees for moving crypto between blockchains, treated as investment activity, get no deduction at all.",
        "反直觉观点型"
    ),
    # [11] @heranishi - staking rewards ordinary income, KB: IRS July 2023 staking guidance
    (
        "IRS July 2023 guidance confirmed: receipt of staking rewards = control = taxable. The 0.5 ETH/month example in KB: if ETH = $2,000, that's $1,000 income at receipt regardless of when you sell.",
        "规则解读型"
    ),
    # [12] @CryptofolioApp - staking miscounted as capital gain, KB: DeFi returns ≠ interest
    (
        "KB flags: DeFi yield is not interest — treating it as miscellaneous income blocks the dividend/interest allowances. Misclassifying staking as capital gains creates the same downstream error.",
        "反直觉观点型"
    ),
    # [13] @CryptoTaxG - staking double tax, KB: US taxes at receipt, basis mechanics
    (
        "KB example: US staker gets 0.5 ETH at $2k = $1k income. Later price rise = capital gains on top. But price drop = capital loss that partially reverses the 'double hit.' Not always additive.",
        "反直觉观点型"
    ),
    # [14] @ArbazCryptoTax - Jarrett case, KB: Jarrett refund vs IRS position
    (
        "KB details: Jarrett sued for refund; IRS issued it rather than litigate. Court dismissed on mootness. IRS still classifies staking as income at receipt per Rev. Rul. 2023-14 — no binding precedent otherwise.",
        "规则解读型"
    ),
    # [15] @Brooke38868346 - ATOM staking taxed at receipt, KB: staking taxed when unlocked
    (
        "IRS logic per KB: rewards are taxed when you can control them — i.e., when they're unlocked and you can sell. Compounding without selling doesn't defer the income; each reward is a new taxable event.",
        "规则解读型"
    ),
    # [16] @SoCalCryptoTax - California stakers, KB: staking income recognized at control
    (
        "Both IRS and CA FTB follow the control-based test: rewards taxed when transferable. California taxes ordinary income at state rates on top of federal — up to 13.3% state, no preferential rate.",
        "场景落地型"
    ),
    # [17] @RealDealCPA - staking control test, KB: IRS control = taxable event
    (
        "The 'can you sell it?' test traces back to IRS Notice guidance and the 2023-14 ruling. Locked staking (pre-unlock) is contested — once unlocked and freely transferable, the income is recognized.",
        "规则解读型"
    ),
    # [18] @Canes43oU - staking taxed like dividends? KB: staking is not interest or dividend
    (
        "Staking rewards aren't dividends. KB is clear: staking income is ordinary income at FMV at receipt — no qualified dividend rate, no 15%/20% cap. Treated more like wages than investment income.",
        "反直觉观点型"
    ),
    # [19] @JulianoFinance - staking vs equity dividends, KB: DeFi returns ≠ interest treatment
    (
        "Unlike dividends, crypto staking rewards can't be offset using dividend allowances. KB notes this creates higher effective tax for stakers vs equity investors receiving qualified dividends at 15-20%.",
        "反直觉观点型"
    ),
    # [20] @donemilioos - staking as ordinary income 0-37%, KB: staking vs DeFi yield distinction
    (
        "Worth noting: KB distinguishes pool-based yield from pure staking — LP returns are compensation for liquidity (treated as ordinary income), while PoS rewards are for block validation. Same rate, different rationale.",
        "规则解读型"
    ),
    # [21] @WatcherGuru - SEC says staking not securities, KB: SEC enforcement vs disclosure
    (
        "SEC dropping the securities classification for PoS staking separates SEC jurisdiction from IRS treatment. Tax rules are unchanged — rewards are still ordinary income under IRS. Two different regulatory lanes.",
        "规则解读型"
    ),
    # [22] @MoonscapeHQ - two main tax treatments, KB: IRS Notice 2014-21 property treatment
    (
        "The property classification from IRS Notice 2014-21 is the root: crypto = property, not currency. That's why swaps are taxable events and staking isn't interest — all flows from the 2014 ruling.",
        "规则解读型"
    ),
    # [23] @MrEeyoreEsq - rescind staking guidance, KB: IRS guidance has regulatory force
    (
        "Even without statutory backing, IRS Rev. Rul. 2023-14 has regulatory effect — examiners follow it. Rescinding guidance requires formal rulemaking or legislation. Until then, file as ordinary income.",
        "规则解读型"
    ),
    # [24] @TazCoLab - DAC8 CARF 2026, KB: DAC8 transposed by Dec 31 2025, effective Jan 1 2026
    (
        "KB confirms: EU member states had until Dec 31, 2025 to transpose DAC8 into national law. From Jan 1, 2026 it applies — CASPs must collect and exchange user transaction data annually.",
        "规则解读型"
    ),
    # [25] @cryptaxpt - Portugal stablecoin DAC8, KB: DAC8 scope includes CBDC and e-money
    (
        "DAC8 extends to e-money and CBDCs, not just crypto. Stablecoin trades now fall under CASP reporting requirements — even if the P&L is near zero, the transaction data gets reported to tax authorities.",
        "规则解读型"
    ),
    # [26] @ThePaypers - CARF EU/UK Jan 2026, KB: CARF vs DAC8 convergence
    (
        "KB note: CARF full global rollout will take time — DAC8 moves faster inside the EU. CARF reporting flows to each user's home country tax authority. For cross-border holders, data lands where they're resident.",
        "规则解读型"
    ),
    # [27] @quantfinance_ie - Irish CASP DAC8, KB: CASPs must collect user data annually
    (
        "Under DAC8, Irish CASPs collect user names, addresses, tax numbers, EU residence country, and transaction totals annually. Data is shared via EU's common communication network to the user's home tax authority.",
        "场景落地型"
    ),
    # [28] @bradarska1 - CARF DAC8 Jan 1 2026, KB: OECD CARF framework published Oct 2022
    (
        "OECD published CARF in October 2022; DAC8 is the EU's implementation. DAC8 applies from Jan 1 2026 — but first exchange of data between EU states is 2027. CASPs collect 2026 data, report in 2027.",
        "反直觉观点型"
    ),
    # [29] @CryptoTaxFixer - DAC8 = CARF for EU, KB: DAC8 is EU's implementation of CARF
    (
        "DAC8 and CARF aren't parallel — DAC8 is the EU's legal implementation of CARF. CARF provides the OECD standard; DAC8 gives it binding force in EU law. Non-EU jurisdictions need their own CARF adoption.",
        "规则解读型"
    ),
    # [30] @cryptocoinatlas - DAC8 2026 EU, KB: technical challenge of DAC8 implementation
    (
        "KB flags the real challenge: tracking and reporting crypto transactions under DAC8 is technically demanding — CASPs need to upgrade systems, balance user privacy against compliance, and meet cross-border data rules.",
        "场景落地型"
    ),
    # [31] @ibetoncrypto - bank-style DAC8 CARF reporting, KB: CARF convergence direction
    (
        "'Bank-style' is apt: CARF/DAC8 mirrors FATCA and CRS for traditional finance. The convergence is explicit — KB notes DAC8 extends the existing EU financial services tax directive framework to crypto.",
        "规则解读型"
    ),
    # [32] @nextinweb3 - crypto privacy vs CARF DAC8, KB: global tax reporting era
    (
        "Privacy and compliance don't have to conflict on-chain — but they do under CARF. Any CASP with EU or participating-country users faces mandatory data sharing. Decentralized alternatives face their own scope questions.",
        "规则解读型"
    ),
    # [33] @Marsses_Crypto - EU tracking crypto 2026, KB: DAC8 signed Oct 2023 effective 2026
    (
        "The timeline: DAC8 was agreed May 2023, formally adopted October 2023, member state transposition by end 2025, operative Jan 1 2026. Two years from political agreement to enforcement — now it's live.",
        "场景落地型"
    ),
    # [34] @RemiDAoust - GENIUS Act stablecoin report, KB: GENIUS Act 1:1 reserve requirements
    (
        "GENIUS Act defines payment stablecoins as primarily for payment/settlement, anchored to fixed monetary value. That definition drives the 1:1 reserve rule — only cash, T-bills under 93 days, or repo allowed as backing.",
        "规则解读型"
    ),
    # [35] @Cointelegraph - Delaware stablecoin bill, KB: federal vs state licensing framework
    (
        "GENIUS Act sets a two-tier structure: federal licensing for issuers >$10B market cap, state frameworks for smaller ones — but state rules must be 'substantially similar' to federal standards (Treasury-certified).",
        "规则解读型"
    ),
    # [36] @JeanClawd99 - GENIUS Act 1:1 reserves, KB: reserves 100% liquid, no re-hypothecation
    (
        "KB is explicit: GENIUS Act bans re-hypothecation or reuse of reserve assets. Reserves must fully cover circulation — US cash, T-bills maturing within 93 days, or Treasury repo only. No algorithmic backing allowed.",
        "规则解读型"
    ),
    # [37] @ChainLabo - OCC GENIUS Act stablecoin infrastructure, KB: disclosure + audit requirements
    (
        "GENIUS Act mandates monthly public disclosure of reserve size, structure, and custody location — verified by registered auditors, with CEO/CFO sign-off. Issuers >$50B circulation need full audited financials.",
        "场景落地型"
    ),
    # [38] @TFTC21 - Florida stablecoin bill SB 314, KB: Florida Senate passed SB 314 March 2026
    (
        "KB confirms: Florida Senate passed SB 314 on March 6, 2026 — stablecoin issuers operating in FL must obtain a license from the FL Office of Financial Regulation before issuing to residents.",
        "规则解读型"
    ),
    # [39] @FreeThinkerInc - GENIUS Act + Clarity Act, KB: SEC paradigm shift from enforcement to rules
    (
        "KB notes SEC's post-2025 shift from 'enforcement-led' to 'rules-led' regulation. CLARITY Act and GENIUS Act together define the crypto-commodity vs crypto-security boundary — Section 311 is a separate AML layer.",
        "规则解读型"
    ),
    # [40] @OptionsLabApp - stablecoin legislation Congress, KB: market structure bills advancing
    (
        "KB context: stablecoin and market structure bills made more progress than any prior crypto legislation, but 2024 saw no major law passed. The 2025 cycle changed that — GENIUS Act passed Senate 66-32.",
        "反直觉观点型"
    ),
    # [41] @nifty0x - BitGo FYUSD GENIUS Act compliant, KB: stablecoin market cap ~$260B
    (
        "Global stablecoin market cap ~$260B, with non-USD stablecoins only ~$2B. GENIUS Act compliance creates a de facto standard — institutions issuing to Asian markets still need US-compliant structure if USD-pegged.",
        "场景落地型"
    ),
    # [42] @edgeandnode - GENIUS Act monthly disclosures, KB: disclosure obligations detail
    (
        "GENIUS Act's disclosure requirements go beyond PR: monthly reserve structure + custody location, CPA-reviewed, with C-suite attestation. Non-listed issuers >$50B need full audited financials — that's institutional grade.",
        "规则解读型"
    ),
    # [43] @HyperXAware - GENIUS Act CFTC oversight, KB: SEC-CFTC harmonization event 2026
    (
        "KB notes a Jan 2026 joint SEC-CFTC harmonization event. GENIUS Act covers stablecoin issuers; CLARITY Act addresses commodity vs security classification. KYC/AML for stablecoin-backed systems follows existing BSA.",
        "规则解读型"
    ),
    # [44] @pennycheck - GENIUS Act bullish, KB: GENIUS Act 66-32 Senate vote
    (
        "GENIUS Act passed Senate 66-32 — bipartisan margin signals durability. For crypto firms, the shift from 'regulation by enforcement' to statutory rules means compliance can finally be built ahead of penalties.",
        "反直觉观点型"
    ),
    # [45] @BitAngels - per-wallet cost basis IRS Rev Proc 2024-28, KB: new reporting regime articles
    (
        "Rev. Proc. 2024-28 ended universal wallet accounting from Jan 1 2025. Under the new rules, each wallet is a separate accounting unit — you can't cherry-pick the highest basis from a pooled view across exchanges.",
        "规则解读型"
    ),
    # [46] @summ_app - per-wallet tracking 2025, KB: cost basis adjustments and fee tracking
    (
        "Per-wallet tracking means fees must also be tracked per-wallet. A buy on Coinbase + a transfer fee to MetaMask = different cost lots. Global pooling is gone — the basis you use must tie back to the specific wallet.",
        "场景落地型"
    ),
    # [47] @TimBR_X - IRS cost basis methods links, KB: IRS Pub 551 and crypto tax references
    (
        "IRS Pub. 551 governs cost basis for property — crypto falls under it. FIFO is the default from Jan 1 2025 under new broker rules. HIFO or specific ID remain available but require election and documentation.",
        "规则解读型"
    ),
    # [48] @SaitoshiAgent - Rev Proc 2024-28 per-wallet, KB: 1099-DA and basis reporting 2025
    (
        "Rev. Proc. 2024-28 and 1099-DA are linked: per-wallet tracking aligns with how brokers report — by account, per exchange. If your software still pools globally, your basis and 1099-DA proceeds will never reconcile.",
        "反直觉观点型"
    ),
    # [49] @CryptoTaxAtty - universal to per-wallet basis, KB: cost basis method documentation
    (
        "Rev. Proc. 2024-28 required transition to per-wallet before Jan 1 2025. If you missed it, your 2025 returns carry the wrong starting basis for every wallet — phantom gains or unearned losses in every lot.",
        "反直觉观点型"
    ),
    # [50] @khalidakbary - check universal vs per-wallet, KB: crypto tax reference only
    (
        "'Per-wallet' means per exchange account, per chain address — not just per asset type. Software grouping by token across wallets still gets it wrong. Already tracking per-wallet? No transition needed.",
        "场景落地型"
    ),
    # [51] @Coin_Tracking - IRS 2025 changes, KB: 1099-DA 2025 reporting requirements
    (
        "Three 2025 changes landing at once: per-wallet basis (Rev. Proc. 2024-28), broker 1099-DA reporting of proceeds, and IRS proceeds-matching. The interaction between all three creates complexity that generic tools miss.",
        "反直觉观点型"
    ),
    # [52] @21DogeLoge42 - 2025 crypto tax laws, KB: wash sale proposals
    (
        "The wash sale extension to crypto has been proposed multiple times — 2021 Ways & Means, 2023 bills. Still not law. Until it passes, crypto tax-loss harvesting with immediate repurchase remains technically legal.",
        "反直觉观点型"
    ),
    # [53] @Bitcoinapolis55 - complicated US crypto taxes, KB: IRS December 2024 broker rules
    (
        "IRS released final broker reporting rules in December 2024. The complexity you're seeing is partly by design — staggered rules, broker grace periods, and self-reporting gaps create a system even CPAs find layered.",
        "规则解读型"
    ),
    # [54] @HughHipsDontLie - Rev Proc 2024-28 per wallet mandatory, KB: FIFO default under new rules
    (
        "KB confirms: FIFO is the new default from Jan 1 2025. IRS temporary relief allows HIFO for 2025 only under specific conditions. Choosing HIFO or Spec ID requires consistent application per wallet going forward.",
        "规则解读型"
    ),
    # [55] @tahoetax - wash sale rule doesn't apply to crypto, KB: no crypto wash sale rule yet
    (
        "Wash sale (IRC 1091) explicitly covers securities — IRS treats crypto as property, not securities. So the 30-day prohibition doesn't apply. Bills to change this have been introduced but none enacted.",
        "规则解读型"
    ),
    # [56] @ChadSlimeBased - sell BTC, buy back in 6 seconds, realize loss, KB: wash sale gap
    (
        "Exactly how it works: crypto isn't a security, so IRC 1091 doesn't apply. Sell BTC at a loss, buy back instantly, realize the loss for tax purposes. This window may close when Congress acts — use it or lose it.",
        "场景落地型"
    ),
    # [57] @BitcoinHofmann - Spain wash sale, KB: Spain crypto tax guide in KB
    (
        "Spain has its own capital gains rules. The wash sale exemption for crypto is a US-specific gap. In Spain, cryptocurrency is taxed as capital gain on disposal — different treatment, separate holding period rules.",
        "规则解读型"
    ),
    # [58] @Itstrev - sell loss buy back same day crypto, KB: wash sale rules details
    (
        "Yes — for US crypto: no wash sale rule, so you can sell at a loss and repurchase the same asset immediately. The loss is still claimable. This differs fundamentally from stocks, where the 30-day rule applies.",
        "规则解读型"
    ),
    # [59] @Reducecryptotax - year-end tax planning, KB: tax loss harvesting mechanics
    (
        "Sell before Dec 31 to realize losses — unrealized doesn't count. Losses offset gains first, then up to $3k ordinary income/year. Unused losses carry forward indefinitely. No wash sale rule means you stay in position.",
        "场景落地型"
    ),
    # [60] @JordanFreyMD - TLH with BTC substantially identical, KB: substantially identical unclear for NFTs
    (
        "The 'substantially identical' test doesn't apply to crypto under current law. For NFTs, KB flags ambiguity — buying a similarly named NFT after selling one may or may not be identical. BTC repurchase is clean for now.",
        "反直觉观点型"
    ),
    # [61] @countonsheep - CEO warns 1099-DA missing basis, KB: 8 billion 1099-DA forms estimate
    (
        "IRS estimated 8 billion 1099-DA forms — more than all other 1099s combined. Missing basis data on that scale means a significant portion of filers will see 'unknown' basis from exchanges without cross-platform history.",
        "反直觉观点型"
    ),
    # [62] @Empower_Capital - tax-loss harvesting offsets gains, KB: US crypto losses as capital losses
    (
        "Under US rules: crypto losses are capital losses. They first offset capital gains dollar-for-dollar. If net losses remain, up to $3,000 offsets ordinary income. Excess carries forward — no expiry.",
        "规则解读型"
    ),
    # [63] @MarketInsigh360 - loss harvesting most don't use, KB: tax loss harvesting mechanics + UK allowance
    (
        "Crypto has an advantage stocks don't: no wash sale rule. You can harvest the loss, stay in the position immediately, and still claim the deduction. That's why the strategy is far more powerful for crypto than equities.",
        "反直觉观点型"
    ),
    # [64] @CryptactGlobal - Canada CRA capital loss harvesting, KB: Canada crypto loss rules
    (
        "Canada has no $3k annual cap — losses offset gains from past 3 years or any future year. But Canada's superficial loss rule DOES apply to crypto: sell and repurchase within 30 days, loss is disallowed.",
        "反直觉观点型"
    ),
    # [65] @nelsonbarss - max loss write-off question, KB: $3k limit + carryforward US rule
    (
        "US rule: capital losses first offset all capital gains. Net losses then deduct up to $3,000 against ordinary income per year. Remaining losses carry forward indefinitely — there's no dollar ceiling, just an annual rate.",
        "规则解读型"
    ),
    # [66] @saylordocs - buy BTC sell loss buy back, KB: wash sale not applicable to crypto
    (
        "The loophole is real and legal: IRS classifies crypto as property (Notice 2014-21), not a security. IRC 1091 wash sale only covers securities. Sell, rebuy, recognize loss — fully valid under current law.",
        "规则解读型"
    ),
    # [67] @the_tax_intern - $4.5B BTC loss harvest, KB: German cost methods + loss harvesting context
    (
        "Year-end loss harvesting at scale affects market prices. Institutions selling billions in realized losses before Dec 31 creates predictable sell pressure — then buybacks in January. The pattern repeats every year.",
        "场景落地型"
    ),
    # [68] @DEFIRUSH_ - tax loss harvesting market dips, KB: wash sale could extend to crypto
    (
        "KB note: if wash sale rules extend to crypto, the 30-day window would disallow losses on repurchases. Investors would need to wait 30 days — or substitute into a similar-but-not-identical asset to preserve the loss.",
        "反直觉观点型"
    ),
    # [69] @Tylerp270 - tax loss harvest laws crypto vs stock, KB: wash sale 30 days for securities
    (
        "Stocks: 30-day wash sale rule applies — buy back before 30 days and the loss is disallowed. Crypto: no such rule. The difference is the asset classification. Crypto is property; stocks are securities. Different rules.",
        "规则解读型"
    ),
    # [70] @skumWgmi - wash sale BTC 6 seconds, KB: no crypto wash sale = technically legal
    (
        "Confirmed by KB: no US crypto wash sale rule. Sell BTC at a loss, repurchase 6 seconds later, claim the $38k loss. Legally valid. But KB also notes legislators are watching — this window has been proposed for closure.",
        "场景落地型"
    ),
    # [71] @VJLvEekhout - year-end crypto dip tax loss harvest, KB: TLH mechanics
    (
        "Year-end dips often reflect tax-loss harvesting — not panic. Investors realize losses before Dec 31, then repurchase in January. The pattern repeats because the incentive is structural: no wash sale rule for crypto.",
        "场景落地型"
    ),
    # [72] @3orovik - TLH year-end volatility, KB: US losses $3k cap + carryforward
    (
        "$3k/year ordinary income offset + unlimited capital gain offset + indefinite carryforward. No wash sale rule means you stay in position while booking the loss. Every dip is a potential tax asset.",
        "规则解读型"
    ),
    # [73] @garvkapur - max loss claim question, KB: $3k limit + carryforward
    (
        "No cap on offsetting capital gains — losses offset dollar-for-dollar. For ordinary income, $3,000/year max. Remainder carries forward indefinitely. The actual 'max' depends on your total gains to offset.",
        "规则解读型"
    ),
    # [74] @SamLedger74 - DeFi DEX 1099-DA coming, KB: DeFi frontend as broker
    (
        "IRS defined DeFi frontends as brokers — even without holding keys, if they facilitate trade execution and order processing they face 1099-DA obligations. Most DEXs aren't reporting yet, but the rule exists.",
        "规则解读型"
    ),
    # [75] @SamLedger75 - DEX swaps not broker-reported, KB: DeFi frontend broker rule detail
    (
        "IRS reasoning: even if a DeFi aggregator adds intermediate steps, it doesn't escape broker classification. Frontend provides trade initiation and execution — that's enough. Basis gaps in DEX history = your audit risk.",
        "反直觉观点型"
    ),
]

def main():
    with open('search_matches_v3.json') as f:
        v3 = json.load(f)
    with open('search_tweets_with_kb.json') as f:
        kb_data = json.load(f)

    assert len(v3) == 76, f"Expected 76 records, got {len(v3)}"
    assert len(kb_data) == 76, f"Expected 76 KB records, got {len(kb_data)}"
    assert len(REPLIES) == 76, f"Expected 76 replies, got {len(REPLIES)}"

    over_220 = 0
    used_kb = 0

    for i, (record, kb_item, (reply, angle)) in enumerate(zip(v3, kb_data, REPLIES)):
        # Merge kb fields
        record['kb_chunks'] = kb_item.get('kb_chunks', [])
        record['relevance'] = kb_item.get('relevance', 0)

        # Update reply
        record['final_reply'] = reply
        record['final_angle'] = angle

        # Stats
        if len(reply) > 220:
            over_220 += 1
            print(f"[{i}] OVER 220 ({len(reply)} chars): {reply}")

        kb_chunks = kb_item.get('kb_chunks', [])
        has_useful_kb = any(len(c.get('text', '').strip()) > 30 for c in kb_chunks)
        if has_useful_kb:
            used_kb += 1

    # Save
    with open('search_matches_v3.json', 'w', encoding='utf-8') as f:
        json.dump(v3, f, ensure_ascii=False, indent=2)

    print(f"\n=== SUMMARY ===")
    print(f"Total records: {len(v3)}")
    print(f"Over 220 chars: {over_220}")
    print(f"Used kb_chunks (had useful content): {used_kb}")

if __name__ == '__main__':
    main()
