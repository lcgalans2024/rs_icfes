import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import io
from statistics import mode,median,mean
from streamlit_extras.metric_cards import style_metric_cards

# Tablero principal
st.set_page_config(layout = "wide")
#st.title("TABLERO SIMULACROS ICFES")
#st.subheader("Resultados")

##############################################################################################################
#Cargamos los datos
datos = pd.read_excel("Resultados_Simulacro_ICFES.xlsx")
datos = datos.dropna()
#datos = pd.read_excel("Resultados_Simulacro_ICFES_Sinteticos.xlsx")

#datos.Grupo.replace(1001, "101G", inplace=True)
#datos.Grupo.replace(1002, "102G", inplace=True)
#datos.Grupo.replace(1003, "103G", inplace=True)
#datos.Grupo.replace(1004, "104G", inplace=True)
datos["Grupo"] = datos["Grupo"].astype(str)
for col in datos.select_dtypes(include=np.float64):
    datos[col] = datos[col].round(2)
datos.head()


#datos["AÑO"] = datos["AÑO"].astype(str)
#datos["Matemáticas"] = datos["Matemáticas"].astype(int)

datos_año = datos.copy()

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

def BARRA_LATERAL():
    """
    ...
    """

########################################## Barra lateral #####################################
with st.sidebar:
    #BAENA CHALARCA JERONIMO
    st.header("GRADO")
    grado = ["11", "10"]
    # Crear un selector de grupo con st.selectbox
    grado_seleccionado = st.selectbox("Seleccione el grado:", grado)

    # Crear un selector de año
    st.header("AÑO")
    año = datos.AÑO.unique().tolist()#[2024, 2025]
    año_seleccionado = st.selectbox("Seleccione el año:", año)

    # Deslizador para seleccionar rango de años
    #min_value = datos['AÑO'].min()
    #max_value = datos['AÑO'].max()
    #
    #from_year, to_year = st.slider(
    #'Cuáles son los añños de interes?',
    #min_value=min_value,
    #max_value=max_value,
    #value=[min_value, max_value])

    # -- Select for high sample rate data
    high_fs = st.sidebar.checkbox('Sin conectar')
    if high_fs:
        datos = datos[datos['Grupo'].isin(['1101','1102','1103','1104'])].copy()
    
    #datos = datos[(datos['Grupo'].str.startswith(grado_seleccionado)) 
    #              & (datos['AÑO'] <= to_year)
    #              & (from_year <= datos['AÑO'])
    #              ]

    datos = datos[(datos['Grupo'].str.startswith(grado_seleccionado)) & (datos['AÑO'] == año_seleccionado)]

    # Validar si hay datos
    #if datos.empty:
    #    st.warning("⚠️ No se tienen datos aún para este grado en el año seleccionado.")
    #else:
    #    st.success("✅ Datos cargados correctamente.")
        #st.dataframe(datos) # Mostrar los datos

################################################# METRICAS EXTERNAS #################################################

media_nacional = 257.0
media_depto = 250.0
media_munpio = 245.0
media_colegio = 266.0
####################################################################################################################
st.title("ANÁLISIS RESULTADOS INSTITUCIONALES")
st.subheader("⚠️ Este es un espacio en construcción ⚠️")

tableros = ["Análisis Puntaje Global", "Análisis Por Area", "Análisis Por Grupo", "Análisis Por Año"
            ,"Olimpiadas Institucionales","Descarga de resultados"
            ]

tab_1, tab_2, tab_3, tab_4, tab_5, tab_6 = st.tabs(tableros)

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
  datos_agrupados = datos.groupby(['Grupo','SIMULACRO','AÑO'])['Puntaje global'].mean().round(2).reset_index()
  datos_agrupados["Grupo"] = datos_agrupados["Grupo"].astype(str)
# Validar si hay datos
  if datos_agrupados.empty:
      st.warning("⚠️ No se tienen datos aún para este grado en el año seleccionado.")
  else:
     # Crear gráfico de barras

      fig = px.bar(datos_agrupados, x="Grupo", y="Puntaje global", color = 'SIMULACRO', barmode='group', text_auto=True)

