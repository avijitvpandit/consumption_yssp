import pandas as pd
from pathlib import Path

DATA_FILE = Path('data/processed/gdd_cleaned_panel.csv')
OUT_FILE = Path('data/processed/red_meat_cohort_education.csv')


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"{DATA_FILE} not found. Please run clean_data.py first.")

    df = pd.read_csv(DATA_FILE)
    df = df[df['food'] == 'Red meat'].copy()
    df = df.dropna(subset=['age', 'year', 'education', 'value'])

    df['birth_year'] = df['year'] - df['age']
    df['cohort'] = (df['birth_year'] // 10) * 10

    summary = (
        df.groupby(['cohort', 'education'])['value']
        .mean()
        .reset_index()
        .rename(columns={'value': 'mean_intake'})
        .sort_values(['cohort', 'education'])
    )

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUT_FILE, index=False)
    print(summary.head())
    print(f"\n✅ Cohort analysis saved to {OUT_FILE.resolve()}")


if __name__ == '__main__':
    main()
