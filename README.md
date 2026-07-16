# Fitness Subscription Analytics

## Project Overview
This project analyzes subscription performance for FitnessHub, a subscription-based fitness platform offering workout plans, nutrition coaching, and on-demand classes. The analysis focuses on customer retention, future revenue expectations, and how long it takes customer cohorts to recover acquisition costs through subscription revenue.

## Business Objective
The goal of this analysis is to help leadership understand whether customer growth is sustainable by answering three key business questions:

1. After how many months do customers typically cancel their subscriptions?
2. What is the expected subscription revenue over the next 12 months?
3. How long does it take for the 2024 and 2025 customer cohorts to recover customer acquisition cost (CAC)?

## Tools Used
- Tableau
- Excel
- Cohort analysis
- Revenue forecasting
- CAC vs. LTV analysis

## Dataset
The project uses one Excel workbook: `Fitness_Subscriptions_Dataset.xlsx`

It includes two worksheets:
- `customers` – customer signup details, subscription plans, acquisition channels, country, and CAC
- `transactions` – customer transaction history, transaction dates, and revenue generated

## Key Findings

## Customer Cohort Analysis
The cohort analysis shows that customers are most likely to churn between months 2 and 3 after signup. Across cohorts, retention declines gradually during the first two months, then drops more sharply around month 3, suggesting that the highest cancellation risk occurs early in the customer lifecycle.

This pattern indicates that FitnessHub may be losing customers shortly after the initial onboarding period. Strengthening customer engagement before month 3 could help reduce early churn and improve retention.

## Revenue Forecast
Historical subscription revenue increases steadily throughout 2024 and 2025, reaching a peak around December 2025. The forecast then shows a steep decline into mid-2026, followed by a partial recovery and another downward movement later in the forecast period.

This pattern suggests that future revenue may not grow in a straight line and may be influenced by seasonality or recurring demand cycles. FitnessHub should plan for possible revenue slowdowns after peak periods and use these trends to guide budgeting and growth decisions.

## CAC vs. LTV Analysis
The CAC vs. LTV analysis shows that both the 2024 and 2025 cohorts recover customer acquisition cost around December of their cohort year. In both cases, cumulative revenue rises steadily and eventually crosses the Total CAC reference line near year-end.

- The 2024 cohort reaches CAC break-even around December 2024
- The 2025 cohort reaches CAC break-even around December 2025

This suggests that FitnessHub currently operates with an approximately one-year CAC payback period. Improving retention or increasing early customer value could shorten this recovery time and improve profitability.

## Business Recommendations
Based on the analysis, the following actions may help improve performance:

- Focus retention efforts during months 2 to 3, when churn risk appears highest
- Strengthen onboarding and early customer engagement to reduce cancellations before month 3
- Monitor seasonal revenue patterns and prepare for slower periods after year-end peaks
- Continue tracking CAC payback by cohort to evaluate whether acquisition spending remains sustainable

## Repository Structure
```
fitness-subscription-analytics/
├── README.md
├── report.twbx
├── data/
│   └── Fitness_Subscriptions_Dataset.xlsx
└── screenshots/
    ├── cohort_analysis.png
    ├── revenue_forecast.png
    ├── cac_vs_ltv.png
    └── data_model.png
```

## Tableau Workbook Pages
The Tableau workbook includes the following report pages:
- Customer Cohort
- Revenue Forecast
- CAC vs LTV

## Conclusion
This analysis shows that FitnessHub’s biggest retention challenge occurs early in the customer lifecycle, especially between months 2 and 3. Revenue growth has been strong historically, but the forecast suggests possible seasonality and future volatility. Both the 2024 and 2025 cohorts recover CAC by December, which means profitability depends heavily on retaining customers long enough to reach that payback point.
