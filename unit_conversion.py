import pandas as pd
from input_output import read_csv_file

def build_conversion_matrix(year):
  filename = "./data/solar_module_data.csv"
  variables = read_csv_file(filename, year)
  Wp_per_m2 = 1000
  # Conversion constants for poly-Si

  # Extract constants
  kg_per_cell = variables['kg_per_cell']
  cell_active_area = variables['cell_active_area']
  efficiency = variables['efficiency']
  cell_to_module_ratio = variables.get('cell_to_module_ratio', 0.98)
  cells_per_module = variables.get('cells_per_module', 60)

  wp_per_cell = cell_active_area * efficiency * Wp_per_m2
  cells_per_kg = 1 / kg_per_cell
  kg_per_module = kg_per_cell * cells_per_module
  wp_per_module = wp_per_cell * cells_per_module * cell_to_module_ratio

  units = ['kg', 'wafer', 'cell', 'module', 'Wp']
  conversion_matrix = pd.DataFrame(1.0, index=units, columns=units)

  units = ['kg', 'wafer', 'cell', 'module', 'Wp']
  conversion_matrix = pd.DataFrame(1.0, index=units, columns=units)

  conversions = {
    ('kg', 'cell'): kg_per_cell,
    ('wafer', 'cell'): 1,
    ('kg', 'wafer'): kg_per_cell,
    ('module', 'cell'): 1 / cells_per_module,
    ('module', 'wafer'): 1 / cells_per_module,
    ('kg', 'module'): kg_per_module,
    ('Wp', 'cell'): wp_per_cell,
    ('Wp', 'wafer'): wp_per_cell,
    ('Wp', 'module'): wp_per_module,
    ('Wp', 'kg'): wp_per_cell / kg_per_cell,
  }
  for (from_unit, to_unit), factor in conversions.items():
    conversion_matrix.at[from_unit, to_unit] = factor
    conversion_matrix.at[to_unit, from_unit] = 1 / factor

  return conversion_matrix

def convert_dataframe_units(df, target_unit, conversion_matrix):
  """Convert the units of a dataframe using the conversion matrix."""
  df_converted = df.copy()

  def convert_row(row):
    from_unit = row['Unit']
    if from_unit == target_unit:
      return row
    factor = conversion_matrix.at[from_unit, target_unit]
    row['Process Cost'] *= factor
    low, high = row['Process Cost Range']
    row['Process Cost Range'] = (low * factor, high * factor)
    row['Unit'] = target_unit
    return row

  return df_converted.apply(convert_row, axis=1)

