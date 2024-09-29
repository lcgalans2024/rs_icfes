import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
from statistics import mode,median,mean
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objects as go
from scipy import stats

############################### Page configuration ###############################
st.set_page_config(
    page_title="Dashboard Notas Master",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

###########################################################################

@st.cache_data
def cargar_datos(file_path, nombre_hoja, numero_periodo):
    df = pd.read_excel(file_path,sheet_name=nombre_hoja)
    df = df[df.PERIODO == numero_periodo]
    return df#.copy()|

@st.cache_data
def filtrar_datos(usuario, df):
    df_filtrado = df[df['DOCUMENTO'] == str(usuario)]
    return df_filtrado.round(2)

def calcular_resultados(df):
    columnas_agrupacion = ['DOCUMENTO_DOCENTE', 'DOCENTE', 'CANVAS_COURSE_ID', 'CURSOS']
    columnas_calculo = ['DOCUMENTO_ESTUDIANTE', 'PROMEDIO_CURSO']
    resultado = df.groupby(columnas_agrupacion)[columnas_calculo].agg({
        'DOCUMENTO_ESTUDIANTE': 'count',
        'PROMEDIO_CURSO': 'mean'
    }).reset_index()

    resultado = resultado.rename(columns={'DOCUMENTO_ESTUDIANTE': 'NUMERO_RESPUESTAS', 'PROMEDIO_CURSO': 'NOTA_PROMEDIO_EST'})
    resultado['NOTA_PROMEDIO_EST'] = resultado['NOTA_PROMEDIO_EST'].round(2)

    return resultado

############################### Load Data ###############################
file_path = "Notas_Master.xlsx"

# Usar ExcelFile para obtener los nombres de las hojas
excel_file = pd.ExcelFile(file_path)

# Obtener los nombres de las hojas
sheet_names = excel_file.sheet_names

# Obtener los nombres de las hojas
periodo_number = [1,2,3]

#datos = cargar_datos(file_path, )
#
#datos["Matricula"] = datos["Matricula"].astype(str)
#datos["DOCUMENTO"] = datos["DOCUMENTO"].astype(str)
#
#for col in datos.select_dtypes(include=np.float64):
#    datos[col] = datos[col].round(2)
#datos.head()

##############################################################################

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

# Barra lateral
with st.sidebar:
    #BAENA CHALARCA JERONIMO
    st.header("DATOS DEL USUARIO")

    clave_docente = st.text_input("Documento", type='password')

    # Crear un selector en Streamlit con los nombres de las hojas
    selected_sheet = st.selectbox("Seleccione su grupo", sheet_names)

    # Crear un selector en Streamlit con los periodod
    selected_periodo = st.selectbox("Seleccione el periodo", periodo_number)

    submitted = st.button("Consultar")

    datos = cargar_datos(file_path, selected_sheet, selected_periodo)

    datos["Matricula"] = datos["Matricula"].astype(str)
    datos["DOCUMENTO"] = datos["DOCUMENTO"].astype(str)

    for col in datos.select_dtypes(include=np.float64):
        datos[col] = datos[col].round(2)

    result_df = filtrar_datos(clave_docente, datos)

    if not result_df.empty:
         with st.container(border=True):
              est_nombre = result_df['Nombre_estudiante'].iloc[0]
              st.markdown("**ESTUDIANTE:**")
              st.markdown(f"{est_nombre}")
              st.markdown(f"**GRUPO:** {selected_sheet}")

##############################################################################

# Tablero principal
st.title("TABLERO: **NOTAS MASTER**")

#st.dataframe(datos.head())

if len(clave_docente) > 0:   
    
    st.subheader("PERIODO 2")

    # Definir la columna por la que se desea agrupar
    columna_grupo = "SIMULACRO"

    df_usuario = filtrar_datos(clave_docente, datos)

    # Resetear el índice del DataFrame
    df_usuario.reset_index(drop=True, inplace=True)

    st.dataframe(df_usuario[["PROCESO","ACTIVIDAD","Calificación"]])

    # Definir los pesos para cada proceso
    pesos = {
        'HACER': 0.3,
        'SABER': 0.3,
        'AUTOEVALUACIÓN': 0.2,
        'PRUEBA_PERIODO': 0.2
    }

    # Calcular el promedio ponderado
    promedio_ponderado = 0

    for proceso, peso in pesos.items():
        promedio_ponderado += df_usuario[df_usuario['PROCESO'] == proceso]['Calificación'].mean() * peso

    est_nombre = df_usuario['Nombre_estudiante'].iloc[0]

    st.markdown(f"**Definitiva**: {round(promedio_ponderado,1)}")