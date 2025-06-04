📁 Data Folder Structure and Usage

This folder contains raw and processed data used in the GDD (Global Dietary Database) analysis pipeline. Data files are not tracked by Git to avoid size limitations and ensure reproducibility.

📂 Folder Structure

/data
│
├── raw/                         # Raw unprocessed data
│   └── GDD/
│       └── Country-level estimates/   # All original CSV files per country
│		#also others from the GDD
├── processed/                   # Cleaned and transformed panel data
│   └── gdd_cleaned_panel.csv    # Final combined panel output (not versioned)
│
├── sample.csv                   #  Small data sample for reference/testing from the processed file

📥 Raw Data Instructions

To use the cleaning pipeline:

Download the GDD country-level files.

Place them in:

data/raw/GDD/Country-level estimates/

These files are excluded from Git and must be manually placed.

⚙️ How to Regenerate Processed Data

Run the following from the project root:

python src/clean_data.py

This will create data/processed/gdd_cleaned_panel.csv by:

Reading each GDD country CSV

Filtering and cleaning demographics

Mapping variables to food groups

Saving an efficient combined panel

⚠️ Git Ignore Policy

To prevent accidental uploads to GitHub:

/data/raw/ and /data/processed/ are excluded via .gitignore

Only small files like sample.csv can be committed for documentation/testing