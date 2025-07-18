def read_production_step_data(year):
  """Load conversion constants for the given year from a wide-format CSV."""
  filename = "./data/solar_module_data.csv"
  df = pd.read_csv(filename)

  # Find the row matching the year
  row = df[df['year'] == year]
  if row.empty:
    raise ValueError(f"No data found for year {year}")

  # Drop the 'year' column and convert the rest to a dictionary
  constants = row.drop(columns='year').iloc[0].to_dict()
  return constants