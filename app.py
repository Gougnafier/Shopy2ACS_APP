import streamlit as st
import pandas as pd
import unidecode
import io

st.title("Générateur de Shipments")

# Étape 1 : Téléchargement du fichier
uploaded_file = st.file_uploader("Téléchargez votre fichier orders_export.csv", type="csv")

if uploaded_file:
    st.write("Fichier chargé avec succès !")
    orders_df = pd.read_csv(uploaded_file, sep=',')

    # Étape 2 : Traitement des données
    def merge_and_sum(group):
        note = "; ".join([f"{qty} : {name}" for name, qty in zip(group['Lineitem name'], group['Lineitem quantity'])])
        total_quantity = group['Lineitem quantity'].sum()
        result = group.iloc[0].copy()
        result['Note'] = f"{group.name} | {note}"
        result['Lineitem quantity'] = total_quantity
        return result

    orders_df = orders_df.groupby('Name', group_keys=False).apply(merge_and_sum).reset_index(drop=True)

    columns_to_create = [
        'Recipient Name', 'Company Name', 'Area', 'Street', 'Number', 'Floor', 'Zip Code', 
        'Recipient Email', 'Phone', 'Mobile', 'Branch', 'Notes', 'Charge', 'Quantity', 
        'Weight', 'COD Amount', 'Payment Method', 'Ins Amount', 'Cost Center', 
        'Relevant 1', 'Relevant 2', 'Delivery Time', 'Special Services'
    ]
    shipments_df = pd.DataFrame(columns=columns_to_create)

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

    shipments_df['COD Amount'] = orders_df['Shipping Phone'].astype(float) + 1.5
    # Mettre 'COD Amount' à 0 si 'Payment Method' n'est pas "Cash on Delivery (COD)"
    shipments_df['COD Amount'] = shipments_df.apply(
        lambda row: row['COD Amount'] if row['Total'] == "Cash on Delivery (COD)" else 0,
        axis=1)
    shipments_df['COD Amount'] = shipments_df['COD Amount'].astype(str).str.replace('.', ',', regex=False)

    orders_df['Lineitem quantity'] = pd.to_numeric(orders_df['Lineitem quantity'], errors='coerce').fillna(0)
    shipments_df['Weight'] = ((orders_df['Lineitem quantity'] * 0.315) + 0.03).astype(str)
    shipments_df['Weight'] = shipments_df['Weight'].str.replace('.', ',', regex=False)
    shipments_df['Notes'] = orders_df["Note"]

    shipments_df['Recipient Name'] = shipments_df['Recipient Name'].apply(lambda x: unidecode.unidecode(x))
    shipments_df['Street'] = shipments_df['Street'].apply(lambda x: unidecode.unidecode(x))
    shipments_df['Area'] = shipments_df['Area'].apply(lambda x: unidecode.unidecode(x))
    shipments_df['Notes'] = shipments_df['Notes'].apply(lambda x: unidecode.unidecode(x))
    shipments_df['Number'] = shipments_df['Number'].apply(lambda x: unidecode.unidecode(x))

    # Étape 3 : Aperçu des données traitées
    st.write("Aperçu des données traitées :")
    st.dataframe(shipments_df)

    # Étape 4 : Télécharger le fichier CSV
    csv = shipments_df.to_csv(index=False, sep=';', encoding='utf-8')
    st.download_button("Télécharger le fichier CSV", data=csv, file_name="Created_Shipments.csv", mime="text/csv")
