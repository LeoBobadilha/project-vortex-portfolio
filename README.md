# Project Vortex Portfolio

A lightweight, static technical portfolio about Price Action research, AI-assisted engineering, quantitative validation and Power BI. The site uses semantic HTML, custom CSS, browser-native JavaScript and SVG charts; it has no backend, trading API, account connection or runtime dependency.

## Run locally

Requirements: Node.js 18+ and Python 3.10+.

Build: npm run build
Preview: npm run preview

Open http://127.0.0.1:4174. The preview serves generated dist/ files.

## Content and data

The three CSVs are approved portfolio-level aggregates. They contain no operation ledger. The companion [Project Vortex BI showcase](https://github.com/LeoBobadilha/project-vortex-bi-showcase) is the 14-page public-safe PBIP repository. The primary P6+SIZE+CE historical benchmark covers 2022-01-04 through 2026-10-20 (324 records, 526 contract units): gross R$23,551, net C30 R$20,395, recorded costs R$3,156, win rate 57.72%, PF 1.951 and realized close-order maximum drawdown R$1,932. No percentage return is reported because no starting-capital assumption is defined. The P6 baseline is separately reported and ends on a different date.

The website's selected case visuals derive from verified historical chart captures. Exact dates, price scales, individual P&L and strategy identifiers are masked; candle geometry is retained. These selected cases are illustrative and not statistically representative.

## Metric behavior

Year and gross/net selectors update monthly/annual P&L views. The headline profit factor and realized drawdown remain full-history portfolio-level net C30 metrics and respond only to portfolio selection. Cumulative monthly P&L is not account equity or a return series.

## Privacy and release

No private trade ledger, executable strategy, raw M5 archive, broker credentials or account data is included. Only approved aggregates and deliberately redacted case visuals are shipped. This repository contains static website source and is not deployed to a public hosting URL.

The research lead's approved profile: [LinkedIn](https://www.linkedin.com/in/leonardobobadilha/). The companion public BI repository is linked above.

## Risk disclosure

Past performance, including historical backtests and simulated trading results, does not guarantee future results. Actual trading involves risk, and execution conditions may differ materially from simulations. No Paper Live P&L or real-money record is claimed.
