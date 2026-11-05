# Project Vortex Portfolio

**Live portfolio:** [leobobadilha.github.io/project-vortex-portfolio](https://leobobadilha.github.io/project-vortex-portfolio/)
**Power BI showcase:** [project-vortex-bi-showcase](https://github.com/LeoBobadilha/project-vortex-bi-showcase)

Project Vortex examines whether discretionary Price Action concepts can be formalized and tested systematically. AI agents supported research, implementation and analysis across historical experiments; I set the research direction, contributed market context and reviewed the evidence.

The static portfolio is published at [leobobadilha.github.io/project-vortex-portfolio](https://leobobadilha.github.io/project-vortex-portfolio/). It uses semantic HTML, custom CSS, browser-native JavaScript and SVG charts. It has no backend, trading API, broker connection or live market feed.

## Historical benchmark

The selected reference is the **P6+SIZE+CE (PSC) historical backtest**, covering 2022-01-04 through 2026-10-20: 324 portfolio records, 526 contract units, R$23,551 gross P&L, R$3,156 C30 costs applied once and R$20,395 net C30 P&L. The win rate is 57.716%, profit factor 1.950816 and maximum realized close-order drawdown R$1,932. M5-close drawdown (R$2,077) and adverse OHLC-envelope drawdown (R$2,113) are separate measures. P6 is reported separately and does not share the same end date.

The monthly cumulative chart is a running sum of monthly aggregates, not account equity or a trade-order path. The website does not calculate percentage returns because initial capital is unspecified.

## Power BI showcase

The companion [Project Vortex BI showcase](https://github.com/LeoBobadilha/project-vortex-bi-showcase) contains the public-safe 14-page PBIP. This website currently displays the clean Executive Overview preview only. The complete screenshot gallery is withheld while eight pages await genuine Power BI Desktop recaptures; do not interpret the single preview as the full report. The PBIP structure is unchanged.

## Data and local preview

Three approved aggregate CSV files are distributed under `public/data/`; the browser currently fetches `monthly_portfolio_results.csv` and `benchmark_summary.csv`. ``annual_portfolio_results.csv` is distributed as the third aggregate file but is not fetched by current JavaScript. No row-level trade ledger or raw market series is embedded.

Requirements: Node.js 18+ and Python 3.10+.

```powershell
node scripts/build.mjs
npm run preview
```

Open `http://127.0.0.1:4174`. The build copies `src/` and approved assets from `public/` into `dist/`.

## Release and risk

The initial `v1.0.0` tag remains intact. The current public `main` includes the screenshot-withdrawal update at commit `0b4b617d072d37e3ef8a668bca948b21bad4ce24`; the successful Pages deployment is [workflow run 42029504199](https://github.com/LeoBobadilha/project-vortex-portfolio/actions/runs/42029504199). Prior public commits still contain the original image blobs; this update does not rewrite history.

Past performance, including historical backtests and simulated trading results, does not guarantee future results. Actual trading involves risk and execution conditions may differ materially from simulations. No Paper Live P&L or real-money record is claimed.

Project and professional profile: [LinkedIn](https://www.linkedin.com/in/leonardobobadilha/).
