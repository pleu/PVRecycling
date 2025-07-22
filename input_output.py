import pandas as pd

def read_conversion_constants(filename, year):
  df = pd.read_csv(filename)
  df.columns = [col.lower() for col in df.columns]  # make column names lowercase
  rows = df[df['year'] == year]                     # match the 'year' column
  if rows.empty:
    raise ValueError(f"No data found for year {year}")
  return rows.drop(columns='year').iloc[0].to_dict()

def read_year_filtered_data(filename, year, converters=None):
  df = pd.read_csv(filename, converters=converters)
  year_col = 'Year' if 'Year' in df.columns else 'year'
  rows = df[df[year_col] == year]
  if rows.empty:
    raise ValueError(f"No {data_label} found for year {year} in {filename}")
  return rows.drop(columns=year_col).reset_index(drop=True)

def read_efficiency_data(year):
  df = read_year_filtered_data("./data/efficiency_data.csv", year,{"Efficiency Range": eval})
  return df

def read_production_steps(year):
  df = read_year_filtered_data("./data/production_step_data.csv", year,{"Process Cost Range": eval})
  return df


