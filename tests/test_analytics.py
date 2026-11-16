import pandas as pd

import analytics


def make_csv(tmp_path):
    df = pd.DataFrame(
        {
            "Branch": ["A", "A", "B", "B"],
            "Product line": ["Food", "Sports", "Food", "Sports"],
            "Unit price": [10.0, 20.0, 30.0, 40.0],
            "Sales": [100.0, 200.0, 300.0, 400.0],
            "Date": ["1/5/2019", "1/6/2019", "1/7/2019", "1/8/2019"],
            "Payment": ["Cash", "Cash", "Ewallet", "Cash"],
            "Rating": [9.0, 7.0, 8.5, 6.0],
        }
    )
    path = tmp_path / "sales.csv"
    df.to_csv(path, index=False)
    return path


def test_analytics_results(tmp_path):
    df = analytics.load_data(make_csv(tmp_path))
    assert analytics.summary(df)["unit_price"]["max"] == 40.0
    assert analytics.sales_by_branch(df)["top_branch"] == "B"
    assert analytics.rating_by_product_line(df)["top_product_line"] == "Food"
    assert analytics.payment_counts(df)["most_used"] == "Cash"
    assert analytics.pivot(df)["Food"]["A"] == 100.0