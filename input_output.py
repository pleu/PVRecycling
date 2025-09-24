import pandas as pd
import os

def read_conversion_constants(filename, year):
  df = pd.read_csv(filename)
  df.columns = [col.lower() for col in df.columns]   
  rows = df[df['year'] == year]                      

  panel = os.getenv('SOLAR_PANEL', '').strip().lower()
  if 'solar_panel' in df.columns and panel:
    rows = rows[rows['solar_panel'].astype(str).str.strip().str.lower() == panel]

  if rows.empty:
    raise ValueError(f"No data found for year {year}" + (f" and solar_panel = '{panel}'" if panel else ""))
  return rows.drop(columns = [c for c in ['year','solar_panel'] if c in rows.columns]).iloc[0].to_dict()

def read_year_filtered_data(filename, year, converters = None):
  df = pd.read_csv(filename, converters = converters)
  year_col = 'Year' if 'Year' in df.columns else 'year'
  rows = df[df[year_col] == year]
  if rows.empty:
    raise ValueError(f"No rows found for year {year} in {filename}")
  return rows.drop(columns = year_col).reset_index(drop = True)

def read_efficiency_data(year, path="./data/efficiency_data.csv"):
    df = read_year_filtered_data(path, year, {"Efficiency Range": eval})
  
    panel = os.getenv('SOLAR_PANEL', '').strip().lower()
    if 'solar_panel' in df.columns and panel:
        df = df[df['solar_panel'].astype(str).str.strip().str.lower() == panel]

    if df.empty:
        raise ValueError(f"No efficiency rows for year {year}" + (f" and solar_panel='{panel}'" if panel else ""))
    return df.drop(columns=[c for c in ['solar_panel'] if c in df.columns]).reset_index(drop=True)

# def read_production_steps(year): df = read_year_filtered_data("./data/production_step_data.csv", year,{"Process Cost Range": eval})

def read_production_steps(year, data_path="data/production_step_data.csv"):
    df = pd.read_csv(data_path)
    return df[df["Year"] == year]
