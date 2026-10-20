# Short Insights Report
## Women's E-Commerce Clothing Reviews Analysis

### Findings from the supplied dataset
1. **Ratings are generally positive.** Mean rating: 4.20/5. Ratings of 4 or 5 make up 77.5% of records; 5-star reviews account for 55.9%.
2. **Most reviews recommend the item.** 82.2% have Recommended IND = 1 (19,293 records); 4,172 do not recommend the item.
3. **Reviewer ages are centered in adulthood.** Mean age: 43.2; median: 41. This describes the dataset, not all shoppers.
4. **Department ratings differ modestly.** Among named departments, Bottoms has the highest average rating (4.29/5), while Trend has the lowest (3.82/5). Trend has far fewer reviews, so its average is less stable.
5. **Feedback counts are right-skewed.** Median positive feedback is 1; the 99th percentile is 26.
6. **Review length varies.** Mean review length is 298 characters. The boxplot compares review length by rating; this is descriptive, not causal.
7. **Age and rating are only weakly related.** Pearson correlation is 0.027.
8. **Frequent words** are shown in a simple token-count chart. This is not a validated sentiment model and does not understand negation, sarcasm, or context.

### Cleaning
The source contained 23,486 rows and 11 columns. Removing the exported index revealed 21 duplicate records; the cleaned analysis contains 23,465 rows and 10 columns. Missing titles/reviews were filled with blank strings, and missing clothing categories were marked Unknown. IQR-flagged values were retained when plausible.

### Limitations and conclusion
The dataset covers one retailer; category means depend on sample size; correlation does not establish causation; and word frequency does not establish sentiment. Overall, reviews are mostly positive and most recommend the products.