#     Actualizar el diseño para etiquetas y título
      fig.update_layout(
          xaxis_title="Grupo",
          yaxis_title="Puntaje global",
          title="Distribución de puntajes globales por grupo",
      )

#     Mostrar el gráfico
      st.plotly_chart(fig)

#%    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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

  # Validar si hay datos
  if datos_agrupados_simulacro.empty:
      st.warning("⚠️ No se tienen datos aún para este grado en el año seleccionado.")
  else:
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

  # Validar si hay datos
  if datos_agrupados.empty:
      st.warning("⚠️ No se tienen datos aún para este grado en el año seleccionado.")
  else:   
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


#%    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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

  #st.header("...")
  #st.title("Resumen general - Simulacro ICFES")

  # Hacemos una copia para convertir la columna AÑO a string y esta sea tratada como una variable ordinal
  datos_año = datos_año[(datos_año['Grupo'].str.startswith(grado_seleccionado))]
  df = datos_año.copy()
  df['AÑO'] = df['AÑO'].astype(str)

  datos_año1 = df.groupby(['AÑO','SIMULACRO'])[['Puntaje global',"Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]].mean().round(2).reset_index()

  # Crear gráfico de barras comparativo por año por prueba
  fig = px.bar(datos_año1, x="SIMULACRO", y='Puntaje global', color = 'AÑO', barmode='group', text_auto=True)

   # Actualizar el diseño para etiquetas y título
  fig.update_layout(
       xaxis_title="Pruebas",
       yaxis_title="Promedios",
       title="Distribución de puntajes por año para cada prueba",
     )

  # Mostrar el gráfico
  #fig.show()
  st.plotly_chart(fig)
  ##################################################################################
  # Mostrar gráfico de barras de distribución de puntajes por grupo

  # Agrupar datos por grupo y calcular promedios de puntajes globales
  datos_agrupados = df.groupby(['Grupo','SIMULACRO','AÑO'])['Puntaje global'].mean().round(2).reset_index()

  # Crear gráfico de barras

  fig = px.bar(datos_agrupados, x="Grupo", y="Puntaje global", color = 'AÑO', barmode='group', text_auto=True)

  # Actualizar el diseño para etiquetas y título
  fig.update_layout(
      xaxis_title="Grupo",
      yaxis_title="Puntaje global",
      title="Distribución de puntajes globales por grupo",
  )

  # Mostrar el gráfico
  #st.plotly_chart(fig)


  ##################################################################################
  datos_agrupados_simulacro = datos_año1.groupby(['AÑO','SIMULACRO'])[["Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]].mean().round(2).reset_index()

  datos1 = datos_agrupados_simulacro.melt(id_vars=['AÑO','SIMULACRO'], var_name="Área", value_name="Promedio")

  # Obtener grupos únicos de la columna elegida
  #simulacro_unicos = datos1.SIMULACRO.unique()

  # Crear un selector de grupo con st.selectbox
  #simulacro_seleccionado = st.selectbox("Seleccione un prueba:", simulacro_unicos)
   # derretir datos_agrupados por columnas de areas

  #datos1 = datos1[datos1['SIMULACRO']==simulacro_seleccionado]

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
    title=f"Distribución de puntajes en el  por año agrupados por area",
  )

  #st.plotly_chart(fig)

  ########################################################################################################################
  st.subheader("Interinstitutional")
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


##############################################################################################################
############################################## ANÁLISIS OLIMPIADAS ##############################################
##############################################################################################################

def ANÁLISIS_OLIMPIADAS():
    """
    ...
    """
 
with tab_5:

  st.header("Olimpiadas Institucionales")

  # Cargar los datos de las olimpiadas
  df_claves = pd.read_excel('Olimpiadas_Institucionales.xlsx', sheet_name='Claves')
  df_olimpiadas = pd.read_excel("Olimpiadas_Institucionales.xlsx", sheet_name='Full')

  df_olimpiadas['QuizClass'].replace({'IEOS_601':'G_601', 'IEOS_602':'G_602', 'IEOS_603':'G_603', 'IEOS_604':'G_604'
                                      ,'IEOS_7':'G_701', 'IEOS_702':'G_702', 'IEOS_703':'G_703', 'IEOS_704':'G_704'
                                      ,'IEOS_801':'G_801','IEOS_802':'G_802','IEOS_803':'G_803','IEOS_804':'G_804'}, inplace=True)

  #st.dataframe(df_claves.head())

  # Obtener años únicos de la columna elegida
  #año = datos_olimpiadas.Año.unique()

  # Crear un diccionario de mapeo para renombrar las columnas
  column_mapping1 = {f'Stu{i}': f'p{i}' for i in range(1, 17)}
  column_mapping2 = {f'Mark{i}': f'CORRECTASp{i}' for i in range(1, 17)}
  column_mapping3 = {f'Points{i}': f'Pts_p{i}' for i in range(1, 17)}

  # Renombrar las columnas en el DataFrame
  df_olimpiadas.rename(columns=column_mapping1, inplace=True)
  df_olimpiadas.rename(columns=column_mapping2, inplace=True)
  df_olimpiadas.rename(columns=column_mapping3, inplace=True)
  df_olimpiadas.rename(columns={"QuizName": "GRADO", "QuizClass": "GRUPO", "CustomID":"MATRICULA", "Earned Points":"PUNTAJE", "PercentCorrect":"%_CORRECTO"}, inplace=True)

  # Creamos la columna de grado
  df_olimpiadas['GRADO'] = np.where(df_olimpiadas['GRUPO'].isin(["G_601","G_602","G_603","G_604"]), 'SEXTO',
                       np.where(df_olimpiadas['GRUPO'].isin(["G_701","G_702","G_703","G_704"]), 'SEPTIMO','OCTAVO'))

  df_resultados = df_olimpiadas[[#'GRADO',
                                 'GRUPO', 'FirstName', 'LastName'
                                 #, 'MATRICULA'
                                 , 'PUNTAJE', '%_CORRECTO'
                               #,'p1', 'Pts_p1', 'p2', 'Pts_p2', 'p3', 'Pts_p3', 'p4', 'Pts_p4', 'p5', 'Pts_p5', 'p6', 'Pts_p6', 'p7', 'Pts_p7', 'p8', 'Pts_p8', 'p9', 'Pts_p9', 'p10', 'Pts_p10', 'p11', 'Pts_p11', 'p12', 'Pts_p12', 'p13', 'Pts_p13', 'p14', 'Pts_p14', 'p15', 'Pts_p15', 'p16', 'Pts_p16'
                         #, 'CORRECTASp1', 'CORRECTASp2', 'CORRECTASp3', 'CORRECTASp4', 'CORRECTASp5', 'CORRECTASp6', 'CORRECTASp7', 'CORRECTASp8', 'CORRECTASp9', 'CORRECTASp10', 'CORRECTASp11', 'CORRECTASp12', 'CORRECTASp13', 'CORRECTASp14', 'CORRECTASp15', 'CORRECTASp16'
                         ]]
  df_resultados['NOTA'] = df_resultados['%_CORRECTO'] /20
  df_resultados['NOTA'] = df_resultados['NOTA'].round(2)
  df_resultados['DESEMPEÑO'] = np.where(df_resultados['NOTA'] >= 4.6, 'SUPERIOR',
                                       np.where(df_resultados['NOTA'] >= 4.0, 'ALTO',
                                               np.where(df_resultados['NOTA'] >= 3.0, 'BÁSICO','BAJO')))
  

  # Derretir el DataFrame por las columnas P1, P2, P3, P4 y P5
  id_vars = ['GRADO', 'GRUPO', 'FirstName', 'LastName', 'StudentID',
           'MATRICULA', 'PUNTAJE', 'Possible Points', '%_CORRECTO']
  value_vars = column_mapping1.values()

  df_melted = pd.melt(df_olimpiadas, id_vars=id_vars, value_vars=value_vars, var_name='PREGUNTA', value_name='OPCION_MARCADA')
  df_melted['OPCION_MARCADA'] = df_melted['OPCION_MARCADA'].fillna('NM')

  # Merge df_melted with df_claves on PREGUNTA
  df_merged = pd.merge(df_melted, df_claves, on='PREGUNTA', how='left')

  # Create the CORRECTAS column
  df_merged['CORRECTAS'] = np.where(df_merged['OPCION_MARCADA'] == df_merged['CORRECTA'], 'C', 'X')
  df_merged['ACIERTOS'] = np.where(df_merged['CORRECTAS'] == 'C', 1, 0)

  # Drop the CORRECTA column as it's no longer needed
  df_merged.drop(columns=['CORRECTA'], inplace=True)

  # Convertir la columna PREGUNTA en una categoría con el orden deseado
  df_merged['PREGUNTA'] = pd.Categorical(df_merged['PREGUNTA'], categories=[f'p{i}' for i in range(1, 17)], ordered=True)

  # Ordenar el DataFrame
  df_merged = df_merged.sort_values(by=['GRUPO', 'LastName', 'PREGUNTA'])

  # Eliminar las filas de las preguntas p1, p4, p7 y p14
  df_12p = df_merged[~df_merged['PREGUNTA'].isin(['p1', 'p4', 'p7', 'p14'])]

  ############################## Crear el gráfico de barras por grupo ##############################

  df_GRADO = df_12p.groupby(['GRADO']).agg(
    count=('PREGUNTA', 'size'),
    aciertos=('ACIERTOS', 'sum'),
    proporcion_aciertos=('ACIERTOS', 'mean')
    ,percent_correct=('%_CORRECTO', 'mean')

  ).reset_index()

  df_GRADO['proporcion_aciertos'] = df_GRADO['proporcion_aciertos'].round(2)

  #st.dataframe(df_GRADO.head())

  fig = px.bar(df_GRADO, x="GRADO", y="proporcion_aciertos", barmode='group', text_auto=True)

  # Actualizar el diseño para etiquetas y título
  fig.update_layout(
        xaxis_title="Grado",
        yaxis_title="% Correctas",
        title="Distribución de % correcto por grado",
    )
  
  # Mostrar el gráfico
  st.plotly_chart(fig)

  ############################## Crear el gráfico de barras por grupo ##############################

  # Calcular el promedio de aciertos por grupo
  df_grupo = df_12p.groupby(['GRUPO']).agg(promedio=('%_CORRECTO', 'mean')).reset_index()

  df_grupo['promedio'] = df_grupo['promedio'].round(2)

  fig = px.bar(df_grupo, x="GRUPO", y="promedio", barmode='group', text_auto=True)

  # Actualizar el diseño para etiquetas y título
  fig.update_layout(
        xaxis_title="Grupo",
        yaxis_title="% Correctas",
        title="Distribución Promedio de % correcto por grupo",
    )
  
  # Mostrar el gráfico
  st.plotly_chart(fig)

  ############################## Crear el gráfico de barras apilado por grupo ##############################
  df_grupo_categoria = df_12p.groupby(['GRUPO','CATEGORIA']).agg(
     count=('PREGUNTA', 'size')
     ,aciertos=('ACIERTOS', 'sum')
     ,proporcion_aciertos=('ACIERTOS', 'mean')
     ).reset_index()

  categories = df_grupo_categoria['CATEGORIA'].unique()
  bottom = np.zeros(len(df_grupo_categoria['GRUPO'].unique()))

  # Redondear los valores de proporcion_aciertos a 2 decimales
  #f_grupo_categoria['proporcion_aciertos'] = df_grupo_categoria['proporcion_aciertos'].round(2)

  # Crear el gráfico de barras apilado
  #ig = px.bar(
  #   df_grupo_categoria,
  #   x='GRUPO',
  #   y='proporcion_aciertos',
  #   color='CATEGORIA',
  #   text='proporcion_aciertos',
  #   barmode='relative',
  #   title="Distribución de % correcto por grupo y categoría"
  #

  # Actualizar el diseño para etiquetas y título
  #ig.update_layout(
  #   xaxis_title="Grupo",
  #   yaxis_title="% Correctas"
  #

  # Normalizar los valores para que sumen 100% por cada grupo
  df_grupo_categoria['proporcion_aciertos'] = df_grupo_categoria.groupby('GRUPO')['proporcion_aciertos'].transform(lambda x: x / x.sum() * 100)
  # Redondear los valores de proporcion_aciertos a 2 decimales
  df_grupo_categoria['proporcion_aciertos'] = df_grupo_categoria['proporcion_aciertos'].round(2)
  # Crear el gráfico de barras 100% apilado
  fig = px.bar(
      df_grupo_categoria,
      x='GRUPO',
      y='proporcion_aciertos',
      color='CATEGORIA',
      text='proporcion_aciertos',
      barmode='relative',
      title="Distribución de % correcto por grupo y categoría" #(100% apilado)
  )

  # Actualizar el diseño para etiquetas y título
  fig.update_layout(
      xaxis_title="Grupo",
      yaxis_title="% Correctas"
  )

  # Mostrar el gráfico
  st.plotly_chart(fig)



##############################################################################################################
############################################## ANÁLISIS POR GRADO ##############################################
##################################################################################################################

def ANÁLISIS_POR_GRADO():
    """
    ...
    """

with tab_6:

  st.header("Descargar de resultados por grupo")

  # Crear selector de checkbox para elegir el si es un simulacro, ICFES o Olipiadas
  Prueba = st.radio("Seleccione la prueba de la cual desea obtener los resultados:", ["Simulacros o ICFES", "Olimpiadas"])

  col1, col2, col3 = st.columns(3)

  if Prueba == "Simulacros o ICFES":

    with col1:
       # Definir la columna por la que se desea agrupar
       columna_grupo = "SIMULACRO"

       # Obtener grupos únicos de la columna elegida
       grupos_unicos = datos[columna_grupo].unique()

        # Crear un selector de grupo con st.selectbox
       grupo_seleccionado = st.selectbox("Seleccione un simulacro o ICFES:", grupos_unicos)
       
    with col2:
        G_unicos = datos["Grupo"].unique()
        # Crear un selector de grupo con st.selectbox
        Eleccion = st.selectbox("Seleccione el grupo:", G_unicos)
    # Seleccionamos grupo
    datos_grupo_seleccionado = datos[(datos.SIMULACRO == grupo_seleccionado) &
                                     (datos.Grupo == Eleccion) &
                                     (datos['AÑO'] == año_seleccionado)
                                     ] 
    df_resultados_grupo = datos_grupo_seleccionado[["DOCUMENTO", "Nombre alumno", "Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]].copy()
    #############################################
    st.dataframe(df_resultados_grupo)

    # Crear archivo Excel en memoria
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
      df_resultados_grupo.to_excel(writer, sheet_name=f"Resultados_{Eleccion}", index=False)
      writer.close()

    output.seek(0)

    # Botón de descarga

    st.download_button(
      label="📥 Descargar resultados en Excel",
      data=output,
      file_name=f"Resultados_Grupo_{Eleccion}.xlsx",
      mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
  else:
     
  
      # Definir la columna por la que se desea agrupar
      columna_grupo = "GRUPO"  

      # Obtener grupos únicos de la columna elegida
      grupos_unicos = df_resultados[columna_grupo].unique()

      # Crear un selector de grupo con st.selectbox
      grupo_seleccionado = st.selectbox("Seleccione un grupo:", grupos_unicos)

      # Seleccionamos grupo
      datos_grupo_seleccionado = df_resultados[df_resultados.GRUPO == grupo_seleccionado]

      #############################################
      st.dataframe(datos_grupo_seleccionado)

      # Crear archivo Excel en memoria
      output = io.BytesIO()
      with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            datos_grupo_seleccionado.to_excel(writer, sheet_name="Datos_Grupo", index=False)
            writer.close()

      output.seek(0)

      # Botón de descarga
      st.download_button(
            label="📥 Descargar en Excel",
            data=output,
            file_name=f"Datos_{grupo_seleccionado}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )



  