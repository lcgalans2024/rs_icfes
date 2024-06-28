import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from statistics import mode,median,mean
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objects as go
from scipy import stats

st.set_page_config(layout = "wide")

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

###############################################################################

#Cargamos los datos
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

tab_1, tab_2, tab_3, tab_4 = st.tabs(tableros)
################################################################################

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

########################### Generar el gráfico de barra de progreso ######################

df_usuario = filtrar_datos(calve_docente, datos_simulacro_seleccionado)

# Tu puntuación
your_score_global = df_usuario['Puntaje global'].iloc[0]

# Calcular el percentil
percentile = round(stats.percentileofscore(datos_simulacro_seleccionado['Puntaje global'], your_score_global),1)

figu = create_progress_bar(percentile)

# Mostrar el gráfico en el tablero de Streamlit


# Mostrar tarjetas con las métricas
col1, col2 = st.columns(2)
with col1:
  st.metric(label="Puntaje global", value=your_score_global)
  #st.metric(label="Promedio puntaje global simulacro 2", value=promedio_general_s2)
with col2:
  st.plotly_chart(figu)
  #st.metric(label="Máximo puntaje global simulacro 1", value=maximo)
  #st.metric(label="Máximo puntaje global simulacro 2", value=maximo_s2)
#with col3:
  #st.metric(label="Mínimo puntaje global simulacro 1", value=minimo)
  #st.metric(label="Mínimo puntaje global simulacro 2", value=minimo_s2)
style_metric_cards(border_color="#3A74E7")

#########################################################################################
if submitted:
    
        result_df = filtrar_datos(calve_docente, datos)
        result_df = result_df.round(2)
        #st.table(result_df)

        # Tu puntuación
        your_score = result_df['Puntaje global'].iloc[0]

        # Calcular el percentil
        percentile = round((datos['Puntaje global'] <= your_score).sum() * 100 / len(datos),2)

        # Mostrar tarjetas con las métricas
        col1, col2, col3 = st.columns(3)
        with col1:
          st.metric(label="Promedio puntaje global simulacro 1", value=percentile)
          #st.metric(label="Promedio puntaje global simulacro 2", value=promedio_general_s2)
        with col2:
          st.metric(label="Máximo puntaje global simulacro 1", value=maximo)
          #st.metric(label="Máximo puntaje global simulacro 2", value=maximo_s2)
        with col3:
          st.metric(label="Mínimo puntaje global simulacro 1", value=minimo)
          #st.metric(label="Mínimo puntaje global simulacro 2", value=minimo_s2)
        style_metric_cards(border_color="#3A74E7")

        st.header(f'Tu puntuación de {your_score} está en el percentil {percentile}')

        # Generar el gráfico de barra de progreso
        figu = create_progress_bar(percentile)

        # Mostrar el gráfico en el tablero de Streamlit
        st.plotly_chart(figu)

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        #df = px.data.gapminder().query("continent == 'Oceania'")
        fig = px.bar(result_df, y='Nombre alumno', x='Puntaje global'
             #,hover_data=['lifeExp', 'gdpPercap']
             ,color='SIMULACRO'
             ,text_auto=True
             #,labels={'pop':'population of Canada'}, height=400
             )
        
        # Actualizar el diseño para etiquetas y título
        fig.update_layout(
            xaxis_title="Puntaje Global",
            yaxis_title="",
            title="Distribución de puntaje global",
        )

        st.plotly_chart(fig)

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        datos_agrupados_simulacro = result_df.groupby(['SIMULACRO'])[["Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]].mean().round(2).reset_index()

        # derretir datos_agrupados por columnas de areas
        datos_derretidos_simulacro = datos_agrupados_simulacro.melt(id_vars=['SIMULACRO'], var_name="Área", value_name="Promedio")

        # Seleccionamos grupo
        #datos_grupo_seleccionado = datos_derretidos[datos_derretidos.Grupo== grupo_seleccionado]

        # Crear gráfico de barras por area
        fig = px.bar(datos_derretidos_simulacro, x="Área", y="Promedio", color = 'SIMULACRO', barmode='group', text_auto=True)

        # Actualizar el diseño para etiquetas y título
        fig.update_layout(
            xaxis_title="Áreas",
            yaxis_title="Promedios",
            title="Distribución de puntajes por área",
        )

        # Mostrar el gráfico
        #fig.show()
        st.plotly_chart(fig)