import streamlit as st
import pandas as pd
import unidecode
import io
from tretement import dfShipment

st.title("Générateur de Shipments")

# Étape 1 : Téléchargement du fichier
uploaded_file = st.file_uploader("Téléchargez votre fichier orders_export.csv", type="csv")

if uploaded_file:
    st.write("Fichier chargé avec succès !")
    orders_df = pd.read_csv(uploaded_file, sep=',')

    # Étape 1.1 : Aperçu du fichier chargé 
    st.write("Aperçu du fichier chargé :")
    st.dataframe(orders_df)

    # Étape 2 : Traitement des données
    def merge_and_sum(group):
        note = "; ".join([f"{qty} : {name}" for name, qty in zip(group['Lineitem name'], group['Lineitem quantity'])])
        total_quantity = group['Lineitem quantity'].sum()
        result = group.iloc[0].copy()
        result['Note'] = f"{group.name} | {note}"
        result['Lineitem quantity'] = total_quantity
        return result

    orders_df = orders_df.groupby('Name', group_keys=False).apply(merge_and_sum).reset_index(drop=True)
    
    # Séparer les données par 'Shipping Country'
    grouped_data = {country: df for country, df in orders_df.groupby('Shipping Country')}

    # Créer et permettre le téléchargement de fichiers pour chaque pays
    st.divider()
    st.write("Téléchargez un fichier pour chaque 'Shipping Country' :")

    for country, df in grouped_data.items():
        st.divider()

        shipments_df = dfShipment(df)

        # Générer le CSV pour le pays
        csv_data = shipments_df.to_csv(index=False, sep=';', encoding='utf-8')

        st.write(f"Aperçu des données traitées pour {country} :")
        st.dataframe(shipments_df)

        # Bouton de téléchargement pour ce pays
        st.download_button(
            label=f"Télécharger les commandes pour {country}",
            data=csv_data,
            file_name=f"Orders_{country}.csv",
            mime="text/csv"
        )
