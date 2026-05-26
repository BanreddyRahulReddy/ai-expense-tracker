"""
forecaster.py

PURPOSE: Given a user's past expense history (list of amounts with dates),
predict how much they will spend next month using Linear Regression.

Simple idea: if you spent 1000, 1200, 1100 in last 3 months,
             the model predicts ~1150 for next month.
"""

import numpy as np
from sklearn.linear_model import LinearRegression


def forecast_next_month(monthly_totals: list) -> dict:
    """
    Input:  monthly_totals = list of total amounts per month
            e.g. [1000, 1200, 950, 1100]  (oldest → newest)

    Output: predicted amount for next month + trend direction

    Example:
        forecast_next_month([1000, 1100, 1200])
        → {"predicted": 1290.0, "trend": "increasing", "change_pct": 7.5}
    """

    if len(monthly_totals) < 2:
        # Not enough data to predict
        return {
            "predicted": monthly_totals[0] if monthly_totals else 0,
            "trend": "insufficient data",
            "change_pct": 0
        }

    # X = month numbers [1, 2, 3, ...]  Y = spending amounts
    X = np.array(range(1, len(monthly_totals) + 1)).reshape(-1, 1)
    y = np.array(monthly_totals)

    # Train the regression model
    reg = LinearRegression()
    reg.fit(X, y)

    # Predict the NEXT month (month number = len + 1)
    next_month_num = np.array([[len(monthly_totals) + 1]])
    predicted = round(float(reg.predict(next_month_num)[0]), 2)

    # Calculate % change from last month to predicted
    last_month = monthly_totals[-1]
    change_pct = round(((predicted - last_month) / last_month) * 100, 1) if last_month else 0

    # Determine trend direction
    if change_pct > 5:
        trend = "increasing"
    elif change_pct < -5:
        trend = "decreasing"
    else:
        trend = "stable"

    return {
        "predicted": max(0, predicted),   # Can't predict negative spending
        "trend": trend,
        "change_pct": change_pct
    }