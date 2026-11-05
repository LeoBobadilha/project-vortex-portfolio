# Historical Pyramiding Replay Methodology

The featured replay uses one completed WIN long from a separate exploratory H36AAA historical scaling study. It is not a row from the PSC aggregate benchmark, Paper Live, or a live account. The separate frozen event ledger contains two independently recorded one-contract legs and one shared modeled exit.

## Event sequence and market coverage

The operation progresses from flat to one contract, through a recorded pullback touch, to a separate one-contract addition, and then back to flat at the recorded exit. Both entry and exit prices fall within their associated M5 OHLC envelopes. The selected session has 107 consecutive M5 bars, beginning at the first available session bar, with 31 bars before Entry 1 and 39 after the modeled exit. The replay starts with the 31-bar pre-entry context and continues after the position closes.

The five-minute OHLC record cannot establish intrabar sequencing. Each simulated fill is therefore revealed after its associated candle is complete. The candle's high, low, and close are not presented before that bar becomes visible. The replay uses separate entry events and computes open marks for each leg independently from the latest visible completed close. After exit, the position remains flat and realized P&L stays fixed while later candles appear.

## Result and costs

The first leg records 2,027 favorable points and R$405.40 gross. The second records 1,724 points and R$344.80 gross. At R$0.20 per point per contract, the two-leg result totals 3,751 contract-points and R$750.20 gross. The weighted average entry is the arithmetic mean of the two one-contract fills.

The display applies the research study's S2 stress scenario once per contract: R$2 round-trip brokerage plus 20 adverse round-trip points at R$0.20 per point, or R$6 per leg. Total S2 costs are R$12 and the resulting net is R$738.20. Other fees are excluded in the source study. S2 is not the PSC portfolio's C30 scenario and these results must not be merged with PSC metrics.

## Public data and reproducibility

The browser receives 107 OHLC bars with a constant price translation and elapsed minutes from session open. A separate outcome file is requested only after playback reaches the recorded exit. The raw market archive, source date and clock, event IDs, exact unshifted price scale, ledger, code and strategy parameters remain private. The public transformation preserves candle shape and point distances; market-correlation risk remains.

The sanitized files are `public/data/replay/pyramiding-win-session.json` and `public/data/replay/pyramiding-win-outcome.json`. Run `npm run test:replay` to check position progression, per-leg P&L, weighted average entry, S2 costs, chronology, candle geometry, full-session coverage, post-exit bars, and the public-data boundary. The source-linked ledger reconciliation, hashes and exact event mapping are maintained in a private local validation record.

## Source limitations

The underlying series is continuous adjusted PRICE_ONLY OHLC. It does not certify bid/ask quotes, exchange-executable fills, contract rollover behavior, or exact intrabar path. The source clock's timezone is unauthenticated; the public chart therefore uses session-relative time. The source study states that the tested period had prior research exposure and is not an untouched holdout. This selected winning example is illustrative, not representative or evidence of future profitability.

> Selected historical backtest example. This operation is not representative of all trades. Past performance, including historical backtests and simulated trading results, does not guarantee future results. Live trading involves risk, and actual execution may differ materially from simulated outcomes.
