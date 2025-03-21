import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
@st.cache_data
# Create a horizontal bar plot representing score
def barra_progreso(M,nota,meta):
    fig, ax = plt.subplots(figsize=(8, 2))
    # Create the bar
    ax.broken_barh([(0, M)], (0.5, 1), facecolors='lightgray')
    ax.broken_barh([(0, nota)], (0.5, 1), facecolors='lightgreen')

    # Add a vertical line for the score
    ax.vlines(meta, 0.5, 1.5, colors='black')

    # Colocar el valor de la nota dentro de la barra verde
    ax.text(nota, 0.95, f'{nota}', ha='right', va='center', fontsize=12, color='black', fontweight='bold')

    # Personalizar el gráfico
    ax.set_yticks([])
    ax.set_xticks(range(0, M + 1))
    ax.set_xlim(0, M)
    ax.set_ylim(0, 2)
    ax.set_title('Nota Acumulada')

    # Mostrar los bordes del gráfico
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(True)

    return fig

############################### Load Data ###############################
file_path = "Notas_Master.xlsx"

# Usar ExcelFile para obtener los nombres de las hojas
excel_file = pd.ExcelFile(file_path)

# Obtener los nombres de las hojas
sheet_names = excel_file.sheet_names

# Obtener los nombres de las hojas
periodo_number = ["",1,2,3]

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

    documento_estudiante = st.text_input("Documento", type='password')

    # Crear un selector en Streamlit con los nombres de las hojas
    selected_sheet_grupo = st.selectbox("Seleccione su grupo", [""] + sheet_names, index= 0)

    # Crear un selector en Streamlit con los periodod
    selected_periodo = st.selectbox("Seleccione el periodo académico", periodo_number, index= 0)

    submitted = st.button("Consultar")

    if selected_sheet_grupo != "":
        datos = cargar_datos(file_path, selected_sheet_grupo, selected_periodo)

        datos["Matricula"] = datos["Matricula"].astype(str)
        datos["DOCUMENTO"] = datos["DOCUMENTO"].astype(str)

        for col in datos.select_dtypes(include=np.float64):
            datos[col] = datos[col].round(2)

        result_df = filtrar_datos(documento_estudiante, datos)

        if not result_df.empty:
            with st.container(border=True):
                est_nombre = result_df['Nombre_estudiante'].iloc[0]
                st.markdown("**ESTUDIANTE:**")
                st.markdown(f"{est_nombre}")
                st.markdown(f"**GRUPO:** {selected_sheet_grupo}")
    else:
        st.warning("Ingresar datos del estudiante")

##############################################################################

# Tablero principal
st.title("TABLERO: **NOTAS MASTER**")

#st.dataframe(datos.head())

if len(documento_estudiante) > 0:   
    if documento_estudiante and selected_sheet_grupo and selected_periodo:

        if not result_df.empty:

            st.subheader(f"PERIODO {selected_periodo}")

            # Definir la columna por la que se desea agrupar
            columna_grupo = "SIMULACRO"

            df_usuario = filtrar_datos(documento_estudiante, datos)

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

            nota_acumulada = round(promedio_ponderado,1)

            #st.markdown(f"**Definitiva**: {nota_acumulada}")

            # Generar y mostrar la gráfica
            fig = barra_progreso(5, nota_acumulada, 3)
            st.pyplot(fig)
        else:
            st.warning("Usuario no registrado, revise los datos seleccionados")
    else:
        st.warning("Por favor, ingrese todos los datos.")