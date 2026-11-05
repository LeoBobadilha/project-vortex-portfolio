# Historical Trade Replay Methodology

The replay uses one completed two-contract WIN short selected from the frozen P6+SIZE+CE (PSC) backtest ledger. It is a single historical case study, not a representative sample and not live trading evidence.

## Reconciliation

The selected row is the highest positive point-capture record among the PSC ledger's 66 completed two-contract winners. Its directional entry-to-exit movement is 2,930 index points. Under the verified WIN point value of R$0.20 per point per contract, gross P&L is R$1,172. The locked C30 scenario charges 30 points per contract once: 30 × 2 × R$0.20 = R$12. The resulting net C30 amount is R$1,160. The replay does not apply another cost deduction. The row records one two-contract operation; no separate add-on sequence is available or represented.

The entry and exit times resolve to the same continuous WIN M5 source series. Both recorded fills fall inside their corresponding candles. The 21 displayed bars cover six context candles before entry through the exit candle, with no missing five-minute interval. The recorded 3,625-point maximum favorable excursion and 55-point maximum adverse excursion match the entry-to-exit M5 OHLC envelope.

## Public representation

The public dataset contains only the selected 21 OHLC bars and the minimum event metadata needed by the replay. A constant offset shifts every price while preserving candle geometry, tick increments and point movement. Calendar date, exact clock times, contract expiry, source row index, strategy identifier and private ledger fields are omitted. The horizontal axis therefore shows elapsed minutes from entry, and the vertical axis shows shifted prices.

The completed result is stored separately from the candle file and requested only after playback reaches the exit. The interface draws only candles up to the current replay step. Open P&L is marked from the latest visible completed M5 close and is labeled as a gross mark. The completed summary appears only at the exit.

This is a deliberate reduction of exposure, not a guarantee against correlation with external market data. The retained candle shape and point moves may still be recognizable. Private source paths, row identifiers and full market archives are not included in the repository.

## Reproduction and local audit

The sanitized files are `public/data/replay/two-contract-win.json` and `public/data/replay/two-contract-win-outcome.json`. `scripts/test_trade_replay.py` checks candle order, event bounds, the two-contract sizing, directional points, gross BRL, C30 cost, net BRL, excursions and the public/private data boundary.

The source-linked row, source file hashes, exact source timestamps and original prices are retained in a private validation record outside the public repositories. The local implementation workspace contains the sanitizer used to reproduce the public export; it is intentionally excluded from the public website and BI repositories.

## Limitations

M5 OHLC bars cannot show the intrabar tick path or establish the precise ordering of every price inside a candle. The ledger supplies the recorded fills; the bars are used to verify candle coverage, fill-range consistency and the excursions. The animation is a stepwise historical visualization, not an execution simulator. The example's positive result must not be generalized to other trades.

> Selected historical backtest example. This operation is not representative of all trades. Past performance does not guarantee future results.
