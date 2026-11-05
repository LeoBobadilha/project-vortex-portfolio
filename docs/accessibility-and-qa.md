# Accessibility and QA

The static interface uses keyboard-visible focus, semantic headings, alt text, reduced-motion support and high-contrast color tokens. Body text uses `#F0F6FC`, labels `#DCE6F0`, secondary copy `#C7D6E4`, surfaces `#102236`, positive `#58E39A` and negative `#FF7F83`.

Previous Chromium QA used these capture sizes: desktop 1920x1080, laptop 1366x768, tablet 768x1024 and mobile 390x844. Browser tests verified portfolio/year/basis behavior, that full-history PF and DD remain fixed across year/basis filters, six/two gallery filters, case dialog operation, no overflowing document width, and loaded visual assets (the empty dialog image before opening is expected).


The current release-content edits passed the static build, public-asset audit and smoke test. The Power BI screenshot gallery is intentionally withheld pending eight real captures. No fresh browser-console check or new desktop/mobile screenshots were produced in this documentation update.
