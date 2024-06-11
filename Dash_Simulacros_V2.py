import streamlit as st
import pandas as pd
import plotly.express as px
from statistics import mode,median,mean
from streamlit_extras.metric_cards import style_metric_cards

# Tablero principal
st.set_page_config(layout = "wide")
#st.title("TABLERO SIMULACROS ICFES")
#st.subheader("Resultados")

#Cargamos los datos
datos = pd.read_excel("Resultados_Simulacro_ICFES.xlsx")

# Definir funciones para calcular métricas

def calcular_promedio(grupo):
  """
  Calcula el promedio de puntajes para un grupo específico.

  Argumentos:
    grupo (int): El número de grupo.

  Retorno:
    float: El promedio de puntajes.
  """
  promedio_grupo = datos[datos['Grupo'] == grupo]['Puntaje global'].mean()
  return promedio_grupo

def calcular_mediana(grupo):
  """
  Calcula la mediana de puntajes para un grupo específico.

  Argumentos:
    grupo (int): El número de grupo.

  Retorno:
    float: La mediana de puntajes.
  """
  mediana_grupo = datos[datos['Grupo'] == grupo]['Puntaje global'].median()
  return mediana_grupo

def calcular_desviacion_estandar(grupo):
  """
  Calcula la desviación estándar de puntajes para un grupo específico.

  Argumentos:
    grupo (int): El número de grupo.

  Retorno:
    float: La desviación estándar de puntajes.
  """
  desviacion_estandar_grupo = datos[datos['Grupo'] == grupo]['Puntaje global'].std()
  return desviacion_estandar_grupo

# Configurar el título y el estilo de la página

st.title("Resumen general - Simulacro ICFES")

# Establecer estilo de página con fondo claro
#st.config(layout="wide", backgroundColor="#f0f0f0")

# Mostrar tarjetas con métricas generales

# Calcular promedios, medianas y desviaciones estándar generales
promedio_general = round(datos['Puntaje global'].mean(),2)
mediana_general = round(datos['Puntaje global'].median(),2)
desviacion_estandar_general = round(datos['Puntaje global'].std(),2)

# Mostrar tarjetas con las métricas
col1, col2, col3 = st.columns(3)
with col1:
  st.metric(label="Promedio general", value=promedio_general, delta=0)
with col2:
  st.metric(label="Mediana general", value=mediana_general)
with col3:
  st.metric(label="Desviación estándar general", value=desviacion_estandar_general)
style_metric_cards(border_color="#3A74E7")
# Mostrar gráfico de barras de distribución de puntajes por grupo

# Agrupar datos por grupo y calcular promedios de puntajes globales
datos_agrupados = datos.groupby('Grupo')['Puntaje global'].mean().reset_index()

# Crear gráfico de barras

fig = px.bar(datos_agrupados, x="Grupo", y="Puntaje global", text_auto=True)

# Actualizar el diseño para etiquetas y título
fig.update_layout(
    xaxis_title="Grupo",
    yaxis_title="Puntaje global",
    title="Distribución de puntajes globales por grupo",
)

# Mostrar el gráfico
st.plotly_chart(fig)

##############################################################
## Definir funciones para procesar datos por área
################################################################

def obtener_datos_por_area(area):
  """
  Obtiene los datos de un área específica.

  Argumentos:
    area (str): El nombre del área (Matemáticas, Lectura crítica, etc.).

  Retorno:
    DataFrame: Subconjunto de datos con la información del área seleccionada.
  """
  datos_area = datos[["Grupo","Nombre alumno",f"{area}"]]
  return datos_area

def calcular_metricas_por_area(datos_area,area):
  """
  Calcula las métricas para un área específica.

  Argumentos:
    datos_area (DataFrame): Subconjunto de datos con la información del área seleccionada.

  Retorno:
    Diccionario: Diccionario con las métricas calculadas (promedio, mediana, desviación estándar, percentiles).
  """
  promedio_area = datos_area[f"{area}"].mean()
  mediana_area = datos_area[f"{area}"].median()
  desviacion_estandar_area = datos_area[f"{area}"].std()
  percentiles_area = datos_area[f"{area}"].quantile([0.25, 0.5, 0.75])

  metricas_area = {
    "Promedio": promedio_area,
    "Mediana": mediana_area,
    "Desviación estándar": desviacion_estandar_area,
    "Percentiles": percentiles_area.to_dict()
  }

  return metricas_area

