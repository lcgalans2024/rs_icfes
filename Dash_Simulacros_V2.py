import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from statistics import mode,median,mean
from streamlit_extras.metric_cards import style_metric_cards

# Tablero principal
st.set_page_config(layout = "wide")
#st.title("TABLERO SIMULACROS ICFES")
#st.subheader("Resultados")

#Cargamos los datos
datos = pd.read_excel("Resultados_Simulacro_ICFES.xlsx")

for col in datos.select_dtypes(include=np.float64):
    datos[col] = datos[col].round(2)
datos.head()

datos["Matemáticas"] = datos["Matemáticas"].astype(int)

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
  maximo_area = max(datos_area[f"{area}"])
  minimo_area = min(datos_area[f"{area}"])

  metricas_area = {
    "Promedio": promedio_area,
    "Mediana": mediana_area,
    "Desviación estándar": desviacion_estandar_area,
    "Percentiles": percentiles_area.to_dict(),
    "maximo_area": maximo_area,
    "minimo_area": minimo_area
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
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd;">Máximo</td>
      <td style="padding: 8px; border: 1px solid #ddd;">{maximo_area:.2f}</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd;">Mínimo</td>
      <td style="padding: 8px; border: 1px solid #ddd;">{mínimo_area:.2f}</td>
    </tr>
  </table>
  """.format(
    promedio=metricas_area["Promedio"],
    mediana=metricas_area["Mediana"],
    desviacion_estandar=metricas_area["Desviación estándar"],
    percentil_25=metricas_area["Percentiles"][0.25],
    percentil_50=metricas_area["Percentiles"][0.5],
    percentil_75=metricas_area["Percentiles"][0.75],
    maximo_area=metricas_area["maximo_area"],
    mínimo_area=metricas_area["minimo_area"]
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

   # Mostrar tarjetas con las métricas
   col1, col2, col3 = st.columns(3)
   with col1:
    promedio = metricas_area['Promedio'].round(2)
    st.metric(label="Promedio general", value=promedio, delta=0)
   with col2:
    maximo = metricas_area['maximo_area']
    st.metric(label="Máximo", value=maximo)
   with col3:
    minimo = metricas_area['minimo_area']
    st.metric(label="Mínimo", value=minimo)
   style_metric_cards(border_color="#3A74E7")

   # Mostrar la tabla HTML en la pestaña
   #st.markdown(tabla_metricas_html, unsafe_allow_html=True)
  
  ############ GRAFICO DE BARRAS POR GRUPO PARA MATEMATICAS##########

   # Agrupar datos por grupo y calcular promedios de puntajes Matemáticas
   datos_agrupados = datos.groupby('Grupo')['Matemáticas'].mean().reset_index()

   # Crear gráfico de barras

   fig = px.bar(datos_agrupados, x="Grupo", y="Matemáticas", text_auto=True)

   # Actualizar el diseño para etiquetas y título
   fig.update_layout(
       xaxis_title="Grupo",
       yaxis_title="Matemáticas",
       title="Distribución de puntaje Matemáticas por grupo",
   )

   # Mostrar el gráfico
   st.plotly_chart(fig)
  ##########################################################################
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

   # Mostrar tarjetas con las métricas
   col1, col2, col3 = st.columns(3)
   with col1:
    promedio = metricas_area['Promedio'].round(2)
    st.metric(label="Promedio general", value=promedio, delta=0)
   with col2:
    maximo = metricas_area['maximo_area']
    st.metric(label="Máximo", value=maximo)
   with col3:
    minimo = metricas_area['minimo_area']
    st.metric(label="Mínimo", value=minimo)
   style_metric_cards(border_color="#3A74E7")

   # Mostrar la tabla HTML en la pestaña
   #st.markdown(tabla_metricas_html, unsafe_allow_html=True)
   
   ############ GRAFICO DE BARRAS POR GRUPO PARA MATEMATICAS##########

   # Agrupar datos por grupo y calcular promedios de puntajes Lectura crítica
   datos_agrupados = datos.groupby('Grupo')['Lectura crítica'].mean().reset_index()

   # Crear gráfico de barras

   fig = px.bar(datos_agrupados, x="Grupo", y="Lectura crítica", text_auto=True)

   # Actualizar el diseño para etiquetas y título
   fig.update_layout(
       xaxis_title="Grupo",
       yaxis_title="Lectura crítica",
       title="Distribución de puntaje Lectura crítica por grupo",
   )

   # Mostrar el gráfico
   st.plotly_chart(fig)
  ##########################################################################

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

   # Mostrar tarjetas con las métricas
   col1, col2, col3 = st.columns(3)
   with col1:
    promedio = metricas_area['Promedio'].round(2)
    st.metric(label="Promedio general", value=promedio, delta=0)
   with col2:
    maximo = metricas_area['maximo_area']
    st.metric(label="Máximo", value=maximo)
   with col3:
    minimo = metricas_area['minimo_area']
    st.metric(label="Mínimo", value=minimo)
   style_metric_cards(border_color="#3A74E7")

   # Mostrar la tabla HTML en la pestaña
   #st.markdown(tabla_metricas_html, unsafe_allow_html=True)
   
   ############ GRAFICO DE BARRAS POR GRUPO PARA MATEMATICAS##########

   # Agrupar datos por grupo y calcular promedios de puntajes Ciencias naturales
   datos_agrupados = datos.groupby('Grupo')['Ciencias naturales'].mean().reset_index()

   # Crear gráfico de barras

   fig = px.bar(datos_agrupados, x="Grupo", y="Ciencias naturales", text_auto=True)

   # Actualizar el diseño para etiquetas y título
   fig.update_layout(
       xaxis_title="Grupo",
       yaxis_title="Ciencias naturales",
       title="Distribución de puntaje Ciencias naturales por grupo",
   )

   # Mostrar el gráfico
   st.plotly_chart(fig)
  ##########################################################################

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

   # Mostrar tarjetas con las métricas
   col1, col2, col3 = st.columns(3)
   with col1:
    promedio = metricas_area['Promedio'].round(2)
    st.metric(label="Promedio general", value=promedio, delta=0)
   with col2:
    maximo = metricas_area['maximo_area']
    st.metric(label="Máximo", value=maximo)
   with col3:
    minimo = metricas_area['minimo_area']
    st.metric(label="Mínimo", value=minimo)
   style_metric_cards(border_color="#3A74E7")

   # Mostrar la tabla HTML en la pestaña
   #st.markdown(tabla_metricas_html, unsafe_allow_html=True)

   ############ GRAFICO DE BARRAS POR GRUPO PARA MATEMATICAS##########

   # Agrupar datos por grupo y calcular promedios de puntajes Sociales y ciudadanas
   datos_agrupados = datos.groupby('Grupo')['Sociales y ciudadanas'].mean().reset_index()

   # Crear gráfico de barras

   fig = px.bar(datos_agrupados, x="Grupo", y="Sociales y ciudadanas", text_auto=True)

   # Actualizar el diseño para etiquetas y título
   fig.update_layout(
       xaxis_title="Grupo",
       yaxis_title="Sociales y ciudadanas",
       title="Distribución de puntaje Sociales y ciudadanas por grupo",
   )

   # Mostrar el gráfico
   st.plotly_chart(fig)
  ##########################################################################

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

   # Mostrar tarjetas con las métricas
   col1, col2, col3 = st.columns(3)
   with col1:
    promedio = metricas_area['Promedio'].round(2)
    st.metric(label="Promedio general", value=promedio, delta=0)
   with col2:
    maximo = metricas_area['maximo_area']
    st.metric(label="Máximo", value=maximo)
   with col3:
    minimo = metricas_area['minimo_area']
    st.metric(label="Mínimo", value=minimo)
   style_metric_cards(border_color="#3A74E7")

   # Mostrar la tabla HTML en la pestaña
   #st.markdown(tabla_metricas_html, unsafe_allow_html=True)

   ############ GRAFICO DE BARRAS POR GRUPO PARA MATEMATICAS##########

   # Agrupar datos por grupo y calcular promedios de puntajes Inglés
   datos_agrupados = datos.groupby('Grupo')['Inglés'].mean().reset_index()

   # Crear gráfico de barras

   fig = px.bar(datos_agrupados, x="Grupo", y="Inglés", text_auto=True)

   # Actualizar el diseño para etiquetas y título
   fig.update_layout(
       xaxis_title="Grupo",
       yaxis_title="Inglés",
       title="Distribución de puntaje Inglés por grupo",
   )

   # Mostrar el gráfico
   st.plotly_chart(fig)
  ##########################################################################

   # Mostrar histogramas y boxplots (opcional)
   st.plotly_chart(px.histogram(datos_area, x="Inglés", text_auto=True))
   st.plotly_chart(px.box(datos_area, x="Inglés"))

##############################################################
## Analisis por grupo
################################################################
        
# Definir funciones para procesar datos por grupo

def obtener_datos_por_grupo(grupo):
  """
  Obtiene los datos de un grupo específico (Género, Grado, etc.).

  Argumentos:
    grupo (str): El nombre del grupo (Masculino, Femenino, 11°, 12°, etc.).

  Retorno:
    DataFrame: Subconjunto de datos con la información del grupo seleccionado.
  """
  datos_grupo = datos[datos["Grupo"] == grupo]
  return datos_grupo

def calcular_metricas_por_grupo(datos_grupo):
  """
  Calcula las métricas para un grupo específico.

  Argumentos:
    datos_grupo (DataFrame): Subconjunto de datos con la información del grupo seleccionado.

  Retorno:
    Diccionario: Diccionario con las métricas calculadas (promedio, mediana, desviación estándar, percentiles).
  """
  promedio_grupo = datos_grupo[columna].mean()
  mediana_grupo = datos_grupo[columna].median()
  desviacion_estandar_grupo = datos_grupo[columna].std()
  percentiles_grupo = datos_grupo[columna].quantile([0.25, 0.5, 0.75])
  maximo_grupo = max(datos_grupo[columna])
  minimo_grupo = min(datos_grupo[columna])

  metricas_grupo = {
    "Promedio": promedio_grupo,
    "Mediana": mediana_grupo,
    "Desviación estándar": desviacion_estandar_grupo,
    "Percentiles": percentiles_grupo.to_dict(),
    "maximo_area": maximo_grupo,
    "minimo_area": minimo_grupo
  }

  return metricas_grupo

def calcular_metricas_por_grupo_area(datos_grupo,columna):
  """
  Calcula las métricas para un grupo específico.

  Argumentos:
    datos_grupo (DataFrame): Subconjunto de datos con la información del grupo seleccionado.

  Retorno:
    Diccionario: Diccionario con las métricas calculadas (promedio, mediana, desviación estándar, percentiles).
  """
  promedio_grupo = datos_grupo[columna].mean()
  mediana_grupo = datos_grupo[columna].median()
  desviacion_estandar_grupo = datos_grupo[columna].std()
  percentiles_grupo = datos_grupo[columna].quantile([0.25, 0.5, 0.75])
  maximo_grupo = max(datos_grupo[columna])
  minimo_grupo = min(datos_grupo[columna])

  metricas_grupo_area = {
    "Promedio": promedio_grupo,
    "Mediana": mediana_grupo,
    "Desviación estándar": desviacion_estandar_grupo,
    "Percentiles": percentiles_grupo.to_dict(),
    "maximo_area": maximo_grupo,
    "minimo_area": minimo_grupo
  }

  return metricas_grupo_area

def generar_tabla_metricas(metricas_grupo):
  """
  Genera una tabla HTML con las métricas de un grupo.

  Argumentos:
    metricas_grupo (Diccionario): Diccionario con las métricas calculadas.

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
    promedio=metricas_grupo["Promedio"],
    mediana=metricas_grupo["Mediana"],
    desviacion_estandar=metricas_grupo["Desviación estándar"],
    percentil_25=metricas_grupo["Percentiles"][0.25],
    percentil_50=metricas_grupo["Percentiles"][0.5],
    percentil_75=metricas_grupo["Percentiles"][0.75]
  )
  return tabla_html

