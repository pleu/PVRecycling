#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

def calculate_mg_si_prices(polysilicon_price_US):
    df = pd.read_csv(polysilicon_price_US)
    
    mg_si_percentage = 0.20  # 20% of total cost
    scrap_rate = 0.20        # 20% scrap rate
    
    def calculate_price(total_cost_per_kg):
        effective_mg_si_cost = total_cost_per_kg * mg_si_percentage
        mg_si_base_price = effective_mg_si_cost * (1 - scrap_rate)
        return round (mg_si_base_price, 2)
        
    df['mg_si_price'] = df['total_cost_per_kg'].apply(calculate_price)
    
    return df


# In[ ]:




