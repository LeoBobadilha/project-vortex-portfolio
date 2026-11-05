# Public data provenance

Three approved aggregate CSV files are distributed in `public/data/`. The portfolio browser code fetches `monthly_portfolio_results.csv` and `benchmark_summary.csv`; `annual_portfolio_results.csv` is the third aggregate CSV and is not requested by that code. The files support historical portfolio views for P6+SIZE+CE and the separate P6 baseline. PSC reconciles to 324 records and 526 contract units: R$23,551 gross, R$3,156 C30 costs applied once and R$20,395 net.

The replay adds one separate research-only scaling case: 107 WIN M5 OHLC bars with a translated price scale and session-relative time, plus outcome figures loaded only after the modeled exit. Its two distinct one-contract legs reconcile to R$750.20 gross and R$738.20 after the study's R$12 S2 stress cost. This is not a PSC record and S2 is not the portfolio C30 scenario. The exact source date/time, event ID, unshifted prices, ledger, and broader archive are excluded. The OHLC geometry remains recognizable, so residual market-correlation risk remains. See the replay methodology for source limitations.

Other case-study images mask exact dates, price scales, family identifiers and individual results. All case studies are selected examples, not a distribution sample.
