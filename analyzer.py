import pandas as pd

def analyze_data(df: pd.DataFrame):
    issues = []

    # 🔹 Missing values
    missing = df.isnull().sum()
    for col, count in missing.items():
        if count > 0:
            issues.append({
                "type": "Missing Values",
                "column": col,
                "count": int(count)
            })

    # 🔹 Duplicate rows
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        issues.append({
            "type": "Duplicate Rows",
            "column": "Multiple",  # ✅ FIX (important for frontend)
            "count": int(duplicates)
        })

    # 🔹 Outliers (IQR)
    for col in df.select_dtypes(include=['number']).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]

        if not outliers.empty:
            issues.append({
                "type": "Outliers",
                "column": col,
                "count": int(len(outliers))
            })

    # 🔹 FIXED text check (SAFE)
    for col in df.select_dtypes(include=['object']).columns:
        try:
            clean_col = df[col].dropna().astype(str)

            if clean_col.str.lower().nunique() != clean_col.nunique():
                issues.append({
                    "type": "Inconsistent Text",
                    "column": col,
                    "count": int(len(clean_col))
                })

        except Exception:
            continue  # skip problematic columns

    return issues