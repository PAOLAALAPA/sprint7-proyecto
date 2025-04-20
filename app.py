import streamlit as st
import pandas as pd

# Título principal
st.title("🚗 Análisis de vehículos en EE.UU.")

# Cargar datos con manejo de errores
@st.cache_data
def load_data():
    try:
        return pd.read_csv("vehicles_us.csv", on_bad_lines='skip')
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return pd.DataFrame()

df = load_data()

# Si no se cargó bien el archivo, no continúes
if df.empty:
    st.warning("El archivo no se pudo cargar correctamente o está vacío.")
else:
    # Mostrar una parte del DataFrame
    st.subheader("Vista previa de los datos")
    st.dataframe(df.head())

    # Mostrar estadísticas
    st.subheader("📊 Estadísticas generales")
    st.write(df.describe())

    # Filtro interactivo
    if 'transmission' in df.columns:
        st.subheader("🔍 Filtrar por tipo de transmisión")
        transmission = st.selectbox("Selecciona el tipo de transmisión", df['transmission'].dropna().unique())
        filtered_data = df[df['transmission'] == transmission]
        st.write(filtered_data.head())
    else:
        st.warning("La columna 'transmission' no existe en los datos.")
import plotly.express as px

# Mostrar gráfico de dispersión si el usuario lo desea
if st.checkbox("Mostrar gráfico de dispersión: precio vs. kilometraje"):
    fig = px.scatter(
        df,
        x='odometer',
        y='price',
        title='Relación entre kilometraje (odometer) y precio (price)',
        labels={'odometer': 'Kilometraje', 'price': 'Precio (USD)'},
        opacity=0.5
    )
    st.plotly_chart(fig)
