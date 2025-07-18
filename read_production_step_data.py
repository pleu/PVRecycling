import pandas as pd
from input_output import read_csv_file

def read_production_steps(filename, year):
  df = pd.read_csv(filename, converters={"Process Cost Range": eval})

  # Match year column case
  year_col = 'Year' if 'Year' in df.columns else 'year'

  rows = df[df[year_col] == year]
  if rows.empty:
    raise ValueError(f"No data found for year {year} in {filename}")

  return rows.drop(columns=year_col).reset_index(drop=True)