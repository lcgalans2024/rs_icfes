#import pandas as pd
#from pyuca import Collator
##################################################
# Grupo
#g = input("Cuál es el grupo: ")
#p = input("Número de periodo: ")
# en colab
df = pd.read_excel('/content/drive/MyDrive/Orestes/Planilla_Master_IEOS.xlsx',
              sheet_name= f"G{g}_P{p}"
              )
######################################################
# Eliminar espacios al principio y al final de los nombres de las columnas
df.columns = df.columns.str.strip()

df["Matricula"] = df.Matricula.astype(str)
# Eliminar espacios al inicio y al final de las columnas "Matricula" y "Nombre_estudiante"
df["Matricula"] = [x.strip() for x in df["Matricula"]]
######################################################
df.drop(df.columns[2:3], axis=1, inplace=True)
df.drop(df.columns[36:], axis=1, inplace=True)
#######################################################
# prompt: Obtener el indice de fila que contiene "Campo" en la columna Matricula
index_campo = df[df['Matricula'] == "Campo"].index[0]

# Crear un dataframe de la fila index_campo en adelante, donde los nombres de la columna sean los valores de la fila index_campo
df_Actividades = df.iloc[index_campo:, :2].copy()
df_Actividades.columns = df_Actividades.iloc[0]
df_Actividades = df_Actividades[1:]
df_Actividades.dropna(inplace=True)
df_Actividades['Campo'] = df_Actividades['Campo'].str.replace('_', '.')
# crear un diccionario con df_Actividades donde campo sea la clave
mi_diccionario1 = df_Actividades.set_index('Campo')['Nombre actividad'].to_dict()
#########################################################
# Seleccionamos solo las notas
df = df.iloc[:index_campo-2].copy()
######################################################
df1 = df[['Matricula', 'Nombre_estudiante'
         , '1.1', '1.2'
         , '1.3', '1.4'
         , '1.5', '1.6'
         , '1.7', '1.8'
         , '1.9', '1.10'
         , '1.11', '1.12'
         , '2.1', '2.2'
         , '2.3', '2.4'
         , '2.5', '2.6'
         , '2.7', '2.8'
         , '3.1', '3.2'
         ,'4.1', '4.2']].copy()
#####################################################
df1.fillna(1, inplace=True)
df1.replace(0,1,inplace=True)
#####################################################
# Lista de estudiantes con documento
df_estudiantes = pd.read_excel('/content/drive/MyDrive/Orestes/Listas_estudiantes_oreste.xlsx'
              ,sheet_name= g
              ,engine='openpyxl'
              )

df_estudiantes["ID"] = df_estudiantes.ID.astype(str)
df_estudiantes["MATRÍCULA"] = df_estudiantes.MATRÍCULA.astype(str)
df_estudiantes["DOCUMENTO"] = df_estudiantes.DOCUMENTO.astype(str)

# Creamos diccionario de documentos
#dict_DOC = pd.read_excel('/content/drive/MyDrive/Planeacion/Data/DICCIONARIOS.xlsx',sheet_name='DOCENTES_FACULTAD_PROGRAMA_UNIC')
dict_DOC_105 = df_estudiantes.set_index("MATRÍCULA")['DOCUMENTO'].to_dict()
## Agregamos columna de documento del docente
indice_columna = df1.columns.get_loc('Nombre_estudiante')
DOCUMENTO = df1.Matricula.map(dict_DOC_105)
df1.insert(indice_columna,'DOCUMENTO',DOCUMENTO)
# Lista de pares de columnas a comparar
columns_to_compare = [
    ('1.1', '1.2'),
    ('1.3', '1.4'),
    ('1.5', '1.6'),
    ('1.7', '1.8'),
    ('1.9', '1.10'),
    ('1.11', '1.12'),
    ('2.1', '2.2'),
    ('2.3', '2.4'),
    ('2.5', '2.6'),
    ('2.7', '2.8'),
    ##('3.1 ', '3.2 '),
    ('4.1', '4.2')
]

# Iterar a través de los pares de columnas y reemplazar los valores en col2 si col1 es mayor
for col1, col2 in columns_to_compare:
    #print(col1)
    #print(col2)
    #df1[col2] = df1.apply(lambda row: row[col1] if row[col1] >= 3.0 and row[col1] > row[col2] else row[col2], axis=1)
    # Aplicar la transformación solo a los valores de tipo string
    df1[col1] = df1[col1].apply(lambda x: float(x.replace(",", ".")) if isinstance(x, str) else x)
    df1[col2] = df1[col2].apply(lambda x: float(x.replace(",", ".")) if isinstance(x, str) else x)
    df1[col2] = df1.apply(lambda row: row[col1] if row[col1] > row[col2] else row[col2], axis=1)

# Calcular los promedios para cada par de columnas y agregar al DataFrame
for col1, col2 in columns_to_compare:
    new_col_name = f'{col1}_prom'
    df1[new_col_name] = df1[[col1, col2]].mean(axis=1)
