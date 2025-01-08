import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
from statistics import mode,median,mean
from streamlit_extras.metric_cards import style_metric_cards

# Tablero principal
st.set_page_config(layout = "wide")
#st.title("TABLERO SIMULACROS ICFES")
#st.subheader("Resultados")

##############################################################################################################
#Cargamos los datos
#datos = pd.read_excel("Resultados_Simulacro_ICFES.xlsx")
datos = pd.read_excel("Resultados_Simulacro_ICFES_Sinteticos.xlsx")

for col in datos.select_dtypes(include=np.float64):
    datos[col] = datos[col].round(2)
datos.head()

datos["Grupo"] = datos["Grupo"].astype(str)
#datos["AÑO"] = datos["AÑO"].astype(str)
datos["Matemáticas"] = datos["Matemáticas"].astype(int)

################################################# FUNCIONES #################################################

## Dona
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
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text
########################################## Barra lateral #####################################
with st.sidebar:
    #BAENA CHALARCA JERONIMO
    st.header("GRADO")
    grado = ["11", "10"]
    # Crear un selector de grupo con st.selectbox
    grado_seleccionado = st.selectbox("Seleccione el grado:", grado)

    st.header("AÑO")
    año = datos.AÑO.unique().tolist()#[2024, 2025]
    # Crear un selector de grupo con st.selectbox
    #año_seleccionado = st.selectbox("Seleccione el año:", año)

    #datos = datos[(datos['Grupo'].str.startswith(grado_seleccionado)) & (datos['AÑO'] == año_seleccionado)]

    min_value = datos['AÑO'].min()
    max_value = datos['AÑO'].max()

    from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

    # -- Select for high sample rate data
    high_fs = st.sidebar.checkbox('Sin conectar')
    if high_fs:
        datos = datos[datos['Grupo'].isin(['1101','1102','1103','1104'])].copy()
    
    datos = datos[(datos['Grupo'].str.startswith(grado_seleccionado)) 
                  & (datos['AÑO'] <= to_year)
                  & (from_year <= datos['AÑO'])
                  ]

    

################################################# METRICAS EXTERNAS #################################################

media_nacional = 257.0
media_depto = 250.0
media_munpio = 245.0
media_colegio = 266.0
####################################################################################################################
st.title("ANÁLISIS RESULTADOS SIMULACROS E ICFES")

tableros = ["Análisis Puntaje Global", "Análisis Por Area", "Análisis Por Grupo", "Análisis Por Año"]

tab_1, tab_2, tab_3, tab_4 = st.tabs(tableros)

##############################################################################################################
########################################## ANÁLISIS PUNTAJE GLOBAL ###########################################
##############################################################################################################

def ANÁLISIS_POR_GLOBAL():
    """
    ...
    """

with tab_1:
  #st.header("Matemáticas")
  #st.title("Resumen general - Simulacro ICFES")

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

