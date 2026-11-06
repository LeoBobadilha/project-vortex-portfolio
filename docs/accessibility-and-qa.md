# Accessibility and QA

The static interface uses keyboard-visible focus, semantic headings, alt text, reduced-motion support and high-contrast color tokens. Body text uses `#F0F6FC`, labels `#DCE6F0`, secondary copy `#C7D6E4`, surfaces `#102236`, positive `#58E39A` and negative `#FF7F83`.

Edge headless QA used the repository-subpath build at desktop 1920x1080, laptop 1366x768, tablet 768x1024 and mobile 390x844. Tests verified PSC and P6 selection, year and gross/net filters, the case-study loss filter, Power BI lightbox navigation, all 14 gallery image decodes, replay entry/seek/play/pause/restart/exit behavior, result gating until exit, and zero document-width overflow at tablet and mobile sizes. The run reported no console errors and no failed requests.

The repository's `docs/screenshots/` folder contains the four standard viewport captures. The browser QA run also produced separate desktop, laptop, tablet, mobile, gallery and replay screenshots in private local QA storage; those artifacts are not part of the public site. The gallery includes all 14 PBIP pages as verified Desktop captures; the report itself is unchanged. The replay now labels its source session date as 30 Sep 2022 and states that the source clock timezone is unverified.
