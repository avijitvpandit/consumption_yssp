import pandas as pd
import numpy as np
import re
from pathlib import Path
import matplotlib.pyplot as plt

DATA_FILE = Path('data/processed/gdd_cleaned_panel.csv')
OUT_FIG = Path('outputs/plots/norway_generational_trend.png')


def age_midpoint(age_group: str) -> float:
    numbers = [int(n) for n in re.findall(r"\d+", str(age_group))]
    if numbers:
        return float(sum(numbers)) / len(numbers)
    return np.nan


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"{DATA_FILE} not found. Please run clean_data.py first.")

    df = pd.read_csv(DATA_FILE)
    df = df[(df['country'] == 'Norway') & df['food'].isin(['Red meat', 'Vegetables'])].copy()

    df['generation'] = pd.cut(
        df['cohort'],
        bins=[1965, 1980, 1996],
        labels=['Gen X', 'Millennials'],
        right=True,
        include_lowest=True,
    )
    df = df.dropna(subset=['generation'])

    summary = (
        df.groupby(['age_group', 'cohort', 'food', 'generation'])['median']
        .mean()
        .reset_index()
    )
    summary['age_mid'] = summary['age_group'].apply(age_midpoint)

    OUT_FIG.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 6))

    for (gen, food), group in summary.groupby(['generation', 'food']):
        linestyle = '-' if gen == 'Gen X' else '--'
        group_sorted = group.sort_values('age_mid')
        ax.plot(
            group_sorted['age_mid'],
            group_sorted['median'],
            label=f"{gen} - {food}",
            linestyle=linestyle,
        )

    ax.set_xlabel('Age (midpoint)')
    ax.set_ylabel('Daily energy intake')
    ax.set_title('Observed Generational Dietary Trend in Norway')
    ax.legend()

    fig.tight_layout()
    fig.savefig(OUT_FIG, dpi=300)
    plt.close(fig)
    print(f"\n✅ Figure saved to {OUT_FIG.resolve()}")


if __name__ == '__main__':
    main()
