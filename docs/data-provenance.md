# Public data provenance

Three approved aggregate CSV files are distributed in `public/data/`. The portfolio browser code fetches `monthly_portfolio_results.csv` and `benchmark_summary.csv`; `annual_portfolio_results.csv` is the third aggregate CSV and is not requested by that code. The files support historical portfolio views for P6+SIZE+CE and the separate P6 baseline. PSC reconciles to 324 records and 526 contract units: R$23,551 gross, R$3,156 C30 costs applied once and R$20,395 net.

The replay adds one deliberately limited historical case: 21 verified WIN M5 OHLC bars, a shifted price scale and elapsed-minute labels, plus separately loaded outcome figures. It does not include the underlying row-level ledger, exact source date or clock times, absolute price levels, contract expiry, strategy identifiers or broader market archive. The case's published result is R$1,172 gross, R$12 C30 costs and R$1,160 net C30. The methodology note documents its limits and reconciliation.

Other case-study images mask exact dates, price scales, family identifiers and individual results. All case studies are selected examples, not a distribution sample.
