# Clean and combine all GDD country-level files into one memory-efficient panel
# Also generate a small sample (~5 rows) for documentation/testing
#%%
import pandas as pd
import os
from pathlib import Path
import numpy as np
import pycountry

# Define paths
data_path = Path("data/raw/GDD/Country-level estimates")
out_path = Path("data/processed/gdd_cleaned_panel.csv")
sample_path = Path("data/sample.csv")

# EU27 + EEA ISO3 codes
EEA_ISO3 = [
    'AUT', 'BEL', 'BGR', 'HRV', 'CYP', 'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'DEU', 'GRC',
    'HUN', 'IRL', 'ITA', 'LVA', 'LTU', 'LUX', 'MLT', 'NLD', 'POL', 'PRT', 'ROU', 'SVK',
    'SVN', 'ESP', 'SWE', 'NOR', 'ISL', 'LIE'
]

# Manually defined varnum → food description map
var_map = {
    1: "Fruits", 2: "Vegetables", 3: "Legumes", 4: "Nuts and seeds", 5: "Whole grains",
    6: "Refined grains", 7: "Red meat", 8: "Processed meat", 9: "Poultry", 10: "Fish",
    11: "Eggs", 12: "Milk", 13: "Cheese", 14: "Yogurt", 15: "Sugar-sweetened beverages",
    16: "100% fruit juice", 17: "Alcohol", 18: "Sodium", 19: "Calcium", 20: "Fiber",
    21: "Iron", 22: "Vitamin A", 23: "Vitamin C", 24: "Trans fats", 25: "Saturated fats",
    26: "Polyunsaturated fats", 27: "Monounsaturated fats", 28: "Total fats",
    29: "Total energy intake", 30: "Cholesterol", 31: "Added sugars", 32: "Processed foods",
    33: "Unprocessed foods", 34: "Oils", 35: "Starchy vegetables", 36: "Other beverages"
}

# Mappings
female_map = {0: 'Male', 1: 'Female'}
edu_map = {1: 'Primary', 2: 'Secondary', 3: 'Tertiary'}

# Read all files in the directory first. EU filtering will happen after
# concatenating the individual files.
csv_files = list(data_path.glob("*.csv"))

# Clear previous output files
for p in [out_path, sample_path]:
    if p.exists():
        p.unlink()

# Collect cleaned frames for each file
cleaned_frames = []

for f in csv_files:
    try:
        df = pd.read_csv(
            f,
            usecols=lambda x: x in ['female', 'edu', 'age', 'iso3', 'year', 'varnum', 'median']
        )
        mask = (
            df['female'].isin([0, 1])
            & df['edu'].isin([1, 2, 3])
            & (df['age'] < 100)
            & (~df['female'].isna())
            & (~df['edu'].isna())
            & (~df['age'].isna())
        )
        df = df[mask].copy()
        df['iso3'] = df['iso3'].astype(str)
        cleaned_frames.append(df)
    except Exception as e:
        print(f"Error processing {f.name}: {e}")

if not cleaned_frames:
    raise RuntimeError("No data files were processed successfully.")

# Concatenate all cleaned data and then keep only EU/EEA countries
df = pd.concat(cleaned_frames, ignore_index=True)
df = df[df['iso3'].isin(EEA_ISO3)]

df['sex'] = df['female'].map(female_map)
df['education'] = df['edu'].map(edu_map)
df['country'] = df['iso3'].apply(lambda x: pycountry.countries.get(alpha_3=x).name)
df['food'] = df['varnum'].map(var_map)
df = df.rename(columns={'median': 'value'})

output = df.melt(
    id_vars=['country', 'iso3', 'year', 'sex', 'education', 'age'],
    var_name='food',
    value_name='value',
)

output.to_csv(out_path, index=False)

# Create sample after entire output is generated
output.sample(5, random_state=42).to_csv(sample_path, index=False)

print(f"\n✅ Cleaned panel saved to {out_path.resolve()}")
print(f"📄 Sample file saved to {sample_path.resolve()}")


# %%
