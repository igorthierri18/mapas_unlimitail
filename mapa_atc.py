import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Configurar a tela de autenticação
def autenticar_usuario():
    st.title("Unlimitail - Acesso Restrito")
    codigo = st.text_input("Insira o código de acesso:", type="password")
    if st.button("Entrar"):
        if codigo == "unlimitail@2025":
            st.session_state['autenticado'] = True
            st.success("Acesso liberado! Bem-vindo.")
        else:
            st.error("Código de acesso inválido. Tente novamente.")

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    autenticar_usuario()
else:
    # Carregar os dados
    file_path_atacadao = r'C:\Users\Administrator\Documents\projetos_py\unlimitail\Lojas_CEPs_Com_Lojas_Mais_Proximas.xlsx'
    file_path_sams = r'C:\Users\Administrator\Documents\projetos_py\unlimitail\Lojas_CEPs_Com_Lojas_Mais_Proximas_Sams.xlsx'
    file_path_carrefour = r'C:\Users\Administrator\Documents\projetos_py\unlimitail\Lojas_CEPs_Com_Lojas_Mais_Proximas_Carrefour.xlsx'
    file_path_blocos = r'C:\Users\Administrator\Documents\projetos_py\unlimitail\Blocos e Trios elétricos - CEP.xlsx'

    df_atacadao = pd.read_excel(file_path_atacadao, sheet_name="Sheet1")
    df_sams = pd.read_excel(file_path_sams, sheet_name="Sheet1")
    df_carrefour = pd.read_excel(file_path_carrefour, sheet_name="Sheet1")
    df_blocos = pd.read_excel(file_path_blocos, sheet_name="Sheet1")

    # Verificar se as colunas necessárias estão presentes no DataFrame de bloquinhos
    required_columns = ['Latitude', 'Longitude', 'Nome da tela / nome do local', 'CEP']
    for col in required_columns:
        if col not in df_blocos.columns:
            st.error(f"A coluna '{col}' está ausente no arquivo de bloquinhos. Verifique o arquivo e tente novamente.")
            st.stop()

    # Remover linhas com valores NaN em Latitude ou Longitude
    df_atacadao = df_atacadao.dropna(subset=['Latitude', 'Longitude'])
    df_sams = df_sams.dropna(subset=['Latitude', 'Longitude'])
    df_carrefour = df_carrefour.dropna(subset=['Latitude', 'Longitude'])
    df_blocos = df_blocos.dropna(subset=['Latitude', 'Longitude'])

    # Inicializar o aplicativo
    st.title("Unlimitail - Mapas das lojas")

    # Criar um controle deslizante para o raio
    raio = st.slider("Selecione o raio de alcance das lojas (em metros):", 500, 5000, 2000, step=500)

    # Criar abas
    aba = st.tabs(["Atacadão", "Carrefour", "Sam's Club"])

    def adicionar_legenda():
        st.write("Legenda:")
        st.markdown(
            "- 🛒 **Lojas**: Representadas pelo ícone de carrinho de compras no mapa.\n"
            "- 🎭 **Bloquinhos e Trios Elétricos**: Representados pelo ícone de máscara no mapa.\n"
            "- 🌊 **Raio verde água**: Indica o intervalo de CEP coberto pela loja."
        )
    
    def adicionar_blocos(mapa):
        for _, row in df_blocos.iterrows():
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                icon=folium.Icon(color='blue', icon='mask', prefix='fa'),
                radius=5,
                color='#090059',
                fill=True,
                fill_color='#090059',
                fill_opacity=0.7,
                popup=f"Bloco/Triô: {row['Nome da tela / nome do local']}\nCEP: {row['CEP']}"
            ).add_to(mapa)

    with aba[0]:
        st.header("Mapa das Lojas Atacadão")
        st.write("Este mapa exibe as lojas de Atacadão e os intervalos de CEP associados como raios, no período carnavalesco.")

        if df_atacadao.empty:
            st.write("Nenhum dado válido disponível para plotar no mapa.")
        else:
            lat_center = df_atacadao['Latitude'].mean()
            lon_center = df_atacadao['Longitude'].mean()
            mapa = folium.Map(location=[lat_center, lon_center], zoom_start=12)

            for _, row in df_atacadao.iterrows():
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    icon=folium.Icon(color='red', icon='shopping-cart', prefix='fa'),
                    popup=f"Loja: {row['NomeLoja']}\nCidade: {row['Cidade']}\nCEP Loja: {row['CEP_Loja']}"
                ).add_to(mapa)

                folium.Circle(
                    location=[row['Latitude'], row['Longitude']],
                    radius=raio,
                    color='#36F5A8',
                    fill=True,
                    fill_color='#36F5A8',
                    fill_opacity=0.3
                ).add_to(mapa)

            adicionar_blocos(mapa)

            st_map = st_folium(mapa, width=700, height=500)
            adicionar_legenda()

    with aba[1]:
        st.header("Mapa das Lojas Carrefour")
        st.write("Este mapa exibe as lojas de Carrefour e os intervalos de CEP associados.")

        if df_carrefour.empty:
            st.write("Nenhum dado válido disponível para plotar no mapa.")
        else:
            lat_center = df_carrefour['Latitude'].mean()
            lon_center = df_carrefour['Longitude'].mean()
            mapa = folium.Map(location=[lat_center, lon_center], zoom_start=12)

            for _, row in df_carrefour.iterrows():
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    icon=folium.Icon(color='red', icon='shopping-cart', prefix='fa'),
                    popup=f"Loja: {row['NomeLoja']}\nCidade: {row['Cidade']}\nCEP Loja: {row['CEP_Loja']}"
                ).add_to(mapa)

                folium.Circle(
                    location=[row['Latitude'], row['Longitude']],
                    radius=raio,
                    color='#36F5A8',
                    fill=True,
                    fill_color='#36F5A8',
                    fill_opacity=0.3
                ).add_to(mapa)

            adicionar_blocos(mapa)

            st_map = st_folium(mapa, width=700, height=500)
            adicionar_legenda()

    with aba[2]:
        st.header("Mapa das Lojas Sam's Club")
        st.write("Este mapa exibe as lojas de Sam's Club e os intervalos de CEP associados.")

        if df_sams.empty:
            st.write("Nenhum dado válido disponível para plotar no mapa.")
        else:
            lat_center = df_sams['Latitude'].mean()
            lon_center = df_sams['Longitude'].mean()
            mapa = folium.Map(location=[lat_center, lon_center], zoom_start=12)

            for _, row in df_sams.iterrows():
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    icon=folium.Icon(color='red', icon='shopping-cart', prefix='fa'),
                    popup=f"Loja: {row['NomeLoja']}\nCidade: {row['Cidade']}\nCEP Loja: {row['CEP_Loja']}"
                ).add_to(mapa)

                folium.Circle(
                    location=[row['Latitude'], row['Longitude']],
                    radius=raio,
                    color='#36F5A8',
                    fill=True,
                    fill_color='#36F5A8',
                    fill_opacity=0.3
                ).add_to(mapa)

            adicionar_blocos(mapa)

            st_map = st_folium(mapa, width=700, height=500)
            adicionar_legenda()
