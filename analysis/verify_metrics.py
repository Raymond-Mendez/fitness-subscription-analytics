"""Recompute the headline metrics for the FitnessHub subscription analysis.

The Tableau workbook (report.twbx) is the presentation layer. This script is the audit trail: it
recalculates every number quoted in the README straight from the source workbook so the figures can
be verified and re-run, and it regenerates the two cohort charts that Tableau plotted on the wrong
axis (see the "Correction" section of the README).

Usage:
    python analysis/verify_metrics.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "Fitness_Subscriptions_Dataset.xlsx"
SHOTS = ROOT / "screenshots"


def load():
    """Read both worksheets and derive signup cohorts from first subscription charge.

    The customers sheet has no signup date, so the cohort a customer belongs to is the month of
    their first Subscription transaction.
    """
    book = pd.ExcelFile(DATA)
    customers = book.parse("customers")
    transactions = book.parse("transactions")

    subs = transactions[transactions["Transaction_Type"] == "Subscription"].copy()
    subs["month"] = subs["Transaction_Date"].dt.to_period("M")

    cohort = subs.groupby("Customer_ID")["month"].min().rename("cohort")
    subs = subs.join(cohort, on="Customer_ID")
    # months since signup (0 = signup month)
    subs["month_index"] = (subs["month"] - subs["cohort"]).apply(lambda offset: offset.n)

    return customers, transactions, subs


def retention(subs):
    """Weighted retention curve across all cohorts, by months since signup."""
    cohort_size = subs.groupby("Customer_ID")["cohort"].first().value_counts().sort_index()
    active = subs.groupby(["cohort", "month_index"])["Customer_ID"].nunique().unstack()
    curve = (active.sum() / cohort_size.sum()).sort_index()

    lifespan = subs.groupby("Customer_ID")["month_index"].max()
    return curve, lifespan, cohort_size


def cac_payback(customers, subs):
    """Cumulative cohort revenue against cohort CAC, measured in months since signup.

    This is the fix for the original chart, which plotted cumulative revenue on a calendar axis
    against a full-cohort CAC total and therefore appeared to break even every December.
    """
    cac_by_customer = customers.set_index("Customer_ID")["CAC"]
    cohort_year = subs.groupby("Customer_ID")["cohort"].first().dt.year

    results = {}
    for year in sorted(cohort_year.unique()):
        members = cohort_year[cohort_year == year].index
        total_cac = cac_by_customer.reindex(members).sum()
        cumulative = (
            subs[subs["Customer_ID"].isin(members)]
            .groupby("month_index")["Revenue"]
            .sum()
            .cumsum()
        )
        reached = cumulative[cumulative >= total_cac]
        results[year] = {
            "customers": len(members),
            "total_cac": total_cac,
            "cumulative_revenue": cumulative,
            "breakeven_month": int(reached.index[0]) if len(reached) else None,
            "months_observed": int(cumulative.index.max()),
        }
    return results


def chart_retention(curve, path):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    months = curve.index[:13]
    values = curve.loc[months] * 100
    ax.plot(months, values, marker="o", color="#1f4e79", linewidth=2)
    ax.axvspan(1.5, 3.5, color="#d9534f", alpha=0.10)
    ax.annotate(
        "sharpest drop:\nmonth 2 to 3",
        xy=(3, values.loc[3]),
        xytext=(4.4, values.loc[3] + 18),
        arrowprops=dict(arrowstyle="->", color="#d9534f"),
        color="#d9534f",
        fontsize=9,
    )
    ax.set_title("Subscriber retention by months since signup (all cohorts)", fontsize=12)
    ax.set_xlabel("Months since signup")
    ax.set_ylabel("Still subscribed (%)")
    ax.set_ylim(0, 105)
    ax.set_xticks(list(months))
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def chart_payback(results, path):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = {2024: "#1f4e79", 2025: "#e07b39"}

    for year, info in results.items():
        cumulative = info["cumulative_revenue"]
        color = colors.get(year, "#666666")
        ax.plot(
            cumulative.index,
            cumulative.values / 1000,
            marker="o",
            markersize=4,
            color=color,
            label=f"{year} cohort - cumulative revenue",
        )
        ax.axhline(
            info["total_cac"] / 1000,
            color=color,
            linestyle="--",
            linewidth=1.2,
            label=f"{year} cohort - total CAC",
        )
        if info["breakeven_month"] is not None:
            month = info["breakeven_month"]
            ax.scatter([month], [cumulative.loc[month] / 1000], s=110,
                       facecolor="white", edgecolor=color, zorder=5)
            ax.annotate(
                f"break-even\nmonth {month}",
                xy=(month, cumulative.loc[month] / 1000),
                xytext=(month + 0.6, cumulative.loc[month] / 1000 - 190),
                arrowprops=dict(arrowstyle="->", color=color),
                color=color,
                fontsize=9,
            )

    ax.set_title("CAC payback by cohort, measured in months since signup", fontsize=12)
    ax.set_xlabel("Months since signup")
    ax.set_ylabel("Cumulative subscription revenue ($000s)")
    ax.grid(axis="y", alpha=0.3)
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main():
    customers, transactions, subs = load()
    curve, lifespan, cohort_size = retention(subs)

    print("=" * 62)
    print("FITNESSHUB SUBSCRIPTION METRICS")
    print("=" * 62)
    print(f"Customers:            {len(customers):,}")
    print(f"Transactions:         {len(transactions):,}")
    print(f"Date range:           {transactions['Transaction_Date'].min():%Y-%m-%d} "
          f"to {transactions['Transaction_Date'].max():%Y-%m-%d}")
    print(f"Total revenue:        ${transactions['Revenue'].sum():,.0f}")
    print(f"Total CAC spend:      ${customers['CAC'].sum():,.0f}")
    print(f"Average CAC:          ${customers['CAC'].mean():,.2f}"
          f"   (median ${customers['CAC'].median():,.2f})")

    print("\nRETENTION BY MONTHS SINCE SIGNUP")
    for month in range(0, 7):
        print(f"  month {month}: {curve.loc[month] * 100:5.1f}%")
    print(f"  Median months active: {lifespan.median():.0f}")
    drop = (curve.loc[2] - curve.loc[3]) * 100
    print(f"  Largest single-month drop: month 2 -> 3, {drop:.1f} percentage points")

    print("\nREVENUE BY YEAR")
    by_year = transactions.groupby(transactions["Transaction_Date"].dt.year)["Revenue"].sum()
    for year, revenue in by_year.items():
        print(f"  {year}: ${revenue:,.0f}")
    monthly = transactions.groupby(transactions["Transaction_Date"].dt.to_period("M"))["Revenue"].sum()
    print(f"  Peak month: {monthly.idxmax()} at ${monthly.max():,.0f}")
    print(f"  Final month in data: {monthly.index[-1]} at ${monthly.iloc[-1]:,.0f}")

    print("\nCAC PAYBACK BY COHORT YEAR (months since signup)")
    results = cac_payback(customers, subs)
    for year, info in results.items():
        status = (f"break-even at month {info['breakeven_month']}"
                  if info["breakeven_month"] is not None
                  else f"NOT yet recovered after {info['months_observed']} observed months")
        print(f"  {year} cohort: {info['customers']:,} customers, "
              f"CAC ${info['total_cac']:,.0f} -> {status}")
        print(f"    cumulative revenue to date: "
              f"${info['cumulative_revenue'].max():,.0f}")

    SHOTS.mkdir(exist_ok=True)
    chart_retention(curve, SHOTS / "retention_curve_verified.png")
    chart_payback(results, SHOTS / "cac_payback_verified.png")
    print(f"\nCharts written to {SHOTS.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