#################################################################
df2 = df1[['Matricula'
           ,'DOCUMENTO'
           , 'Nombre_estudiante'
           , '1.1_prom'
           , '1.3_prom'
           , '1.5_prom'
           , '1.7_prom'
           , '1.9_prom'
           , '1.11_prom'
           , '2.1_prom'
           , '2.3_prom'
           , '2.5_prom'
           , '2.7_prom'
           #, '3.1 _prom'
           , '3.1', '3.2'
           , '4.1_prom'
           ]
           ].copy()

mi_diccionario2 = {
#  "1.1":"Taller de Pitágoras",
#  "1.3":"Taller resolución de triángulos",
#  "1.5":"Guía 1 de estadística",
#  "1.7":"Guía 2 de estadística",
#  "1.9":"Guía 3 de estadística",
#  "1.11":"Guía 4 de estadística",
  #"2.1":"Quiz Pitágoras",
  #"2.3":"Prueba Tipo Icfes",
  #"3.1 ":"Autoevaluación",
  #"3.2 ":"Heteroevaluación",
  #"4.1":"Prueba de periodo"
}

mi_diccionario = mi_diccionario1#{**mi_diccionario1, **mi_diccionario2}

dict_orden_act = {
  "1.1":1,
  "1.3":2,
  "1.5":3,
  "1.7":4,
  "1.9":5,
  "1.11":6,
  "2.1":7,
  "2.3":8,
  "2.5":9,
  "2.7":10,
  "3.1":11,
  "3.2":12,
  "4.1":13
}

df2.rename(columns={#'Nombre_estudiante ':'Nombre_estudiante'
                    '1.1_prom':'1.1'
                    ,'1.3_prom':'1.3'
                    ,'1.5_prom':'1.5'
                    ,'1.7_prom':'1.7'
                    ,'1.9_prom':'1.9'
                    ,'1.11_prom':'1.11'
                    ,'2.1_prom':'2.1'
                    ,'2.3_prom':'2.3'
                    ,'2.5_prom':'2.5'
                    ,'2.7_prom':'2.7'
                    #,'3.1_prom':'3.1'
                    ,'4.1_prom':'4.1'
                    }
                    , inplace= True
                    )
# Derretir la tabla
melted_df = pd.melt(df2, id_vars=['Matricula', 'DOCUMENTO', 'Nombre_estudiante'], var_name='Tarea', value_name='Calificación')
## Agregamos columna de documento del docente
indice_columna = melted_df.columns.get_loc('Calificación')
ACTIVIDAD = melted_df.Tarea.map(mi_diccionario)
################################################################
################################################################
#if ejecutar_hasta_aqui:#########################################
    # Detenemos la ejecución aquí###############################
#    raise SystemExit("Se ha detenido el código manualmente.")###
################################################################
################################################################
melted_df.insert(indice_columna,'ACTIVIDAD',ACTIVIDAD)

indice_columna = melted_df.columns.get_loc('Tarea')
ORDEN_ACT = melted_df.Tarea.map(dict_orden_act)
melted_df.insert(indice_columna,'ORDEN_ACT',ORDEN_ACT)

# prompt: Agregar columna llamada DIMENSION con las siguientes categorias: si tarea inicia con 1 C, si inicia con 2 P, si inicia con 3 ETICA, si inicia con 4 ESTETICA

def agregar_dimension(tarea):
  if tarea.startswith('1'):
    return 'HACER'
  elif tarea.startswith('2'):
    return 'SABER'
  elif tarea.startswith('3'):
    return 'AUTOEVALUACIÓN'
  elif tarea.startswith('4'):
    return 'PRUEBA_PERIODO'
  else:
    return None

melted_df['PROCESO'] = melted_df['Tarea'].apply(agregar_dimension)

# Crear un objeto Collator
collator = Collator()

# Primero, generamos la clave de ordenación en la columna 'Nombre_estudiante'
melted_df['Sort_Key'] = melted_df['Nombre_estudiante'].apply(collator.sort_key)

# prompt: agrupar por DIMENSION y por Nombre estudiante y ordenar por Nombre estudiante

grouped_df = melted_df.groupby(['PROCESO', 'Matricula', 'DOCUMENTO', 'Nombre_estudiante', 'ORDEN_ACT', 'Tarea', 'ACTIVIDAD','Sort_Key']).agg(
    Calificación=('Calificación', 'mean')
).sort_values(['Nombre_estudiante','ORDEN_ACT'])
#########################################################################
grouped_df.reset_index(inplace=True)

# Ordenar según la clave de ordenación y ORDEN_ACT
grouped_df = grouped_df.sort_values(['Sort_Key', 'ORDEN_ACT'])

# Finalmente, eliminamos la columna auxiliar 'Sort_Key'
grouped_df = grouped_df.drop(columns=['Sort_Key'])

grouped_df