def generar_tabla_metricas(metricas_area):
  """
  Genera una tabla HTML con las métricas de un área.

  Argumentos:
    metricas_area (Diccionario): Diccionario con las métricas calculadas.

  Retorno:
    str: Cadena HTML con la tabla de métricas.
  """
  tabla_html = """
  <table style="border: 1px solid #ddd; border-spacing: 0; width: auto;">
    <tr>
      <th style="padding: 8px; border: 1px solid #ddd;">Métrica</th>
      <th style="padding: 8px; border: 1px solid #ddd;">Valor</th>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd;">Promedio</td>
      <td style="padding: 8px; border: 1px solid #ddd;">{promedio:.2f}</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd;">Mediana</td>
      <td style="padding: 8px; border: 1px solid #ddd;">{mediana:.2f}</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd;">Desviación estándar</td>
      <td style="padding: 8px; border: 1px solid #ddd;">{desviacion_estandar:.2f}</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd;">Percentiles</td>
      <td style="padding: 8px; border: 1px solid #ddd;">
        <ul style="list-style: none; margin: 0; padding: 0;">
          <li>25%: {percentil_25:.2f}</li>
          <li>50%: {percentil_50:.2f}</li>
          <li>75%: {percentil_75:.2f}</li>
        </ul>
      </td>
    </tr>
  </table>
  """.format(
    promedio=metricas_area["Promedio"],
    mediana=metricas_area["Mediana"],
    desviacion_estandar=metricas_area["Desviación estándar"],
    percentil_25=metricas_area["Percentiles"][0.25],
    percentil_50=metricas_area["Percentiles"][0.5],
    percentil_75=metricas_area["Percentiles"][0.75]
  )
  return tabla_html

# Establecer título de la sección
st.title("Análisis por área - Simulacro ICFES")

# Definir lista de áreas para las pestañas
areas = ["Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]

tab1, tab2, tab3, tab4, tab5 = st.tabs(areas)

with tab1:
   st.header("Matemáticas")
   # Obtener datos del área actual
   datos_area = obtener_datos_por_area("Matemáticas")

   # Calcular métricas para el área actual
   metricas_area = calcular_metricas_por_area(datos_area,"Matemáticas")
   
   # Generar tabla HTML con las métricas
   tabla_metricas_html = generar_tabla_metricas(metricas_area)

   # Mostrar la tabla HTML en la pestaña
   st.markdown(tabla_metricas_html, unsafe_allow_html=True)

   # Mostrar histogramas y boxplots (opcional)
   st.plotly_chart(px.histogram(datos_area, x="Matemáticas", text_auto=True))
   st.plotly_chart(px.box(datos_area, x="Matemáticas"))
with tab2:
   st.header("Lectura crítica")
   # Obtener datos del área actual
   datos_area = obtener_datos_por_area("Lectura crítica")

   # Calcular métricas para el área actual
   metricas_area = calcular_metricas_por_area(datos_area,"Lectura crítica")
   
   # Generar tabla HTML con las métricas
   tabla_metricas_html = generar_tabla_metricas(metricas_area)

   # Mostrar la tabla HTML en la pestaña
   st.markdown(tabla_metricas_html, unsafe_allow_html=True)

   # Mostrar histogramas y boxplots (opcional)
   st.plotly_chart(px.histogram(datos_area, x="Lectura crítica", text_auto=True))
   st.plotly_chart(px.box(datos_area, x="Lectura crítica"))

with tab3:
   st.header("Ciencias naturales")
   # Obtener datos del área actual
   datos_area = obtener_datos_por_area("Ciencias naturales")

   # Calcular métricas para el área actual
   metricas_area = calcular_metricas_por_area(datos_area,"Ciencias naturales")
   
   # Generar tabla HTML con las métricas
   tabla_metricas_html = generar_tabla_metricas(metricas_area)

   # Mostrar la tabla HTML en la pestaña
   st.markdown(tabla_metricas_html, unsafe_allow_html=True)

   # Mostrar histogramas y boxplots (opcional)
   st.plotly_chart(px.histogram(datos_area, x="Ciencias naturales", text_auto=True))
   st.plotly_chart(px.box(datos_area, x="Ciencias naturales"))

with tab4:
   st.header("Sociales y ciudadanas")
   # Obtener datos del área actual
   datos_area = obtener_datos_por_area("Sociales y ciudadanas")

   # Calcular métricas para el área actual
   metricas_area = calcular_metricas_por_area(datos_area,"Sociales y ciudadanas")
   
   # Generar tabla HTML con las métricas
   tabla_metricas_html = generar_tabla_metricas(metricas_area)

   # Mostrar la tabla HTML en la pestaña
   st.markdown(tabla_metricas_html, unsafe_allow_html=True)

   # Mostrar histogramas y boxplots (opcional)
   st.plotly_chart(px.histogram(datos_area, x="Sociales y ciudadanas", text_auto=True))
   st.plotly_chart(px.box(datos_area, x="Sociales y ciudadanas"))

with tab5:
   st.header("Inglés")
   # Obtener datos del área actual
   datos_area = obtener_datos_por_area("Inglés")

   # Calcular métricas para el área actual
   metricas_area = calcular_metricas_por_area(datos_area,"Inglés")
   
   # Generar tabla HTML con las métricas
   tabla_metricas_html = generar_tabla_metricas(metricas_area)

   # Mostrar la tabla HTML en la pestaña
   st.markdown(tabla_metricas_html, unsafe_allow_html=True)

   # Mostrar histogramas y boxplots (opcional)
   st.plotly_chart(px.histogram(datos_area, x="Inglés", text_auto=True))
   st.plotly_chart(px.box(datos_area, x="Inglés"))

        



  

