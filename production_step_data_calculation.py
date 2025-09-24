#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd

def calculate_production_step_data(input_file='manufacturing_values.csv', 
                                 output_file='production_step_data.csv',
                                 years=range(2020, 2026)):
    input_df = pd.read_csv('manufacturing_values.csv')
    years = range(2020, 2026)
    output_columns = ['Year', 'Production Step', 'Unit', 'Distribution', 'Process Cost', 'Process Cost Min', 'Process Cost Max']
    
    all_years_data = []
    
    for year in years:
    # Create output structure for current year 
        data = {
            'Production Step': [
            'Purchase mg-Si',
            'SoG Poly-Si (exclude mg-Si cost)',
            'Mono Wafer (exclude poly-Si cost)',
            'Mono PERC cell (exclude wafer cost)',
            'Mono PERC module (exclude cell cost)',
            'Recycled mg-Si',
            'Recycled SOG poly-Si',
            'Recycled Mono wafer'
            ],
            
            'Unit': ['kg', 'kg', 'wafer', 'cell', 'module', 'kg', 'kg', 'wafer'],
            'Distribution': ['Log-normal'] * 5 + ['Uniform'] * 3,
            'Year': [year] * 8
        }
        
    # Create dataframe for current year
    year_df = pd.DataFrame(data)
    
    # Get manufacturing values for this year
    year_values = input_df.set_index('variable')[str(year)].astype(float)
    
    # Set process costs
    year_df.loc[0, 'Process Cost'] = year_values['mg-Si ($/kg)']
    year_df.loc[1, 'Process Cost'] = year_values['poly-Si ($/kg)']
    year_df.loc[2, 'Process Cost'] = year_values['mono-wafer ($/wafer)']
    year_df.loc[3, 'Process Cost'] = year_values['mono-cell ($/cell)']
    year_df.loc[4, 'Process Cost'] = year_values['mono-module ($/module)']
    
    # Set recycled material costs (50% of virgin materials)
    year_df.loc[5, 'Process Cost'] = 0.5 * year_values['mg-Si ($/kg)']
    year_df.loc[6, 'Process Cost'] = 0.5 * year_values['poly-Si ($/kg)']
    year_df.loc[7, 'Process Cost'] = 0.5 * year_values['mono-wafer ($/wafer)']
    
    # Calculate min/max values
    for i in range(5):  # First 5 are Log-normal
        cost = year_df.loc[i, 'Process Cost']
        year_df.loc[i, 'Process Cost Min'] = 0.8 * cost
        year_df.loc[i, 'Process Cost Max'] = 1.2 * cost
        
        
    for i in range(5, 8):  # Last 3 are Uniform
        cost = year_df.loc[i, 'Process Cost']
        year_df.loc[i, 'Process Cost Min'] = 0
        year_df.loc[i, 'Process Cost Max'] = 2 * cost
    
    
    all_years_data.append(year_df)
    
    combined_df = pd.concat(all_years_data, ignore_index=True)

# Save the result
combined_df = combined_df[output_columns]
combined_df.to_csv('production_step_data.csv', index=False)


# In[ ]:





# In[ ]:




