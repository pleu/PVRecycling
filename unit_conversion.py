import pandas as pd
from input_output import read_conversion_constants

# def build_conversion_matrix(year): filename = "./data/solar_module_data.csv"

import pandas as pd
from input_output import read_conversion_constants

# TECH comes from your config cell:
# TECH = "mono"  # or "bi"

def build_conversion_matrix(year, data_path="./data/solar_module_data.csv", tech="mono"):
  filename = data_path
  variables = read_conversion_constants(filename, year)
  Wp_per_m2 = 1000

  # Choose efficiency column based on tech
  eff_key = "efficiency_bi" if tech in ("bi", "bifacial") else "efficiency_mono"
  
  # Compatible if the function still returns 'efficiency'
  efficiency = variables.get(eff_key, variables.get("efficiency"))
  if efficiency is None:
      raise KeyError(f"Expected '{eff_key}' (or 'efficiency') in read_conversion_constants output.")
  
  # normalize if saved % instead of a fraction
  if efficiency > 1.0:
      efficiency = efficiency / 100.0

  # Extract the rest
  kg_per_cell = variables['kg_per_cell']
  cell_active_area = variables['cell_active_area']
  cell_to_module_ratio = variables['cell_to_module_ratio']
  cells_per_module = variables['cells_per_module'] if 'cells_per_module' in variables else 60

  # Power per cell (Wp)
  wp_per_cell = cell_active_area * efficiency * Wp_per_m2
  cells_per_kg = 1 / kg_per_cell
  kg_per_module = kg_per_cell * cells_per_module
  wp_per_module = wp_per_cell * cells_per_module * cell_to_module_ratio

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
    row['Process Cost Min'] *= factor
    row['Process Cost Max'] *= factor
    row['Unit'] = target_unit
    return row

  return df_converted.apply(convert_row, axis=1)
