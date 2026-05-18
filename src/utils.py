import pandas as pd

def facts_to_dataframe(facts):
    df = pd.DataFrame(facts).copy()
    if not df.empty and "as_of" in df.columns:
        df["as_of"] = df["as_of"].astype(str)
    return df

def build_distribution_dataframe(distribution):
    order = [
        "Above national average",
        "Same as national average",
        "Below national average"
    ]
    rows = [{"comparison": label, "count": distribution.get(label, 0)} for label in order]
    return pd.DataFrame(rows)

def get_fact_value(facts_df, label):
    if facts_df.empty or "label" not in facts_df.columns or "value" not in facts_df.columns:
        return "N/A"
    matched = facts_df.loc[facts_df["label"] == label, "value"]
    if matched.empty:
        return "N/A"
    return str(matched.iloc[0])

def freshness_order():
    return ["current", "official_historical", "historical_case_study"]
