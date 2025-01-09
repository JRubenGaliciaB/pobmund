import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Población Mundial", layout="wide")

# Generar datos simulados
@st.cache
def cargar_datos():
    np.random.seed(42)
    num_registros = 5000  # Aumentar el número de registros para mayor cobertura

    data = {
        "latitude": np.random.uniform(-90, 90, num_registros),  # Distribución global
        "longitude": np.random.uniform(-180, 180, num_registros),
        "sexo": np.random.choice(["Masculino", "Femenino"], num_registros),
        "edad": np.random.randint(0, 100, num_registros),
        "nivel_socioeconomico": np.random.choice(["Bajo", "Medio", "Alto"], num_registros, p=[0.5, 0.3, 0.2]),
        "poblacion": np.random.randint(1000, 10000, num_registros),
        "country": np.random.choice(
            ["México", "Estados Unidos", "China", "India", "Brasil", "Nigeria", "Rusia", "Japón", "Alemania", "Sudáfrica"],
            num_registros
        )
    }

    return pd.DataFrame(data)

# Cargar los datos simulados
datos = cargar_datos()

# Título de la aplicación
st.title("Visualización Interactiva de la Población Mundial")

# Controles en la barra lateral
st.sidebar.header("Filtros")
sexo_filtro = st.sidebar.multiselect("Sexo", ["Masculino", "Femenino"], default=["Masculino", "Femenino"])
edad_min = st.sidebar.slider("Edad mínima", 0, 100, 0)
edad_max = st.sidebar.slider("Edad máxima", 0, 100, 100)
nivel_socioeconomico_filtro = st.sidebar.multiselect(
    "Nivel Socioeconómico", ["Bajo", "Medio", "Alto"], default=["Bajo", "Medio", "Alto"]
)

# Filtrar datos según los controles
datos_filtrados = datos[
    (datos["sexo"].isin(sexo_filtro)) &
    (datos["edad"] >= edad_min) & (datos["edad"] <= edad_max) &
    (datos["nivel_socioeconomico"].isin(nivel_socioeconomico_filtro))
]

# Configurar colores como un gradiente basado en la población
max_poblacion = datos["poblacion"].max()
min_poblacion = datos["poblacion"].min()

# Normalizar población a un rango de 0-255 para el gradiente
datos_filtrados["color"] = datos_filtrados["poblacion"].apply(
    lambda x: int((x - min_poblacion) / (max_poblacion - min_poblacion) * 255)
)

# Mapa interactivo con gradiente
st.subheader("Mapa Interactivo de la Población Mundial (Gradiente por Densidad de Población)")
layer = pdk.Layer(
    "ScatterplotLayer",
    datos_filtrados,
    get_position=["longitude", "latitude"],
    get_fill_color=["color", "0", "255 - color", "200"],  # Gradiente RGB (rojo -> azul)
    get_radius=200000,  # Aumentar el radio para mejorar la visibilidad
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=20,
    longitude=0,
    zoom=1,
    pitch=0,
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "html": "<b>País:</b> {country}<br><b>Sexo:</b> {sexo}<br><b>Edad:</b> {edad}<br><b>Nivel:</b> {nivel_socioeconomico}<br><b>Población:</b> {poblacion}",
        "style": {"color": "white"}
    },
    map_style="mapbox://styles/mapbox/light-v10",
)

st.pydeck_chart(r)

# Mostrar datos en tabla
st.subheader("Datos Filtrados")
st.dataframe(datos_filtrados)

# Mostrar estadísticas resumidas
st.subheader("Estadísticas Resumidas")
st.write(datos_filtrados.describe())

