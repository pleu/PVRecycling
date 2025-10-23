import pandas as pd
from input_output import read_conversion_constants


def build_conversion_matrix(year, data_path="./data/solar_module_data.csv"):
    filename = data_path
    variables = read_conversion_constants(filename, year)
    Wp_per_m2 = 1000.0

    # Extract constants
    kg_per_cell = variables["kg_per_cell"]
    cell_active_area = variables["cell_active_area"]
    efficiency = variables["efficiency"]
    cell_to_module_ratio = variables["cell_to_module_ratio"]
    cells_per_module = variables.get("cells_per_module", 60)

    # Detect half-cell
    cells_are_half = cells_per_module >= 100
    full_cells_in_module = (cells_per_module // 2) if cells_are_half else cells_per_module

    # Normalize to FULL-cell 
    full_cell_area = cell_active_area * 2.0 if cells_are_half else cell_active_area
    full_cell_kg = kg_per_cell * 2.0 if cells_are_half else kg_per_cell

    full_cell_wp = full_cell_area * efficiency * Wp_per_m2
    
    counted_cell_wp = (full_cell_wp / 2.0) if cells_are_half else full_cell_wp

    # Mass and module-level power
    kg_per_module = full_cell_kg * full_cells_in_module
    wp_per_module = full_cell_wp * full_cells_in_module * cell_to_module_ratio

    # Build matrix
    units = ["kg", "wafer", "cell", "module", "Wp"]
    conversion_matrix = pd.DataFrame(1.0, index=units, columns=units)

    conversions = {
        ("kg", "cell"): full_cell_kg,
        ("wafer", "cell"): 1.0,
        ("kg", "wafer"): full_cell_kg,
        ("module", "cell"): 1.0 / cells_per_module,
        ("module", "wafer"): 1.0 / cells_per_module,
        ("kg", "module"): kg_per_module,
        ("Wp", "cell"): counted_cell_wp,
        ("Wp", "wafer"): full_cell_wp,
        ("Wp", "module"): wp_per_module,
        ("Wp", "kg"): full_cell_wp / full_cell_kg,
    }

    for (from_unit, to_unit), factor in conversions.items():
        conversion_matrix.at[from_unit, to_unit] = factor
        conversion_matrix.at[to_unit, from_unit] = 1.0 / factor

    return conversion_matrix


def convert_dataframe_units(df, target_unit, conversion_matrix):
    df_converted = df.copy()

    def norm(u):
        return str(u).strip() if pd.notna(u) else u

    tgt = norm(target_unit)

    def convert_row(row):
        from_unit = norm(row.get("Unit", None))
        if from_unit is None or from_unit == tgt:
            row["Unit"] = tgt if from_unit is not None else tgt
            return row

        factor = conversion_matrix.at[from_unit, tgt]
        row["Process Cost"] = row["Process Cost"] * factor

        for bound in ["Process Cost Min", "Process Cost Max"]:
            if bound in row and pd.notna(row[bound]):
                row[bound] = row[bound] * factor

        row["Unit"] = tgt
        return row

    return df_converted.apply(convert_row, axis=1)
