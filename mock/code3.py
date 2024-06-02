import pandas as pd

# import semi_production_and_use.xlsx sheet
semi_production_and_use = pd.read_excel('semi_production_and_use.xlsx', sheet_name='production', header=3)
#drop the first 9 rows
semi_production_and_use = semi_production_and_use.drop(semi_production_and_use.index[0:9])
#drop the last 4 rows
semi_production_and_use = semi_production_and_use.drop(semi_production_and_use.index[-4:])
# rename Class 8 Tractor Regional Haul to regional
semi_production_and_use = semi_production_and_use.rename(columns={'Class 8 Tractor Regional Haul': 'regional'})
# rename Class 8 Tractor Long Haul to long
semi_production_and_use = semi_production_and_use.rename(columns={'Class 8 Tractor Long Haul': 'long'})
# select year, regional, and long columns
semi_production_and_use = semi_production_and_use[['regional', 'long']]
# create short column as 0.1 * regional
semi_production_and_use['short'] = 0.1 * semi_production_and_use['regional']
semi_production_and_use

# convert df to dict
semi_production_and_use_dict = semi_production_and_use.to_dict('records')
semi_production_and_use_dict

data = [{'diesel': x, 'electric': {'short': 0, 'regional': 0, 'long': 0}} for x in semi_production_and_use_dict]
data

import pandas as pd

hauls = ['short', 'regional', 'long']

diesel_price_ratios = {
    'short': 0.55,
    'regional': 0.65,
    'long': 0.75
}

truck_counts = data.copy()

stay = 0.91

on_the_fence = 0.08
revert = 0.01

for i in range(20):
    count_next = {'electric': {}, 'diesel': {}}
    for haul in hauls:
        decommissioned_diesel = truck_counts[-12]['diesel'][haul]
        decommissioned_electric = truck_counts[-12]['electric'][haul]

        switch_to_electric = decommissioned_diesel * diesel_price_ratios[haul]
        revert_to_diesel = decommissioned_electric * revert + (1 - diesel_price_ratios[haul])*decommissioned_electric*on_the_fence

        print(switch_to_electric)
        print(revert_to_diesel)

        new_electric = truck_counts[-1]['electric'][haul] + switch_to_electric - revert_to_diesel
        new_diesel = truck_counts[-1]['diesel'][haul] - switch_to_electric + revert_to_diesel

        count_next['electric'][haul] = new_electric
        count_next['diesel'][haul] = new_diesel

    truck_counts.append(count_next)

output = [x['electric'] for x in truck_counts]

#convert output to df
output_df = pd.DataFrame(output)
output_df