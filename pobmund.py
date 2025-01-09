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
    paises = [
        "México", "Estados Unidos", "China", "India", "Brasil", "Nigeria", 
        "Rusia", "Japón", "Alemania", "Sudáfrica"
    ]
    latitudes = [23.6345, 37.0902, 35.8617, 20.5937, -14.2350, 9.0820, 61.5240, 36.2048, 51.1657, -30.5595]
    longitudes = [-102.5528, -95.7129, 104.1954, 78.9629, -51.9253, 8.6753, 105.3188, 138.2529, 10.4515, 22.9375]

    data = []
    for i, pais in enumerate(paises):
        for _ in range(100):  # 100 personas por país
            data.append({
                "country": pais,
                "latitude": latitudes[i] + np.random.uniform(-0.5, 0.5),
                "longitude": longitudes[i] + np.random.uniform(-0.5, 0.5),
                "sexo": np.random.choice(["Masculino", "Femenino"]),
                "edad": np.random.randint(0, 100),
                "nivel_socioeconomico": np.random.choice(["Bajo", "Medio", "Alto"], p=[0.5, 0.3, 0.2]),
                "poblacion": np.random.randint(1000, 10000),
            })
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

# Configurar colores como un gradiente basado en la edad
max_edad = datos["edad"].max()
min_edad = datos["edad"].min()

# Normalizar edades a un rango de 0-255 para el gradiente
datos_filtrados["color"] = datos_filtrados["edad"].apply(
    lambda x: int((x - min_edad) / (max_edad - min_edad) * 255)
)

# Mapa interactivo con gradiente
st.subheader("Mapa Interactivo de la Población Mundial (Gradiente por Edad)")
layer = pdk.Layer(
    "ScatterplotLayer",
    datos_filtrados,
    get_position=["longitude", "latitude"],
    get_fill_color=["color", "255 - color", "128"],  # Gradiente RGB
    get_radius=50000,
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=20,
    longitude=0,
    zoom=1.5,
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
