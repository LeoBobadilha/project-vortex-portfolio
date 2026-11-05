# Public Security Review

Review date: 2026-11-04. Scope includes website source, generated `dist/`, published CSVs, case images, Power BI screenshots, docs and release history.

The site is static HTML, CSS and browser-native JavaScript. It has no backend, trading endpoint, broker connection, account data, authentication or external runtime script. Client-side datasets are the approved portfolio-level annual, monthly and benchmark aggregate CSVs. The website build reproduces `dist/` from `src/`, `public/images/` and `public/data/`.

The Power BI section retains the clean Executive Overview capture. The full-page gallery is withheld: visual inspection found Zoom windows, controls and meeting-related information in report pages 04–11, including a participant name and shared market windows. No replacement captures were made because Power BI Desktop is unavailable in this session. The full report and its 14-page structure remain in the companion public PBIP; the website does not display the affected screenshot files.

This is a local hotfix branch based on the published v1.0.0 site. The static source and generated build are subject to local checks; no new remote publication or deployment was possible because GitHub authentication is unavailable. This is not an external GitHub secret-scanner result. Existing public history is unchanged, so previously published image blobs remain in the repository's historical commits.