# Establecer título de la sección
st.title("Análisis por grupo - Simulacro ICFES")

# Definir la columna por la que se desea agrupar
columna_grupo = "Grupo"  # Ejemplo: "Género", "Grado", etc.

# Obtener grupos únicos de la columna elegida
grupos_unicos = datos[columna_grupo].unique()

# Crear un selector de grupo con st.selectbox
grupo_seleccionado = st.selectbox("Seleccione un grupo:", grupos_unicos)

###################################################################################

datos_agrupados = datos.groupby('Grupo')[["Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]].mean().reset_index()

# derretir datos_agrupados por columnas de areas
datos_derretidos = datos_agrupados.melt(id_vars="Grupo", var_name="Área", value_name="Promedio")

# Seleccionamos grupo
datos_grupo_seleccionado = datos_derretidos[datos_derretidos.Grupo== grupo_seleccionado]

# Crear gráfico de barras
fig = px.bar(datos_grupo_seleccionado, x="Área", y="Promedio", text_auto=True)

# Actualizar el diseño para etiquetas y título
fig.update_layout(
    xaxis_title="Áreas",
    yaxis_title="Promedios",
    title="Distribución de puntajes por área y por grupo",
)

# Mostrar el gráfico
#fig.show()
st.plotly_chart(fig)

####################################################################################

# Obtener datos del grupo seleccionado
datos_grupo = obtener_datos_por_grupo(grupo_seleccionado)

# Calcular métricas para el grupo seleccionado
metricas_grupo_area = calcular_metricas_por_grupo_area(datos_grupo,"Matemáticas")

# Definir lista de áreas para las pestañas
areas = ["Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]

tab1, tab2, tab3, tab4, tab5 = st.tabs(areas)

with tab1:
   st.header("Matemáticas")
   # Mostrar tarjetas con las métricas
   col1, col2, col3 = st.columns(3)
   with col1:
     promedio = metricas_grupo_area['Promedio'].round(2)
     st.metric(label="Promedio general", value=promedio, delta=0)
   with col2:
     maximo = metricas_grupo_area['maximo_area']
     st.metric(label="Máximo", value=maximo)
   with col3:
     minimo = metricas_grupo_area['minimo_area']
     st.metric(label="Mínimo", value=minimo)
   style_metric_cards(border_color="#3A74E7")

# Generar tabla HTML con las métricas
#tabla_metricas_html = generar_tabla_metricas(metricas_grupo)

# Mostrar la tabla HTML y otras visualizaciones (opcional)
#st.markdown(tabla_metricas_html, unsafe_allow_html=True)

# Mostrar histogramas y boxplots (opcional)
st.plotly_chart(px.histogram(datos_grupo, x="Matemáticas"))
st.plotly_chart(px.box(datos_grupo, x="Matemáticas"))

  

