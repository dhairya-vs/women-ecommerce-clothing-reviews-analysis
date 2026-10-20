# Data Cleaning Log

- Original shape: 23,486 rows × 11 columns.
- Missing values before cleaning: Title 3,810; Review Text 845; Division Name 14; Department Name 14; Class Name 14.
- Dropped `Unnamed: 0`, an exported index column.
- Filled missing `Title` and `Review Text` with empty strings; no review text was invented.
- Filled missing clothing categories with `Unknown`.
- Converted numeric fields and checked age (13–100), rating (1–5), recommendation (0/1), and non-negative feedback count.
- Removing the exported index exposed 21 exact duplicate records; these were removed. No invalid numeric values were found.
- IQR age bounds: 7 to 79; flagged records: 109.
- IQR positive-feedback upper bound: 7.5; flagged records: 2,147.
- IQR-flagged values were retained because unusual does not automatically mean erroneous. Feedback values are capped at 30 in the chart only.
- Cleaned output: 23,465 rows × 10 columns; no missing values or duplicates remain after cleaning.
