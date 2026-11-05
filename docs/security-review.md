# Public Security Review

Review date: 2026-11-05. This review covers website source, generated `dist/`, public aggregate data, images, documentation and repository history.

The site is a static HTML, CSS and browser-native JavaScript application. It has no backend, trading endpoint, broker connection, account data, authentication or external runtime script. Three approved aggregate CSVs are distributed; portfolio JavaScript fetches the monthly portfolio and benchmark summary files. The replay loads one sanitized candle window and requests its outcome only at the final replay step. The website build reproduces `dist/` from `src/`, `public/images/` and `public/data/`.

The release candidate displays six inspected clean Power BI Desktop captures (pages 01-03 and 12-14) in an accessible gallery. Eight screenshots for PBIP pages 04-11 remain withheld because the former captures contained Zoom or desktop overlays; no replacements have been fabricated or recaptured. The companion public PBIP retains all 14 pages.

The screenshot-withdrawal update is published on website `main` at `0b4b617d072d37e3ef8a668bca948b21bad4ce24`. The successful Pages deployment is [workflow run 42029504199](https://github.com/LeoBobadilha/project-vortex-portfolio/actions/runs/42029504199). The initial `v1.0.0` tag still points to `0fc9239bfd860c63cb60fa0d2186f09492c48545`, which contains the previous gallery; the current-tree withdrawal is in `0b4b617`. This review is a source and asset audit, not a claim of an external secret-scanner result.

The current published trees withhold the affected images, but prior public commits and the original release tag still contain historical image blobs. This release did not rewrite history. A history rewrite, if approved, requires a separate privacy-remediation decision.

The release candidate includes a single case-specific two-contract historical WIN replay. It preserves the 21-bar shape and point movements with a constant price offset and relative time labels. A private validation record maps it to the frozen source ledger and M5 data; that record and the broader market files are excluded. The public assets contain no private trade identifier, exact source timestamp, contract expiry, strategy trigger logic, credential, account field or broker connection. The website audit found no sensitive/path matches in text-based public files. Historical backtest results are not Paper Live or live-account performance.
