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
    page_title="Dashboard Resultados Simulacros ICFES",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

###########################################################################

@st.cache_data
def cargar_datos():
    df = pd.read_excel("Resultados_Simulacro_ICFES.xlsx")
    return df#.copy()

@st.cache_data
def filtrar_datos(usuario, df):
    df_filtrado = df[df['Nombre alumno'] == str(usuario)]
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

#@st.cache_data
def create_progress_bar(percentage):
    fig = go.Figure()

    # Agregar la barra de progreso
    fig.add_trace(go.Bar(
        x=[percentage],
        y=[''],
        orientation='h',
        marker=dict(color='Blue', line=dict(color='Black', width=3)),
        width=0.4,
        hoverinfo='none'
    ))

    # Configuración de diseño
    fig.update_layout(
        xaxis=dict(
            range=[0, 100],
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=True,
            zeroline=True
        ),
        shapes=[
            dict(
                type='rect', #['circle', 'rect', 'path', 'line'],
                x0=0, y0=-0.2, x1=100, y1=0.2,
                line=dict(color='Black', width=3)
            )
        ],
        annotations=[
            dict(
                x=percentage, y=0,
                text=f'{percentage}%',
                showarrow=False,
                font=dict(size=25, color='white'),
                xanchor='right', yanchor='middle'
            )
        ],
        height=150,
        width=600,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        title=dict(
          text="Percentil asociado al puntaje",
          font=dict(size=24, color='navy'),
          xref='paper',
          x=0.5,
          yref='paper',
          #y=1.2,
          xanchor='center',
          yanchor='top'
        )
    )

    return fig

#Donut chart

def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "value": [500-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "value": [500, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=100, cornerRadius=40).encode(
      theta="value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=330, height=330)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=65, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response}'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=100, cornerRadius=40).encode(
      theta="value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=330, height=330)
  return plot_bg + plot + text

############################### Load Data ###############################
datos = cargar_datos()

datos_s1 = datos[datos["SIMULACRO"] == "S1"]
datos_s2 = datos[datos["SIMULACRO"] == "S2"]

for col in datos.select_dtypes(include=np.float64):
    datos[col] = datos[col].round(2)
datos.head()

datos["Grupo"] = datos["Grupo"].astype(str)
datos["Matemáticas"] = datos["Matemáticas"].astype(int)

##############################################################################

# Barra lateral
with st.sidebar:
    #BAENA CHALARCA JERONIMO
    st.header("DATOS DEL USUARIO")

    calve_docente = st.text_input("Contraseña", '', type='password')
    submitted = st.button("Consultar")

    result_df = filtrar_datos(calve_docente, datos)

    if not result_df.empty:
         with st.container(border=True):
              est_nombre = result_df['Nombre alumno'].iloc[0]
              grupo = result_df['Grupo'].iloc[0]
              st.markdown(f"**ESTUDIANTE:** {est_nombre}")
              st.markdown(f"**GRUPO:** {grupo}")

    
# Tablero principal
st.title("TABLERO RESULTADOS SIMULACROS ICFES")
st.subheader("Resultados")

################################################################################
tableros = ["Puntaje Global", "Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]

tab_1, tab_2, tab_3, tab_4, tab_5, tab_6 = st.tabs(tableros)

##############################################################################################################
########################################## ANÁLISIS PUNTAJE GLOBAL ###########################################
##############################################################################################################

with tab_1:
    # Definir la columna por la que se desea agrupar
    columna_grupo = "SIMULACRO"  

    # Obtener grupos únicos de la columna elegida
    grupos_unicos = result_df[columna_grupo].unique()

    # Crear un selector de grupo con st.selectbox
    grupo_seleccionado = st.selectbox("Seleccione un grupo:", grupos_unicos)

    # Seleccionamos grupo
    datos_simulacro_seleccionado = datos[datos.SIMULACRO== grupo_seleccionado]

    promedio = round(datos_simulacro_seleccionado['Puntaje global'].mean(),2)
    maximo = max(datos_simulacro_seleccionado['Puntaje global'])
    minimo = min(datos_simulacro_seleccionado['Puntaje global'])

    df_usuario = filtrar_datos(calve_docente, datos_simulacro_seleccionado)

    # Tu puntuación
    your_score_global = df_usuario['Puntaje global'].iloc[0]

    # Calcular el percentil
    percentile = round(stats.percentileofscore(datos_simulacro_seleccionado['Puntaje global'], your_score_global),1)

    figu = create_progress_bar(percentile)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('Puntaje Global')
        st.altair_chart(make_donut(your_score_global, "Puntaje global", "green"))
    with col2:
        st.write('Puntaje Global')
        st.altair_chart(make_donut(promedio, "Puntaje global promedio", "green"))
    with col3:
        st.plotly_chart(figu)

    #st.metric(label="Puntaje global", value=your_score_global)

    style_metric_cards(border_color="#3A74E7")