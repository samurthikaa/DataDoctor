import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame):

    # 🔹 Remove duplicates
    df = df.drop_duplicates()

    # 🔹 Convert numeric safely
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            continue

    # 🔹 Fix numeric columns
    for col in df.select_dtypes(include=['number']).columns:

        if col.lower() == 'age':
            df[col] = df[col].clip(0, 100)

        df[col] = df[col].fillna(df[col].mean())
        df[col] = df[col].round(0)

    # 🔹 Fix text columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip().str.lower()

        df[col] = df[col].replace(
            ['nan', 'none', 'not_available', 'not_availa'],
            'unknown'
        )

    # 🔹 Fix salary
    if 'salary' in df.columns:
        df['salary'] = pd.to_numeric(df['salary'], errors='coerce')
        df['salary'] = df['salary'].fillna(df['salary'].mean()).round(0)

    # 🔹 Fix email (SMART)
    if 'email' in df.columns:
        def fix_email(x):
            if not isinstance(x, str) or x.strip() == '':
                return 'unknown@email.com'

            x = x.strip().lower()

            if '@' in x and '.' not in x:
                return x + ".com"

            if '@' not in x:
                return 'unknown@email.com'

            return x

        df['email'] = df['email'].apply(fix_email)

    # 🔹 Normalize country
    if 'country' in df.columns:
        df['country'] = df['country'].replace({
            'usa': 'united states',
            'us': 'united states',
            'uk': 'united kingdom',
            'india': 'india'
        })

    return df