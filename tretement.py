import pandas as pd

def dfShipment(orders_df):
    # Créer un nouveau DataFrame avec les colonnes spécifiques de Shipments
    columns_to_create = [
        'Recipient Name', 'Company Name', 'Area', 'Street', 'Number', 'Floor', 'Zip Code', 
        'Recipient Email', 'Phone', 'Mobile', 'Branch', 'Notes', 'Charge', 'Quantity', 
        'Weight', 'COD Amount', 'Payment Method', 'Ins Amount', 'Cost Center', 
        'Relevant 1', 'Relevant 2', 'Delivery Time', 'Special Services'
    ]

    # Créer un DataFrame vide avec ces colonnes
    shipments_df = pd.DataFrame(columns=columns_to_create)

    # Remplir les colonnes avec les correspondances trouvées dans orders_export.csv
    shipments_df['Recipient Name'] = orders_df['Shipping Name']
    shipments_df['Company Name'] = orders_df['Shipping Company']
    shipments_df['Street'] = orders_df['Shipping Street']

    shipments_df['Zip Code'] = orders_df['Shipping Zip']
    shipments_df['Zip Code'] = shipments_df['Zip Code'].astype(str).str.replace(' ', '')
    shipments_df['Zip Code'] = shipments_df['Zip Code'].astype(str).str.replace("'", "")

    shipments_df['Recipient Email'] = orders_df['Email']
    shipments_df['Phone'] = orders_df['Shipping Phone']
    shipments_df['Payment Method'] = orders_df['Payment Method']
    shipments_df['Notes'] = orders_df['Notes']
    shipments_df['Area'] = orders_df["Shipping City"]
    shipments_df['Number'] = orders_df["Shipping Address1"]


    shipments_df['COD Amount'] = orders_df['Total'].astype(float) + 1.5
    # Mettre 'COD Amount' à 0 si 'Payment Method' n'est pas "Cash on Delivery (COD)"
    shipments_df['COD Amount'] = shipments_df.apply(
        lambda row: row['COD Amount'] if row['Payment Method'] == "Cash on Delivery (COD)" else 0,
        axis=1)
    shipments_df['COD Amount'] = shipments_df['COD Amount'].astype(str).str.replace('.', ',', regex=False)

    shipments_df['Payment Method'] = shipments_df['Payment Method'].apply(
        lambda x: "M" if x == "Cash on Delivery (COD)" else None)

    # Assurez-vous que 'Lineitem quantity' ne contient pas de valeurs nulles ou non numériques
    orders_df['Lineitem quantity'] = pd.to_numeric(orders_df['Lineitem quantity'], errors='coerce').fillna(0)

    # Calculez le poids et remplissez la colonne 'Weight'
    shipments_df['Weight'] = ((orders_df['Lineitem quantity'] * 0.315) + 0.03).astype(str)
    shipments_df['Weight'] = shipments_df['Weight'].str.replace('.', ',', regex=False)
    shipments_df['Notes'] = orders_df["Note"]

    import unidecode

    # Appliquer la translittération sur les colonnes pertinentes (par exemple, 'Recipient Name', 'Street', 'Area', etc.)
    shipments_df['Recipient Name'] = shipments_df['Recipient Name'].apply(lambda x: unidecode.unidecode(x))
    shipments_df['Street'] = shipments_df['Street'].apply(lambda x: unidecode.unidecode(x))
    shipments_df['Area'] = shipments_df['Area'].apply(lambda x: unidecode.unidecode(x))
    shipments_df['Notes'] = shipments_df['Notes'].apply(lambda x: unidecode.unidecode(x))
    shipments_df['Number'] = shipments_df['Number'].apply(lambda x: unidecode.unidecode(x))

    return shipments_df