##################################### DATOS SIMULACROS ####################################
  # Inicializar las métricas como None o valores por defecto
  promedio_general_s1 = promedio_general_s2 = promedio_general_s3 = promedio_general_icfes = None
  maximo_s1 = maximo_s2 = maximo_s3 = maximo_icfes = None
  minimo_s1 = minimo_s2 = minimo_s3 = minimo_icfes = None
  S1 = 0
  S2 = 0
  S3 = 0
  ICFES = 0
  # Comprobar si los simulacros están presentes en los datos
  if "S1" in datos["SIMULACRO"].unique():
      S1 = 1
      datos_s1 = datos[datos["SIMULACRO"] == "S1"]
      promedio_general_s1 = round(datos_s1['Puntaje global'].mean(), 2)
      maximo_s1 = max(datos_s1['Puntaje global'])
      minimo_s1 = min(datos_s1['Puntaje global'])
  
  if "S2" in datos["SIMULACRO"].unique():
      S2 = 1
      datos_s2 = datos[datos["SIMULACRO"] == "S2"]
      promedio_general_s2 = round(datos_s2['Puntaje global'].mean(), 2)
      maximo_s2 = max(datos_s2['Puntaje global'])
      minimo_s2 = min(datos_s2['Puntaje global'])
  
  if "S3" in datos["SIMULACRO"].unique():
      S3 = 1
      datos_s3 = datos[datos["SIMULACRO"] == "S3"]
      promedio_general_s3 = round(datos_s3['Puntaje global'].mean(), 2)
      maximo_s3 = max(datos_s3['Puntaje global'])
      minimo_s3 = min(datos_s3['Puntaje global'])

  if "ICFES" in datos["SIMULACRO"].unique():
      ICFES = 1
      datos_icfes = datos[datos["SIMULACRO"] == "ICFES"]
      promedio_general_icfes = round(datos_icfes['Puntaje global'].mean(), 2)
      maximo_icfes = max(datos_icfes['Puntaje global'])
      minimo_icfes = min(datos_icfes['Puntaje global'])
  
  # Mostrar tarjetas con las métricas
  col1, col2, col3 = st.columns(3)
  
  with col1:
      if promedio_general_s1 is not None:
          st.metric(label="Promedio puntaje global simulacro 1", value=promedio_general_s1, delta=round(promedio_general_s1 - media_colegio, 1))
      if promedio_general_s2 is not None:
          st.metric(label="Promedio puntaje global simulacro 2", value=promedio_general_s2, delta=round(promedio_general_s2 - media_colegio, 1))
      if promedio_general_s3 is not None:
          st.metric(label="Promedio puntaje global simulacro 3", value=promedio_general_s3, delta=round(promedio_general_s3 - media_colegio, 1))
      if promedio_general_icfes is not None:
          st.metric(label="Promedio puntaje global ICFES", value=promedio_general_icfes, delta=round(promedio_general_icfes - media_colegio, 1))
  
  with col2:
      if maximo_s1 is not None:
          st.metric(label="Máximo puntaje global simulacro 1", value=maximo_s1)
      if maximo_s2 is not None:
          st.metric(label="Máximo puntaje global simulacro 2", value=maximo_s2)
      if maximo_s3 is not None:
          st.metric(label="Máximo puntaje global simulacro 3", value=maximo_s3)
      if maximo_icfes is not None:
          st.metric(label="Máximo puntaje global ICFES", value=maximo_icfes)
  
  with col3:
      if minimo_s1 is not None:
          st.metric(label="Mínimo puntaje global simulacro 1", value=minimo_s1)
      if minimo_s2 is not None:
          st.metric(label="Mínimo puntaje global simulacro 2", value=minimo_s2)
      if minimo_s3 is not None:
          st.metric(label="Mínimo puntaje global simulacro 3", value=minimo_s3)
      if minimo_icfes is not None:
          st.metric(label="Mínimo puntaje global ICFES", value=minimo_icfes)
  style_metric_cards(border_color="#3A74E7")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Mostrar gráfico de barras de distribución de puntajes por grupo

# Agrupar datos por grupo y calcular promedios de puntajes globales
  datos_agrupados = datos.groupby(['Grupo','SIMULACRO'])['Puntaje global'].mean().round(2).reset_index()

# Crear gráfico de barras

  fig = px.bar(datos_agrupados, x="Grupo", y="Puntaje global", color = 'SIMULACRO', barmode='group', text_auto=True)

# Actualizar el diseño para etiquetas y título
  fig.update_layout(
      xaxis_title="Grupo",
      yaxis_title="Puntaje global",
      title="Distribución de puntajes globales por grupo",
  )

# Mostrar el gráfico
  st.plotly_chart(fig)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  #Ordenar por 'Puntaje global' y seleccionar los top 10
  if S1 == 1:
     top_ten_s1 = datos_s1[["Grupo","Nombre alumno","Puntaje global"]].nlargest(10, 'Puntaje global')

  if S2 == 1:
     top_ten_s2 = datos_s2[["Grupo","Nombre alumno","Puntaje global"]].nlargest(10, 'Puntaje global')

  if S3 == 1:
     top_ten_s3 = datos_s3[["Grupo","Nombre alumno","Puntaje global"]].nlargest(10, 'Puntaje global')

  if ICFES == 1:
     top_ten_icfes = datos_icfes[["Grupo","Nombre alumno","Puntaje global"]].nlargest(10, 'Puntaje global')

  st.subheader("Top Ten Puntajes Globales")

  col1, col2, col3= st.columns(3)
  with col1:
    if S1 == 1:
       st.subheader("Primer Simulacro")
       st.dataframe(top_ten_s1)
    if ICFES == 1:
       st.subheader("ICFES 2024")
       st.dataframe(top_ten_icfes)
  with col2:
    if S2 == 1:
       st.subheader("Segundo Simulacro")
       st.dataframe(top_ten_s2)
  with col3:
    if S3 == 1:
       st.subheader("Tercer Simulacro")
       st.dataframe(top_ten_s3)

