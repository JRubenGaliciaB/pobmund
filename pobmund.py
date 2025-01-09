import pandas as pd

# Ejemplo de cómo cargar datos desde un archivo CSV descargado
df_poblacion = pd.read_csv('poblacion_por_pais_sexo.csv')
df_edad = pd.read_csv('distribucion_edad.csv')
df_socioeconomico = pd.read_csv('indicadores_socioeconomicos.csv')

# Unir los dataframes según el país
df = pd.merge(df_poblacion, df_edad, on='country_code')
df = pd.merge(df, df_socioeconomico, on='country_code')

import streamlit as st
import pydeck as pdk

# Configuración de la página
st.set_page_config(page_title="Visualización de la Población Mundial", layout="wide")

# Título de la aplicación
st.title("Visualización Interactiva de la Población Mundial")

# Controles de filtro en la barra lateral
st.sidebar.header("Filtros")
sexo = st.sidebar.selectbox("Sexo", ["Ambos", "Masculino", "Femenino"])
edad_min = st.sidebar.slider("Edad mínima", 0, 100, 0)
edad_max = st.sidebar.slider("Edad máxima", 0, 100, 100)
nivel_socioeconomico = st.sidebar.multiselect("Nivel Socioeconómico", ["Bajo", "Medio", "Alto"], default=["Bajo", "Medio", "Alto"])

# Filtrar datos según los controles
df_filtrado = df[
    (df['edad'] >= edad_min) &
    (df['edad'] <= edad_max) &
    (df['nivel_socioeconomico'].isin(nivel_socioeconomico))
]
if sexo != "Ambos":
    df_filtrado = df_filtrado[df_filtrado['sexo'] == sexo]

# Mapa interactivo con pydeck
st.subheader("Mapa de la Población Mundial")
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_filtrado,
    get_position=["longitude", "latitude"],
    get_fill_color=[255, 0, 0] if sexo == "Femenino" else [0, 0, 255],
    get_radius=100000,
    pickable=True,
)
view_state = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=1,
    pitch=0,
)
r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{country_name}\nPoblación: {population}"})
st.pydeck_chart(r)

# Mostrar datos en tabla
st.subheader("Datos Filtrados")
st.dataframe(df_filtrado)
