# Historical Pyramiding Replay Methodology

The featured replay uses one completed WIN long from a separate exploratory H36AAA historical scaling study. It is not a row from the PSC aggregate benchmark, Paper Live, or a live account. The separate frozen event ledger contains two independently recorded one-contract legs and one shared modeled exit.

## Event sequence and market coverage

The operation progresses from flat to one contract, through a recorded pullback touch, to a separate one-contract addition, and then back to flat at the recorded exit. Both entry and exit prices fall within their associated M5 OHLC envelopes. The selected session has 107 consecutive M5 bars, beginning at the first available session bar, with 31 bars before Entry 1 and 39 after the modeled exit. The replay starts with the 31-bar pre-entry context and continues after the position closes.

The five-minute OHLC record cannot establish intrabar sequencing. Each simulated fill is therefore revealed after its associated candle is complete. The candle's high, low, and close are not presented before that bar becomes visible. The replay uses separate entry events and computes open marks for each leg independently from the latest visible completed close. After exit, the position remains flat and realized P&L stays fixed while later candles appear.

## Result and costs

These are model values, not executable trade results. The H36 run configuration specifies a five-point minimum tick for WIN, but the selected adjusted-price model fills are not all grid-aligned. Entry 1 is aligned; Entry 2 is three points off-grid and the modeled exit is two points off-grid. The public price translation is a multiple of five, so it preserves these residuals. No fills were rounded or snapped.

The source ledger's exact arithmetic is 2,027 + 1,724 = 3,751 modeled points, and 3,751 × R$0.20 = R$750.20 modeled gross. That explains the 20-cent remainder; it is not a currency-rounding defect. The study's S2 stress assumption applies R$6 per modeled contract: R$2 round-trip brokerage plus two adverse ticks per side (20 points total at R$0.20), or R$12 for two contracts. The resulting R$738.20 is net under that research assumption, not a tick-valid or exchange-executable result. Other fees are excluded. S2 is not the PSC portfolio's C30 scenario and these figures must not be merged with PSC metrics.

An execution-realistic recalculation is not defensible from the available source: it is continuous-adjusted PRICE_ONLY OHLC from a demo `WIN$` series, with no certified individual-contract quotations, bid/ask or fills. The related broker-wall timestamp view is derived from the same feed and marks price adjustment as unverified. Snapping the event prices would change the model outcome without rerunning and validating the strategy on a verified unadjusted contract series. No better evidenced 1+1 WIN example is available in the inspected H36 artifacts; the replay is retained only as an explicitly qualified view of the research model.

## Public data and reproducibility

The browser receives 107 OHLC bars with a constant price translation and elapsed-minute offsets. Chart labels map those offsets to the source-session clock from 09:00 through 17:50. The source timezone is unauthenticated, so the labels are not certified B3 local timestamps. The date and clock labels are intentionally public; exact absolute event timestamps, event IDs, the unshifted price scale, raw market archive, ledger, code and strategy parameters remain private. Publishing the date, clock labels and recognizable candle geometry increases external market-correlation risk.

The sanitized files are `public/data/replay/pyramiding-win-session.json` and `public/data/replay/pyramiding-win-outcome.json`. Run `npm run test:replay` to check position progression, per-leg P&L, weighted average entry, S2 costs, chronology, candle geometry, full-session coverage, post-exit bars, and the public-data boundary. The source-linked ledger reconciliation, hashes and exact event mapping are maintained in a private local validation record.

## Source limitations

The source market session date is **30 September 2022**, cross-checked against both the frozen H36 event ledger and the 107-bar WIN$ M5 source series. The public chart labels run from 09:00 to 17:50 according to the source-session clock convention. Its timezone has not been authenticated, so these are not certified B3 local timestamps. The data are continuous-adjusted PRICE_ONLY M5 OHLC, not raw contract quotations. The series does not certify tick-valid bid/ask quotes, exchange-executable fills, contract rollover behavior, or exact intrabar path. Publishing the date and clock labels with recognizable candle geometry materially increases correlation with external market data. The source study states that the tested period had prior research exposure and is not an untouched holdout. This selected winning example is illustrative, not representative or evidence of future profitability.

> Selected historical backtest example. This operation is not representative of all trades. Past performance, including historical backtests and simulated trading results, does not guarantee future results. Live trading involves risk, and actual execution may differ materially from simulated outcomes.
