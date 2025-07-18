import pandas as pd

def read_csv_file(filename, year):
  df = pd.read_csv(filename)

  # Filter rows for the given year
  rows = df[df['year'] == year]
  if rows.empty:
    raise ValueError(f"No data found for year {year} in {filename}")

  # Convert each row to a dictionary and return as a list
  return rows.drop(columns='year').iloc[0].to_dict()