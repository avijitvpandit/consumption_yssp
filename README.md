# Consumption YSSP

This repository processes Global Dietary Database (GDD) data. Raw GDD CSV files are not tracked in Git. The cleaning pipeline combines these files into `data/processed/gdd_cleaned_panel.csv`.

## Scripts

- `scripts/clean_data.py` – cleans the raw GDD country files into a single panel.
- `scripts/analyze_red_meat.py` – analyzes cohort-based Red meat intake across education levels.

## Cohort-Based Red Meat Analysis

Run the analysis after generating the cleaned panel:

```bash
python scripts/analyze_red_meat.py
```

The script will create `data/processed/red_meat_cohort_education.csv` with mean intake by birth cohort (decades) and education level.
