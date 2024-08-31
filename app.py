import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar la página de Streamlit
st.set_page_config(page_title="Dashboard de Datos", layout="wide")

# Título de la aplicación
st.title("Dashboard Interactivo de Datos 📊")

# Cargar archivo Excel
st.sidebar.header("Sube tu archivo Excel")
uploaded_file = st.sidebar.file_uploader("Elige un archivo Excel", type=["xlsx"])

# Si el usuario ha subido un archivo
if uploaded_file:
    # Leer el archivo Excel
    df = pd.read_excel(uploaded_file)

    # Mostrar solo las primeras 5 filas de los datos cargados
    st.write("### Primeras 5 Filas de los Datos Cargados:")
    st.write(df.head(5))  # Mostrar solo las primeras 5 filas

    # Verificar si las columnas necesarias existen
    required_columns = ['Genero', 'Categoria', 'Club']
    if all(column in df.columns for column in required_columns):
        
        # Filtros en la barra lateral
        st.sidebar.header("Filtros")
        genero = st.sidebar.multiselect("Selecciona Género:", options=df['Genero'].unique(), default=df['Genero'].unique())
        categoria = st.sidebar.multiselect("Selecciona Categoría:", options=df['Categoria'].unique(), default=df['Categoria'].unique())
        club = st.sidebar.multiselect("Selecciona Club:", options=df['Club'].unique(), default=df['Club'].unique())

        # Filtrar los datos basado en la selección del usuario
        filtered_df = df[
            (df['Genero'].isin(genero)) &
            (df['Categoria'].isin(categoria)) &
            (df['Club'].isin(club))
        ]

        # Mostrar solo las primeras 5 filas de los datos filtrados
        st.write("### Primeras 5 Filas de los Datos Filtrados:")
        st.write(filtered_df.head(5))

        # Mostrar más filas si el usuario lo desea
        if st.button("Mostrar más filas"):
            st.write(filtered_df)

        # Visualizaciones con Plotly
        st.write("### Visualización de Datos")

        # Ejemplo: Gráfico de barras de la cantidad por categoría
        fig = px.bar(filtered_df, x='Categoria', color='Genero', barmode='group',
                     title="Distribución por Categoría y Género",
                     labels={'Categoria': 'Categoría', 'count': 'Cantidad'})

        st.plotly_chart(fig, use_container_width=True)

        # Ejemplo: Gráfico de torta por club
        fig2 = px.pie(filtered_df, names='Club', title="Distribución por Club")
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.error("El archivo debe contener las columnas: Genero, Categoria, y Club.")

else:
    st.info("Por favor sube un archivo Excel para comenzar.")
