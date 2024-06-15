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

##############################################################################################################
#Cargamos los datos
datos = pd.read_excel("Resultados_Simulacro_ICFES.xlsx")

for col in datos.select_dtypes(include=np.float64):
    datos[col] = datos[col].round(2)
datos.head()

datos["Grupo"] = datos["Grupo"].astype(str)
datos["Matemáticas"] = datos["Matemáticas"].astype(int)
##############################################################################################################

st.title("ANÁLISIS RESULTADOS SIMULACROS ICFES")

tableros = ["Análisis Puntaje Global", "Análisis Por Area", "Análisis Por Grupo", "Análisis Por Año"]

tab_1, tab_2, tab_3, tab_4 = st.tabs(tableros)

##############################################################################################################
########################################## ANÁLISIS PUNTAJE GLOBAL ###########################################
##############################################################################################################

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
  datos_s1 = datos[datos["SIMULACRO"] == "S1"]
  datos_s2 = datos[datos["SIMULACRO"] == "S2"]
###########################################################################################

# Calcular metricas simulacro 1
  promedio_general_s1 = round(datos_s1['Puntaje global'].mean(),2)
  maximo_s1 = max(datos_s1['Puntaje global'])
  minimo_s1 = min(datos_s1['Puntaje global'])

# Calcular metricas simulacro 2
  promedio_general_s2 = round(datos_s2['Puntaje global'].mean(),2)
  maximo_s2 = max(datos_s2['Puntaje global'])
  minimo_s2 = min(datos_s2['Puntaje global'])

# Mostrar tarjetas con las métricas
  col1, col2, col3 = st.columns(3)
  with col1:
    st.metric(label="Promedio puntaje global simulacro 1", value=promedio_general_s1)
    st.metric(label="Promedio puntaje global simulacro 2", value=promedio_general_s2)
  with col2:
    st.metric(label="Máximo puntaje global simulacro 1", value=maximo_s1)
    st.metric(label="Máximo puntaje global simulacro 2", value=maximo_s2)
  with col3:
    st.metric(label="Mínimo puntaje global simulacro 1", value=minimo_s1)
    st.metric(label="Mínimo puntaje global simulacro 2", value=minimo_s2)
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
  top_ten_s1 = datos_s1[["Grupo","Nombre alumno","Puntaje global"]].nlargest(10, 'Puntaje global')
  top_ten_s2 = datos_s2[["Grupo","Nombre alumno","Puntaje global"]].nlargest(10, 'Puntaje global')

  st.subheader("Top Ten Puntajes Globales")

  col1, col2= st.columns(2)
  with col1:
    st.subheader("Primer Simulacro")
    st.dataframe(top_ten_s1)
  with col2:
    st.subheader("Segundo Simulacro")
    st.dataframe(top_ten_s2)
  #with col3:
  #  minimo = metricas_grupo_area['minimo_area']
  #  st.metric(label="Mínimo", value=minimo)

##############################################################################################################
############################################# ANÁLISI POR AREA ###############################################
##############################################################################################################

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
  datos_area_s1 = obtener_datos_por_area_simulacro(area_seleccionado,"S1")
  datos_area_s2 = obtener_datos_por_area_simulacro(area_seleccionado,"S2")

  # Calcular métricas para el área actual
  metricas_area_s1 = calcular_metricas_por_area(datos_area_s1,area_seleccionado)
  metricas_area_s2 = calcular_metricas_por_area(datos_area_s2,area_seleccionado)
  # Generar tabla HTML con las métricas
  #tabla_metricas_html = generar_tabla_metricas(metricas_area)

  # Mostrar tarjetas con las métricas
  col1, col2, col3 = st.columns(3)
  with col1:
   st.metric(label="Promedio global simulacro 1", value=metricas_area_s1['Promedio'].round(2))
   st.metric(label="Promedio global simulacro 2", value=metricas_area_s2['Promedio'].round(2))
  with col2:
   st.metric(label="Máximo simulacro 1", value=metricas_area_s1['maximo_area'])
   st.metric(label="Máximo simulacro 2", value=metricas_area_s2['maximo_area'])
  with col3:
   st.metric(label="Mínimo simulacro 1", value= metricas_area_s1['minimo_area'])
   st.metric(label="Mínimo simulacro 2", value= metricas_area_s2['minimo_area'])
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
  top_ten_area_s1 = datos_area_s1[["Grupo","Nombre alumno",area_seleccionado]].nlargest(10, area_seleccionado)
  top_ten_area_s2 = datos_area_s2[["Grupo","Nombre alumno",area_seleccionado]].nlargest(10, area_seleccionado)

  st.subheader(f"Top Ten {area_seleccionado}")

  col1, col2= st.columns(2)
  with col1:
    st.subheader("Primer Simulacro")
    st.dataframe(top_ten_area_s1)
  with col2:
    st.subheader("Segundo Simulacro")
    st.dataframe(top_ten_area_s2)

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  st.plotly_chart(px.histogram(datos_area_s1, x=area_seleccionado, text_auto=True))
  st.plotly_chart(px.box(datos_area_s1, x=area_seleccionado))

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

##############################################################################################################
############################################# ANÁLISI POR GRUPO ##############################################
##############################################################################################################

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
       st.metric(label="Promedio", value=promedio)
     with col2:
       maximo = metricas_grupo_area['maximo_area']
       st.metric(label="Máximo", value=maximo)
     with col3:
       minimo = metricas_grupo_area['minimo_area']
       st.metric(label="Mínimo", value=minimo)
     style_metric_cards(border_color="#3A74E7")
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  # Mostrar histogramas y boxplots (opcional)
  st.plotly_chart(px.histogram(datos_grupo, x="Matemáticas"))
  st.plotly_chart(px.box(datos_grupo, x="Matemáticas"))
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

##############################################################################################################
############################################## ANÁLISIS POR AÑO ##############################################
##############################################################################################################
 
with tab_4:

  st.header("En construcción...")
  #st.title("Resumen general - Simulacro ICFES")