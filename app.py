import pandas as pd
from taipy.gui import Gui, notify
import os

# Inicializa variables globales
df = pd.DataFrame()  # DataFrame vacío para almacenar los datos cargados
filtered_df = pd.DataFrame()  # DataFrame para los datos filtrados
required_columns = ['Genero', 'Categoria', 'Club']  # Columnas requeridas

# Definir la estructura de la interfaz
page = """
# Dashboard Interactivo de Datos 📊

<|layout|columns=1 3 1|
<|! Load your Excel file|>
<|{file_selector}|file_selector|extensions=xlsx|on_change=load_file|>
|>

<|layout|columns=1 1 1|
<|multiselect|value={genero}|options={genero_options}|label=Selecciona Género:|>

<|multiselect|value={categoria}|options={categoria_options}|label=Selecciona Categoría:|>

<|multiselect|value={club}|options={club_options}|label=Selecciona Club:|>
|>

<|{filtered_df}|table|width=100%|height=400px|>
<|button|label=Mostrar más filas|on_action=show_all|>

<|{fig_bar}|chart|type=bar|width=100%|height=400px|>

<|{fig_pie}|chart|type=pie|width=100%|height=400px|>
"""

# Función para cargar y mostrar el archivo Excel
def load_file(state):
    global df, filtered_df
    try:
        df = pd.read_excel(state.file_selector)
        if all(column in df.columns for column in required_columns):
            state.genero_options = list(df['Genero'].unique())
            state.categoria_options = list(df['Categoria'].unique())
            state.club_options = list(df['Club'].unique())
            filter_data(state)  # Filtrar datos inicialmente
        else:
            notify(state, "error", "El archivo debe contener las columnas: Genero, Categoria, y Club.")
    except Exception as e:
        notify(state, "error", f"Error al cargar el archivo: {e}")

# Función para filtrar los datos
def filter_data(state):
    global df, filtered_df
    filtered_df = df[
        (df['Genero'].isin(state.genero)) &
        (df['Categoria'].isin(state.categoria)) &
        (df['Club'].isin(state.club))
    ]
    state.filtered_df = filtered_df.head(5)  # Mostrar las primeras 5 filas

    # Crear gráficos
    state.fig_bar = {
        "x": filtered_df['Categoria'],
        "y": filtered_df.groupby('Categoria')['Genero'].count(),
        "color": filtered_df['Genero'],
        "type": "bar",
        "title": "Distribución por Categoría y Género",
        "labels": {"x": "Categoría", "y": "Cantidad"}
    }
    state.fig_pie = {
        "labels": filtered_df['Club'],
        "values": filtered_df['Club'].value_counts(),
        "type": "pie",
        "title": "Distribución por Club"
    }

# Función para mostrar todas las filas
def show_all(state):
    state.filtered_df = filtered_df  # Mostrar todas las filas

# Configuración inicial del estado
state = {
    "file_selector": "",
    "genero": [],
    "genero_options": [],
    "categoria": [],
    "categoria_options": [],
    "club": [],
    "club_options": [],
    "filtered_df": pd.DataFrame(),
    "fig_bar": {},
    "fig_pie": {}
}

# Inicializar la aplicación Taipy con la dirección y puerto correctos
gui = Gui(page)
gui.run(state=state, host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