##############################################################################################################
############################################# ANÁLISI POR AREA ###############################################
##############################################################################################################

def ANÁLISIS_POR_AREA():
    """
    ...
    """

with tab_2:

# Definir funciones para procesar datos por área
  def obtener_datos_por_area_simulacro(area,simulacro):
    """
    Obtiene los datos de un área específica.

    Argumentos:
      area (str): El nombre del área (Matemáticas, Lectura crítica, etc.).

    Retorno:
      DataFrame: Subconjunto de datos con la información del área seleccionada.
    """
    datos_area_simulacro = datos[["Grupo","Nombre alumno", "SIMULACRO",f"{area}"]]
    datos_area_simulacro = datos_area_simulacro[datos_area_simulacro["SIMULACRO"] == simulacro]
    return datos_area_simulacro

  def calcular_metricas_por_area(datos_area_simulacro,area):
    """
    Calcula las métricas para un área específica.

    Argumentos:
      datos_area (DataFrame): Subconjunto de datos con la información del área seleccionada.

    Retorno:
      Diccionario: Diccionario con las métricas calculadas (promedio, mediana, desviación estándar, percentiles).
    """
    promedio_area = datos_area_simulacro[f"{area}"].mean()
    mediana_area = datos_area_simulacro[f"{area}"].median()
    desviacion_estandar_area = datos_area_simulacro[f"{area}"].std()
    percentiles_area = datos_area_simulacro[f"{area}"].quantile([0.25, 0.5, 0.75])
    maximo_area = max(datos_area_simulacro[f"{area}"])
    minimo_area = min(datos_area_simulacro[f"{area}"])

    metricas_area = {
      "Promedio": promedio_area,
      "Mediana": mediana_area,
      "Desviación estándar": desviacion_estandar_area,
      "Percentiles": percentiles_area.to_dict(),
      "maximo_area": maximo_area,
      "minimo_area": minimo_area
    }

    return metricas_area

  # Establecer título de la sección
  #st.title("Análisis por área - Simulacro ICFES")

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  datos_agrupados_simulacro = datos.groupby(['SIMULACRO'])[["Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]].mean().round(2).reset_index()

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
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  # Definir lista de áreas para las pestañas
  areas = ["Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]

  #tab1, tab2, tab3, tab4, tab5 = st.tabs(areas)

  # Crear un selector de grupo con st.selectbox
  area_seleccionado = st.selectbox("Seleccione el numero de simulacro:", areas)

  #datos = datos[datos["SIMULACRO"] == simulacro_seleccionado]

  st.header(area_seleccionado)
  # Obtener datos del área actual
  if S1 == 1:
     datos_area_s1 = obtener_datos_por_area_simulacro(area_seleccionado,"S1")
  if S2 == 1:
     datos_area_s2 = obtener_datos_por_area_simulacro(area_seleccionado,"S2")
  if S3 == 1:
     datos_area_s3 = obtener_datos_por_area_simulacro(area_seleccionado,"S3")
  if ICFES == 1:
     datos_area_icfes = obtener_datos_por_area_simulacro(area_seleccionado,"ICFES")

  # Calcular métricas para el área actual
  if S1 == 1:
     metricas_area_s1 = calcular_metricas_por_area(datos_area_s1,area_seleccionado)
  if S2 == 1:
     metricas_area_s2 = calcular_metricas_por_area(datos_area_s2,area_seleccionado)
  if S3 == 1:
     metricas_area_s3 = calcular_metricas_por_area(datos_area_s3,area_seleccionado)
  if ICFES == 1:
     metricas_area_icfes = calcular_metricas_por_area(datos_area_icfes,area_seleccionado)
  # Generar tabla HTML con las métricas
  #tabla_metricas_html = generar_tabla_metricas(metricas_area)

  # Mostrar tarjetas con las métricas
  col1, col2, col3 = st.columns(3)
  with col1:
   if S1 == 1:
      st.metric(label="Promedio global simulacro 1", value=metricas_area_s1['Promedio'].round(2))
   if S2 == 1:
      st.metric(label="Promedio global simulacro 2", value=metricas_area_s2['Promedio'].round(2))
   if S3 == 1:
      st.metric(label="Promedio global simulacro 3", value=metricas_area_s3['Promedio'].round(2))
   if ICFES == 1:
      st.metric(label="Promedio global ICFES", value=metricas_area_icfes['Promedio'].round(2))
  with col2:
   if S1 == 1:
      st.metric(label="Máximo simulacro 1", value=metricas_area_s1['maximo_area'])
   if S2 == 1:
      st.metric(label="Máximo simulacro 2", value=metricas_area_s2['maximo_area'])
   if S3 == 1:
      st.metric(label="Máximo simulacro 3", value=metricas_area_s3['maximo_area'])
   if ICFES == 1:
      st.metric(label="Máximo ICFES", value=metricas_area_icfes['maximo_area'])
  with col3:
   if S1 == 1:
      st.metric(label="Mínimo simulacro 1", value= metricas_area_s1['minimo_area'])
   if S2 == 1:
      st.metric(label="Mínimo simulacro 2", value= metricas_area_s2['minimo_area'])
   if S3 == 1:
      st.metric(label="Mínimo simulacro 3", value= metricas_area_s3['minimo_area'])
   if ICFES == 1:
      st.metric(label="Mínimo ICFES", value= metricas_area_icfes['minimo_area'])
  style_metric_cards(border_color="#3A74E7")

  ########### GRAFICO DE BARRAS POR GRUPO PARA MATEMATICAS##########

  # Agrupar datos por grupo y calcular promedios de puntajes Matemáticas
  datos_agrupados = datos.groupby(['Grupo','SIMULACRO'])[area_seleccionado].mean().round(2).reset_index()

  # Crear gráfico de barras

  fig = px.bar(datos_agrupados, x="Grupo", y=area_seleccionado, color = 'SIMULACRO', barmode='group', text_auto=True)

  # Actualizar el diseño para etiquetas y título
  fig.update_layout(
      xaxis_title="Grupo",
      yaxis_title="Matemáticas",
      title=f"Distribución de puntaje {area_seleccionado} por grupo",
  )

  # Mostrar el gráfico
  st.plotly_chart(fig)
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  #Ordenar por área y seleccionar los top 10
  if S1 == 1:
     top_ten_area_s1 = datos_area_s1[["Grupo","Nombre alumno",area_seleccionado]].nlargest(10, area_seleccionado)
  if S2 == 1:
     top_ten_area_s2 = datos_area_s2[["Grupo","Nombre alumno",area_seleccionado]].nlargest(10, area_seleccionado)
  if S3 == 1:
     top_ten_area_s3 = datos_area_s3[["Grupo","Nombre alumno",area_seleccionado]].nlargest(10, area_seleccionado)
  if ICFES == 1:
     top_ten_area_icfes = datos_area_icfes[["Grupo","Nombre alumno",area_seleccionado]].nlargest(10, area_seleccionado)

  st.subheader(f"Top Ten {area_seleccionado}")

  col1, col2, col3= st.columns(3)
  with col1:
    if S1 == 1:
       st.subheader("Primer Simulacro")
       st.dataframe(top_ten_area_s1)

    if ICFES == 1:
       st.subheader("ICFES 2024")
       st.dataframe(top_ten_area_icfes)
  with col2:
    if S2 == 1:
       st.subheader("Segundo Simulacro")
       st.dataframe(top_ten_area_s2)
  with col3:
    if S3 == 1:
       st.subheader("Tercer Simulacro")
       st.dataframe(top_ten_area_s3)

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  #st.plotly_chart(px.histogram(datos_area_s1, x=area_seleccionado, text_auto=True))
  #st.plotly_chart(px.box(datos_area_s1, x=area_seleccionado))

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

##############################################################################################################
############################################# ANÁLISI POR GRUPO ##############################################
##############################################################################################################

def ANÁLISIS_POR_GRUPO():
    """
    ...
    """

with tab_3:

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%       
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

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  # Establecer título de la sección
  #st.title("Análisis por grupo - Simulacros ICFES")

  # Definir la columna por la que se desea agrupar
  columna_grupo = "Grupo"  

  # Obtener grupos únicos de la columna elegida
  grupos_unicos = datos[columna_grupo].unique()

  # Crear un selector de grupo con st.selectbox
  grupo_seleccionado = st.selectbox("Seleccione un grupo:", grupos_unicos)

  datos_agrupados = datos.groupby(['Grupo','SIMULACRO'])[["Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]].mean().round(2).reset_index()

  # derretir datos_agrupados por columnas de areas
  datos_derretidos = datos_agrupados.melt(id_vars=['Grupo','SIMULACRO'], var_name="Área", value_name="Promedio")

  # Seleccionamos grupo
  datos_grupo_seleccionado = datos_derretidos[datos_derretidos.Grupo== grupo_seleccionado]

  # Crear gráfico de barras por area
  fig = px.bar(datos_grupo_seleccionado, x="Área", y="Promedio", color = 'SIMULACRO', barmode='group', text_auto=True)

  # Actualizar el diseño para etiquetas y título
  fig.update_layout(
      xaxis_title="Áreas",
      yaxis_title="Promedios",
      title="Distribución de puntajes por área para cdad grupo grupo",
  )

  # Mostrar el gráfico
  #fig.show()
  st.plotly_chart(fig)

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  # Obtener datos del grupo seleccionado
  datos_grupo = obtener_datos_por_grupo(grupo_seleccionado)

  # Obtener datos del área actual
  if S1 == 1:
     datos_garea_s1 = datos_grupo[datos_grupo["SIMULACRO"] == "S1"]
  if S2 == 1:
     datos_garea_s2 = datos_grupo[datos_grupo["SIMULACRO"] == "S2"]
  if S3 == 1:
     datos_garea_s3 = datos_grupo[datos_grupo["SIMULACRO"] == "S3"]
  if ICFES == 1:
     datos_garea_icfes = datos_grupo[datos_grupo["SIMULACRO"] == "ICFES"]

  # Definir lista de áreas para las pestañas
  areas = ["Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]

  # Crear un selector de grupo con st.selectbox
  garea_seleccionado = st.selectbox("Seleccione el área:", areas)

  # Calcular métricas para el grupo seleccionado
  metricas_grupo_area = calcular_metricas_por_grupo_area(datos_grupo,garea_seleccionado)

  

  #Ordenar por área y seleccionar los top 10
  if S1 == 1:
     top_ten_garea_s1 = datos_garea_s1[["Grupo","Nombre alumno",garea_seleccionado]].nlargest(10, garea_seleccionado)
  if S2 == 1:
     top_ten_garea_s2 = datos_garea_s2[["Grupo","Nombre alumno",garea_seleccionado]].nlargest(10, garea_seleccionado)
  if S3 == 1:
     top_ten_garea_s3 = datos_garea_s3[["Grupo","Nombre alumno",garea_seleccionado]].nlargest(10, garea_seleccionado)
  if ICFES == 1:
     top_ten_garea_icfes = datos_garea_icfes[["Grupo","Nombre alumno",garea_seleccionado]].nlargest(10, garea_seleccionado)

  st.subheader(f"Top Ten {garea_seleccionado}")

  col1, col2, col3= st.columns(3)
  with col1:
    if S1 == 1:
       st.subheader("Primer Simulacro")
       st.dataframe(top_ten_garea_s1)

    if S2 == 1:
       st.subheader("Segundo Simulacro")
       st.dataframe(top_ten_garea_s2)

    #if ICFES == 1:
    #   st.subheader("ICFES")
    #   st.dataframe(top_ten_garea_icfes)
  with col2:
    #if S3 == 1:
    #   st.subheader("Tercer Simulacro")
    #   st.dataframe(top_ten_garea_s3)
  #with col3:
    if S3 == 1:
       st.subheader("Tercer Simulacro")
       st.dataframe(top_ten_garea_s3)

    if ICFES == 1:
      st.subheader("ICFES")
      st.dataframe(top_ten_garea_icfes)

  #tab1, tab2, tab3, tab4, tab5 = st.tabs(areas)
  

  #with tab1:
  #   st.header("Matemáticas")
  #   # Mostrar tarjetas con las métricas
  #   col1, col2, col3 = st.columns(3)
  #   with col1:
  #     promedio = metricas_grupo_area['Promedio'].round(2)
  #     st.metric(label="Promedio", value=promedio)
  #   with col2:
  #     maximo = metricas_grupo_area['maximo_area']
  #     st.metric(label="Máximo", value=maximo)
  #   with col3:
  #     minimo = metricas_grupo_area['minimo_area']
  #     st.metric(label="Mínimo", value=minimo)
  #   style_metric_cards(border_color="#3A74E7")

  
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  # Mostrar histogramas y boxplots (opcional)
  #st.plotly_chart(px.histogram(datos_grupo, x="Matemáticas"))
  #st.plotly_chart(px.box(datos_grupo, x="Matemáticas"))
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

##############################################################################################################
############################################## ANÁLISIS POR AÑO ##############################################
##############################################################################################################

def ANÁLISIS_POR_AÑO():
    """
    ...
    """
 
with tab_4:

  st.header("...")
  #st.title("Resumen general - Simulacro ICFES")

  # Hacemos una copia para convertir la columna AÑO a string y esta sea tratada como una variable ordinal
  df = datos.copy()
  df['AÑO'] = df['AÑO'].astype(str)

  datos_año = df.groupby(['AÑO','SIMULACRO'])[['Puntaje global',"Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]].mean().round(2).reset_index()

  # Crear gráfico de barras comparativo por año por prueba
  fig = px.bar(datos_año, x="SIMULACRO", y='Puntaje global', color = 'AÑO', barmode='group', text_auto=True)

   # Actualizar el diseño para etiquetas y título
  fig.update_layout(
       xaxis_title="Pruebas",
       yaxis_title="Promedios",
       title="Distribución de puntajes por año para cada prueba",
     )

  # Mostrar el gráfico
  #fig.show()
  st.plotly_chart(fig)


  ###################
  datos_agrupados_simulacro = datos_año.groupby(['AÑO','SIMULACRO'])[["Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]].mean().round(2).reset_index()

  datos1 = datos_agrupados_simulacro.melt(id_vars=['AÑO','SIMULACRO'], var_name="Área", value_name="Promedio")

  # Obtener grupos únicos de la columna elegida
  simulacro_unicos = datos1.SIMULACRO.unique()

  # Crear un selector de grupo con st.selectbox
  simulacro_seleccionado = st.selectbox("Seleccione un prueba:", simulacro_unicos)
   # derretir datos_agrupados por columnas de areas

  datos1 = datos1[datos1['SIMULACRO']==simulacro_seleccionado]

  fig = px.bar(datos1
             , x="Área"
             , y="Promedio"
             , color = 'AÑO'
             , barmode='group'
             , text_auto=True
             )

   # Actualizar el diseño para etiquetas y título
  fig.update_layout(
    xaxis_title="Pruebas",
    yaxis_title="Promedios",
    title=f"Distribución de puntajes en el {simulacro_seleccionado} por año agrupados por area",
  )

  st.plotly_chart(fig)

########################################################################################################################
# Mostrar gráfico de barras de distribución de puntajes por area y año

datos_historicos = pd.read_excel("Resultados_historico_2016_2024.xlsx")

# Obtener años únicos de la columna elegida
año = datos_historicos.Año.dt.year.unique()

# Obtener grupos únicos de la columna elegida
area = datos_historicos.Area.unique()

# Crear un selector de grupo con st.selectbox
Año_seleccionado = st.selectbox("Seleccione un año:", año)

# Crear un selector de grupo con st.selectbox
Area_seleccionado = st.selectbox("Seleccione un area:", area)

datos_historicos = datos_historicos[(datos_historicos.Sector == 'OFICIAL') & (datos_historicos.Area == Area_seleccionado) & (datos_historicos.Año.dt.year == int(Año_seleccionado))].copy()


# Agrupar datos por grupo y calcular promedios de puntajes globales
datos_agrupados = datos_historicos.groupby(['Año','Colegio'])['Promedio'].mean().round(2).reset_index()

# Ordenar por valores
datos_agrupados = datos_agrupados.sort_values(by="Promedio", ascending=True)

# Crear gráfico de barras

fig = px.bar(datos_agrupados, x="Promedio", y="Colegio", barmode='group', text_auto=True)

# Actualizar el diseño para etiquetas y título
fig.update_layout(
      xaxis_title="Grupo",
      yaxis_title="Puntaje global",
      title="Distribución de puntajes globales por grupo",
  )

# Mostrar el gráfico
st.plotly_chart(fig)

########################################################################################################################

# Insertar GIF desde un archivo local o URL
#gif_url = "Resultados_ICFES2016_2024.gif"
#st.image(gif_url, caption="¡Bienvenidos al tablero!", use_container_width=True)
#st.markdown(
#    f'<div style="text-align: center;"><img src="{gif_url}" width="500"></div>',
#    unsafe_allow_html=True
#)

#gif_path = "Resultados_ICFES2016_2024.gif"
#file_ = open(gif_path, "rb")
#contents = file_.read()
#data_url = f"data:image/gif;base64,{contents.decode('latin1')}"
#st.markdown(f'<img src="{data_url}" width="100">', unsafe_allow_html=True)

from PIL import Image

# Cargar el archivo subido
uploaded_file = "Resultados_ICFES2016_2024.png"

if uploaded_file is not None:
    gif_url = uploaded_file
    st.markdown(
        f'<div style="text-align: center;"><img src="{gif_url}" width="500"></div>',
        unsafe_allow_html=True
    )

