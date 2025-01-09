import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Configuración de la página
st.set_page_config(page_title="Visualización de la Población Mundial", layout="wide")

# Generar datos simulados
def generar_datos_poblacion(n=1000):
    np.random.seed(42)
    latitudes = np.random.uniform(-90, 90, n)
    longitudes = np.random.uniform(-180, 180, n)
    sexos = np.random.choice(["Masculino", "Femenino"], n)
    edades = np.random.randint(0, 100, n)  # Edad entre 0 y 99 años
    nivel_socioeconomico = np.random.choice(["Bajo", "Medio", "Alto"], n, p=[0.5, 0.3, 0.2])
    return pd.DataFrame({
        "latitude": latitudes,
        "longitude": longitudes,
        "sexo": sexos,
        "edad": edades,
        "nivel_socioeconomico": nivel_socioeconomico
    })

# Crear datos simulados
datos = generar_datos_poblacion()

# Título de la aplicación
st.title("Visualización Interactiva de la Población Mundial")

# Controles para filtrar datos
st.sidebar.header("Controles de Filtro")
sexo_seleccionado = st.sidebar.multiselect("Sexo", ["Masculino", "Femenino"], default=["Masculino", "Femenino"])
edad_min = st.sidebar.slider("Edad mínima", 0, 100, 0)
edad_max = st.sidebar.slider("Edad máxima", 0, 100, 100)
nivel_socioeconomico_seleccionado = st.sidebar.multiselect(
    "Nivel Socioeconómico", ["Bajo", "Medio", "Alto"], default=["Bajo", "Medio", "Alto"]
)

# Filtrar datos según los controles
datos_filtrados = datos[
    (datos["sexo"].isin(sexo_seleccionado)) &
    (datos["edad"] >= edad_min) & (datos["edad"] <= edad_max) &
    (datos["nivel_socioeconomico"].isin(nivel_socioeconomico_seleccionado))
]

# Visualización con pydeck (mapa esférico)
st.subheader("Mapa Esférico de la Población Mundial")
layer = pdk.Layer(
    "ScatterplotLayer",
    datos_filtrados,
    get_position="[longitude, latitude]",
    get_fill_color=[
        "255 * (sexo == 'Femenino')",  # Rojo para Femenino
        "255 * (sexo == 'Masculino')",  # Verde para Masculino
        "100 * (nivel_socioeconomico == 'Alto')",  # Intensidad para nivel socioeconómico
    ],
    get_radius=50000,
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=0.5,
    pitch=0,
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "Sexo: {sexo}\nEdad: {edad}\nNivel: {nivel_socioeconomico}"},
    map_style="mapbox://styles/mapbox/dark-v10",
)

st.pydeck_chart(r)

# Mostrar datos en tabla
st.subheader("Datos Filtrados")
st.dataframe(datos_filtrados)
