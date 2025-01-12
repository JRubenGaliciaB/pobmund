import streamlit as st
from streamlit_globe import streamlit_globe

# Configuración de la página
st.set_page_config(page_title="Mapa de Población Mundial", layout="wide")

# Datos simulados: Población por país
# Para un uso real, reemplaza esto con datos oficiales
poblacion_paises = {
    "México": {"lat": 23.6345, "lng": -102.5528, "poblacion": 126014024},
    "Estados Unidos": {"lat": 37.0902, "lng": -95.7129, "poblacion": 331893745},
    "China": {"lat": 35.8617, "lng": 104.1954, "poblacion": 1411778724},
    "India": {"lat": 20.5937, "lng": 78.9629, "poblacion": 1407563842},
    "Brasil": {"lat": -14.235, "lng": -51.9253, "poblacion": 214326223},
    "Nigeria": {"lat": 9.082, "lng": 8.6753, "poblacion": 223804632},
    "Rusia": {"lat": 61.524, "lng": 105.3188, "poblacion": 144444359},
    "Japón": {"lat": 36.2048, "lng": 138.2529, "poblacion": 123457506},
    "Alemania": {"lat": 51.1657, "lng": 10.4515, "poblacion": 83889762},
    "Sudáfrica": {"lat": -30.5595, "lng": 22.9375, "poblacion": 60142978},
}

# Definir colores basados en la población
def calcular_color(poblacion):
    """
    Asigna un color basado en la población. 
    Poblaciones más altas se representan con colores más cálidos.
    """
    if poblacion > 1_000_000_000:
        return "red"
    elif poblacion > 500_000_000:
        return "orange"
    elif poblacion > 100_000_000:
        return "yellow"
    elif poblacion > 50_000_000:
        return "green"
    else:
        return "blue"

# Preparar los datos para el globo
points_data = [
    {
        "lat": datos["lat"],
        "lng": datos["lng"],
        "size": 0.5,  # Tamaño constante para todos los puntos
        "color": calcular_color(datos["poblacion"]),
    }
    for datos in poblacion_paises.values()
]

labels_data = [
    {
        "lat": datos["lat"],
        "lng": datos["lng"],
        "text": f"{pais}: {datos['poblacion']:,}",
        "color": calcular_color(datos["poblacion"]),
        "size": 0.5,
    }
    for pais, datos in poblacion_paises.items()
]

# Mostrar el globo interactivo
st.subheader("Globo Interactivo de Población Mundial")
streamlit_globe(
    pointsData=points_data, labelsData=labels_data, daytime="day", width=800, height=600
)

# Mostrar una tabla con los datos
st.subheader("Datos de Población")
st.table(
    pd.DataFrame(
        [
            {"País": pais, "Latitud": datos["lat"], "Longitud": datos["lng"], "Población": datos["poblacion"]}
            for pais, datos in poblacion_paises.items()
        ]
    )
)
