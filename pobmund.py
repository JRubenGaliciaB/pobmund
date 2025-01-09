import streamlit as st
import numpy as np
from streamlit_globe import streamlit_globe

# Configuración de la página
st.set_page_config(page_title="Globo Poblacional", layout="wide")

# Generar datos simulados
@st.cache
def generar_datos():
    np.random.seed(42)
    num_puntos = 1000

    datos = {
        "lat": np.random.uniform(-90, 90, num_puntos),
        "lng": np.random.uniform(-180, 180, num_puntos),
        "size": np.random.uniform(0.1, 0.5, num_puntos),
        "color": np.random.choice(["red", "blue", "green"], num_puntos),
        "text": [f"Población: {np.random.randint(1000, 1000000)}" for _ in range(num_puntos)],
    }

    return datos

# Cargar datos simulados
datos = generar_datos()

# Convertir datos a formato compatible con streamlit_globe
pointsData = [{"lat": lat, "lng": lng, "size": size, "color": color}
              for lat, lng, size, color in zip(datos["lat"], datos["lng"], datos["size"], datos["color"])]
labelsData = [{"lat": lat, "lng": lng, "size": size, "color": color, "text": text}
              for lat, lng, size, color, text in zip(datos["lat"], datos["lng"], datos["size"], datos["color"], datos["text"])]

# Visualización del globo
st.subheader("Globo Poblacional Interactivo")
streamlit_globe(
    pointsData=pointsData,
    labelsData=labelsData,
    daytime="day",
    width=800,
    height=600
)

# Información adicional
st.sidebar.header("Información sobre los datos")
st.sidebar.write("Los puntos representan ubicaciones con población simulada. El tamaño y el color varían según los datos.")
