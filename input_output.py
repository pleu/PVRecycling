import pandas as pd

def read_csv_file(filename, year):
  df = pd.read_csv(filename)

  # Filter rows for the given year
  rows = df[df['Year'] == year]
  if rows.empty:
    raise ValueError(f"No data found for year {year} in {filename}")

  # Convert each row to a dictionary and return as a list
  return rows.drop(columns='Year').to_dict(orient='records')