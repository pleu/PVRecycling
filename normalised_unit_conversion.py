#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Usage:
# from normalised_unit_conversion import (
#     normalised_read_production_steps,
#     normalised_build_conversion_matrix
# )

import pandas as pd
from input_output import read_production_steps
from unit_conversion import build_conversion_matrix

# Conversion factors to standard units
mass_factors = {
    'kg': 1.0,
    'g': 1e-3,
    'gram': 1e-3,
    'grams': 1e-3,
    'mg': 1e-6,
    'milligram': 1e-6,
    'milligrams': 1e-6,
    'lb': 0.453592,
    'lbs': 0.453592,
}

area_factors = {
    'm2': 1.0,
    'm^2': 1.0,
    'cm2': 1e-4,
    'cm^2': 1e-4,
    'mm2': 1e-6,
    'mm^2': 1e-6,
}

power_factors = {
    'wp': 1.0,
    'w': 1.0,
    'kw': 1e3,
    'mw': 1e6,
    'kwp': 1e3,
    'mwp': 1e6,
}

def to_standard_rate(value, unit):
    """Convert $/unit → standard rates ($/kg, $/m2, $/Wp)"""
    if unit is None or unit == '' or pd.isna(unit):
        return value

    u = str(unit).strip().lower().replace('usd', '$').replace('per ', '/')
    denom = u.split('/')[-1] if '/' in u else u

    if denom in mass_factors:
        return value / mass_factors[denom]
    if denom in area_factors:
        return value / area_factors[denom]
    if denom in power_factors:
        return value / power_factors[denom]
    return value  # leave unchanged if unknown

def normalise_input_data(df, cost_column='Process Cost', unit_column=None, cost_unit=None):
    """Normalize cost data to standard rates"""
    out = df.copy()

    def apply_row(row, unit):
        row[cost_column] = to_standard_rate(row[cost_column], unit)
        min_col, max_col = f'{cost_column} Min', f'{cost_column} Max'
        if min_col in row and pd.notna(row[min_col]):
            row[min_col] = to_standard_rate(row[min_col], unit)
        if max_col in row and pd.notna(row[max_col]):
            row[max_col] = to_standard_rate(row[max_col], unit)
        return row

    if unit_column and unit_column in out.columns:
        out = out.apply(lambda r: apply_row(r, r[unit_column]), axis=1)
    elif cost_unit:
        out = out.apply(lambda r: apply_row(r, cost_unit), axis=1)

    return out

def normalise_solar_parameters(solar_df, parameter_units=None):
    """Normalize solar parameters like kg_per_cell, area, and efficiency"""
    if not parameter_units:
        return solar_df

    out = solar_df.copy()

    for col, unit in parameter_units.items():
        if col not in out.columns:
            continue
        u = str(unit).strip().lower()

        if col == 'kg_per_cell' and u in mass_factors:
            out[col] = out[col].astype(float) * mass_factors[u]
        elif col == 'cell_active_area' and u in area_factors:
            out[col] = out[col].astype(float) * area_factors[u]
        elif col == 'efficiency':
            if u in ('%', 'percent', 'percentage'):
                out[col] = out[col].astype(float) / 100.0
            elif out[col].max() > 1.0:
                out[col] = out[col].astype(float) / 100.0

    return out

def normalised_read_production_steps(year, cost_unit=None, unit_column=None):
    """Read production steps and normalize cost data"""
    df = read_production_steps(year)
    return normalise_input_data(df, cost_column='Process Cost', unit_column=unit_column, cost_unit=cost_unit)

def normalised_build_conversion_matrix(year, parameter_units=None, data_path="data/solar_module_data.csv"):
    """Build a conversion matrix using normalized parameters if provided"""
    df = pd.read_csv(data_path)
    df_norm = normalise_solar_parameters(df, parameter_units)
    temp_path = "data/solar_module_data_normalised_temp.csv"
    df_norm.to_csv(temp_path, index=False)
    return build_conversion_matrix(year, data_path=temp_path)

