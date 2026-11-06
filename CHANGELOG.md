# Changelog

## Unreleased

- Refreshed all 14 Power BI images after the report correction: P6 and PSC are never combined, page 05 is PSC only, and the case pages are now 16:9 with their caveat fully visible.
- The Executive Overview preview now uses the current page 03 image; the separate older file is removed.
- The file manifest now hashes canonical LF text and exact image bytes, and CI checks that it reproduces on Linux.
- Added the verified source market session date (30 September 2022) with an explicit timezone qualification; documented the resulting OHLC correlation risk. Clarified that the case-study examples are historical and the replay position is simulated.
- Added a prominent WIN tick-grid qualification to the 1+1 replay: the 20-cent remainder comes from exact arithmetic on off-grid adjusted-price model fills; no fills were rounded, and the displayed BRL outcome is not exchange-executable performance.

- Replaced the fixed two-contract PSC replay with a separate, event-ledger-backed one-plus-one WIN scaling study. The new replay covers the available 107-bar session, shows 39 candles after exit, and reports its distinct S2 research cost scenario without mixing it with PSC C30 metrics.
- Added an interactive candlestick chart using locally bundled TradingView Lightweight Charts, accessible replay controls, per-leg position marks, and position-state regression tests in the Pages workflow.
- Added a complete 14-page Power BI gallery with keyboard-operable full-size previews. All 14 images are genuine Power BI Desktop captures from one refreshed session (3208 x 1804); they replace the six earlier images and the eight withheld pages.
- Added reproducible public replay checks and refreshed the methodology and data-provenance notes; the source-linked validation record remains local and private.

## Published main update (0b4b617)

- Withheld the Zoom-contaminated Power BI gallery and kept the clean Executive Overview preview.
- Added the GitHub Actions workflow that builds and deploys `dist/` to GitHub Pages.
- Updated publication, data and historical-risk documentation. The initial `v1.0.0` tag remains unchanged.

## 1.0.0

- Published the static portfolio, approved aggregate data and reproducible build.
- Documented historical net C30 profit factor and realized drawdown semantics.
- Redacted exact timestamps, price values, individual results and strategy labels from selected case visuals.
