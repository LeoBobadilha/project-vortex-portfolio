# Project Vortex Portfolio

**Live portfolio:** [leobobadilha.github.io/project-vortex-portfolio](https://leobobadilha.github.io/project-vortex-portfolio/)
**Power BI showcase:** [project-vortex-bi-showcase](https://github.com/LeoBobadilha/project-vortex-bi-showcase)

Project Vortex examines whether discretionary Price Action concepts can be formalized and tested systematically. AI agents supported research, implementation and analysis across historical experiments; I set the research direction, contributed market context and reviewed the evidence.

The static portfolio is published at [leobobadilha.github.io/project-vortex-portfolio](https://leobobadilha.github.io/project-vortex-portfolio/). It uses semantic HTML, custom CSS, browser-native JavaScript and SVG charts. It has no backend, trading API, broker connection or live market feed.

## Historical benchmark

The selected reference is the **P6+SIZE+CE (PSC) historical backtest**, covering 2022-01-04 through 2026-10-20: 324 portfolio records, 526 contract units, R$23,551 gross P&L, R$3,156 C30 costs applied once and R$20,395 net C30 P&L. The win rate is 57.716%, profit factor 1.950816 and maximum realized close-order drawdown R$1,932. M5-close drawdown (R$2,077) and adverse OHLC-envelope drawdown (R$2,113) are separate measures. P6 is reported separately and does not share the same end date.

The monthly cumulative chart is a running sum of monthly aggregates, not account equity or a trade-order path. The website does not calculate percentage returns because initial capital is unspecified.

## Power BI showcase

The companion [Project Vortex BI showcase](https://github.com/LeoBobadilha/project-vortex-bi-showcase) contains the public-safe 14-page PBIP. The website gallery currently shows six verified clean Desktop captures: pages 01-03 and 12-14. Pages 04-11 remain part of the PBIP but are withheld until genuine clean recaptures are available. The gallery does not represent the full report.

The case-study area includes an interactive replay from a separate exploratory WIN scaling backtest. Its event ledger records a one-contract long, a pullback, a separately recorded one-contract add-on, and a shared model exit. The selected session contains all 107 available M5 bars, including 39 after the modeled exit. The source is continuous-adjusted PRICE_ONLY OHLC: Entry 2 and exit are off WIN's 5-point tick grid, so the displayed R$750.20 gross and R$738.20 after the study's S2 assumptions are unrounded research-model arithmetic, not exchange-executable performance or account P&L. We did not snap fills to the grid because no verified unadjusted contract quotes are available for a valid rerun. S2 is not C30. See [Trade Replay Methodology](docs/trade-replay-methodology.md).

## Data and local preview

Three approved aggregate CSV files are distributed under `public/data/`; the browser currently fetches `monthly_portfolio_results.csv` and `benchmark_summary.csv`. `annual_portfolio_results.csv` is distributed as the third aggregate file but is not fetched by current JavaScript. The replay publishes a translated, session-relative representation of 107 M5 bars plus a separately loaded completed-position summary. The broader market archive and source ledger are not included. Price geometry remains recognizable, so the transformation reduces direct identifiers but does not eliminate correlation risk.

Requirements: Node.js 18+ and Python 3.10+.

```powershell
node scripts/build.mjs
npm run preview
```

Open `http://127.0.0.1:4174`. The build copies `src/` and approved assets from `public/` into `dist/`.

Run the replay model and public-site checks with:

```powershell
node scripts/test_replay_model.mjs
python scripts/test_trade_replay.py
python scripts/audit_public_site.py
python scripts/test_static_site.py
```

## Release and risk

The site is published at [GitHub Pages](https://leobobadilha.github.io/project-vortex-portfolio/). Current `main` state and deployment history are available from the [repository](https://github.com/LeoBobadilha/project-vortex-portfolio) and [Pages workflow](https://github.com/LeoBobadilha/project-vortex-portfolio/actions/workflows/deploy-pages.yml). The initial `v1.0.0` tag remains intact. Prior public commits may retain earlier screenshot blobs; this repository does not rewrite history or claim those historical objects have been erased.

Past performance, including historical backtests and simulated trading results, does not guarantee future results. Actual trading involves risk and execution conditions may differ materially from simulations. No Paper Live P&L or real-money record is claimed.

Project and professional profile: [LinkedIn](https://www.linkedin.com/in/leonardobobadilha/).
