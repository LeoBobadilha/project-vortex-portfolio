# Architecture

```mermaid
flowchart LR
  H[Human Price Action knowledge] --> I[Structured Intelligence artifacts]
  I --> R[Research hypotheses]
  R --> C[Implementation requests and versioned code]
  C --> B[Historical replay and scenario tests]
  B --> A[Audit, retest and portfolio review]
  A --> P[Paper Live preparation]
  P --> G[Human authorization gate]
```

The portfolio site is a separate static artifact: approved aggregate CSVs load in the browser, custom JavaScript calculates filtered P&L summaries and renders SVG charts. It has no trading connection.
