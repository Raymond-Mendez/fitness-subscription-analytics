# Fitness Subscription Analytics

## Project overview
This project analyzes subscription data for a fitness business using Tableau. The goal is to understand customer cancellations, forecast revenue, and compare customer acquisition cost (CAC) with lifetime value (LTV).

## Tools used
- Tableau
- Excel dataset with "customers" and "transactions" worksheets

## Business questions
1. After how many months do customers usually cancel their subscriptions?
2. What is the expected subscription revenue over the next 12 months?
3. How long does it take for the 2024 and 2025 cohorts to recover CAC?

## Key findings

### Customer cohort analysis
The cohort analysis shows that many customers cancel within the first few months after signing up. Retention drops early, which suggests that churn happens relatively soon in the customer lifecycle.

### Revenue forecast
The revenue forecast shows expected subscription revenue for the next 12 months based on historical monthly trends. The forecast suggests continued revenue growth and shows signs of seasonality in the data.

### CAC vs. LTV
The CAC vs. LTV analysis compares how long it takes different customer cohorts to recover acquisition cost.

- The 2024 cohort reaches CAC break-even around January 2025
- The 2025 cohort reaches CAC break-even around June 2025

This suggests the 2025 cohort recovers CAC faster than the 2024 cohort.

## Repository structure
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

## Tableau pages
The Tableau workbook includes:
- Customer Cohort
- Revenue Forecast
- CAC vs LTV

## Submission
This repository contains the Tableau workbook, dataset, screenshots, and README for the fitness subscription analytics project.
