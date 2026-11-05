# Public Security Review

Review date: 2026-11-05. This review covers website source, generated `dist/`, public aggregate data, images, documentation and repository history.

The site is a static HTML, CSS and browser-native JavaScript application. It has no backend, trading endpoint, broker connection, account data, authentication or external runtime script. Three approved aggregate CSVs are distributed; current JavaScript fetches the monthly portfolio and benchmark summary files. The website build reproduces `dist/` from `src/`, `public/images/` and `public/data/`.

The live page displays the clean Executive Overview capture. The complete screenshot gallery remains withheld: captures for PBIP pages 04-11 contained Zoom or desktop overlays. No replacement captures have been made. The companion public PBIP retains all 14 pages and its BI repository currently contains six inspected clean screenshots.

The screenshot-withdrawal update is published on website `main` at `0b4b617d072d37e3ef8a668bca948b21bad4ce24`. The successful Pages deployment is [workflow run 42029504199](https://github.com/LeoBobadilha/project-vortex-portfolio/actions/runs/42029504199). The initial `v1.0.0` tag still points to `0fc9239bfd860c63cb60fa0d2186f09492c48545`, which contains the previous gallery; the current-tree withdrawal is in `0b4b617`. This review is a source and asset audit, not a claim of an external secret-scanner result.

The current published trees withhold the affected images, but prior public commits and the original release tag still contain historical image blobs. This release did not rewrite history. A history rewrite, if approved, requires a separate privacy-remediation decision.

The site contains only approved portfolio aggregates and deliberately redacted case visuals. It excludes private trade ledgers, executable strategy source, raw M5 archives, credentials, account data and broker connections. The reported performance is historical backtest data; Paper Live P&L and live-account results are not claimed.
