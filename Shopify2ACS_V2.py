import pandas as pd
from tretement import dfShipment

# Charger le fichier orders_export.csv avec le bon séparateur
orders_file = 'orders_export_1 (4).csv'
orders_df = pd.read_csv(orders_file, sep=',')

# Group data by "Name" and summarize information into a new column "Note"
def merge_and_sum(group):
    note = "; ".join([f"{qty} : {name}" for name, qty in zip(group['Lineitem name'], group['Lineitem quantity'])])
    total_quantity = group['Lineitem quantity'].sum()
    result = group.iloc[0].copy()
    result['Note'] = f"{group.name} | {note}"
    result['Lineitem quantity'] = total_quantity
    return result

# Grouping by "Name" and merging notes
orders_df = orders_df.groupby('Name').apply(merge_and_sum).reset_index(drop=True)

# Séparer les données par 'Shipping Country'
grouped_data = {country: df for country, df in orders_df.groupby('Shipping Country')}

for country, df in grouped_data.items():
    
    shipments_df = dfShipment(df)
    
    shipments_df.to_csv(f'Created_Shipments_{country}.csv', sep=';', index=False, encoding='utf-8')

    # Vérifier les premières lignes du DataFrame
    print(shipments_df.head())
