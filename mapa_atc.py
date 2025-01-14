import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Carregar os dados
file_path = r'C:\Users\Administrator\Documents\projetos_py\unlimitail\Lojas_CEPs_Com_Lojas_Mais_Proximas.xlsx'
df = pd.read_excel(file_path, sheet_name="Sheet1")

# Remover linhas com valores NaN em Latitude ou Longitude
df = df.dropna(subset=['Latitude', 'Longitude'])

# Inicializar o aplicativo
st.title("Unlimitail - Mapas das lojas")

# Criar abas
aba = st.tabs(["Atacadão", "Carrefour", "Sam's Club"])

with aba[0]:
    st.header("Mapa das Lojas Atacadão")
    st.write("Este mapa exibe as lojas de Atacadão e os intervalos de CEP associados como raios, no período carnavalesco.")

    # Verificar se há dados válidos após a filtragem
    if df.empty:
        st.write("Nenhum dado válido disponível para plotar no mapa.")
    else:
        # Criar o mapa centralizado na média das coordenadas
        lat_center = df['Latitude'].mean()
        lon_center = df['Longitude'].mean()
        mapa = folium.Map(location=[lat_center, lon_center], zoom_start=12)

        # Adicionar os CEPs das lojas como bolinhas azuis
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=5,
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.7,
                popup=f"Loja: {row['NomeLoja']}\nCEP Loja: {row['CEP_Loja']}\nCidade: {row['Cidade']}"
            ).add_to(mapa)

        # Adicionar os intervalos de CEP como raios
        for _, row in df.iterrows():
            folium.Circle(
                location=[row['Latitude'], row['Longitude']],
                radius=500,  # Exemplo: ajustar o raio conforme necessário
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.3,
                popup=f"Intervalo CEP: {row['CEP_Inicio']} - {row['CEP_Fim']}"
            ).add_to(mapa)

        # Renderizar o mapa no Streamlit
        st_map = st_folium(mapa, width=700, height=500)

with aba[1]:
    st.header("Mapa das Lojas Carrefour")
    st.write("Mapa das lojas Carrefour será implementado em breve.")

with aba[2]:
    st.header("Mapa das Lojas Sam's Club")
    st.write("Mapa das lojas Sam's Club será implementado em breve.")
