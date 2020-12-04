import csv
import os
import urllib
import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import inv
import plotly.express as px
import plotly
from tkinter import *
from tkinter import messagebox as MessageBox
#import geopandas as gpd

'''
#Ingresar al sitio y descargar el CSV con los datos de Colombia
url="https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD&bom=true&format=true"
response = requests.get(url)
with open(os.path.join("Archivo", "DataColombia.csv"), "wb") as f:
    f.write(response.content)

#Ingresar al sitio y descargar el CSV con los datos de Bogotá
url="https://datosabiertos.bogota.gov.co/dataset/44eacdb7-a535-45ed-be03-16dbbea6f6da/resource/b64ba3c4-9e41-41b8-b3fd-2da21d627558/download/osb_enftransm-covid26102020.csv"
response = requests.get(url)
with open(os.path.join("Archivo", "DataBogota.csv"), "wb") as f:
    f.write(response.content)
'''

#///////////////////COLOMBIA///////////////////////////////////////
#Abrir el CSV que se descargó de Colombia y obtener la información

data =pd.read_csv('Archivo/DataColombia.csv', parse_dates=[0], dayfirst=True)
data.head()
data.columns=['Fecha', 'ID', 'Fecha2', 'Código DIVIPOLA', 'Departamento', 'Código DIVIPOLA2', 'Ciudad','Edad','Unnidad', 'Sexo', 'Tipo', 'Ubicacion','Atencion', 'Código ISO del país','Nombre del país','Recuperado','Fecha de inicio de síntomas','Fecha de muerte','Fecha de diagnóstico','Fecha de recuperación','Tipo de recuperación','Pertenencia étnica','Nombre del grupo étnico']
d={'m':'M', 'f':'F','F':'F', 'M':'M'}
data['Sexo']=data['Sexo'].apply(lambda x:d[x])
#print(data['Fecha'])
data['Fecha']= pd.to_datetime(data['Fecha'])
#data['Fecha'] = data['Fecha'].apply(pd.to_datetime)
#data['Fecha']= data['Fecha'].apply(pd.to_datetime, format='%m/%d/%Y')

'''
#GRÁFICAS DE BARRAS

#fig0=plt.figure(figsize=(12,6))
#data['Fecha'].dt.month.value_counts().plot(kind='bar', alpha=0.5)
#plt.title('Número de Casos Totales en Colombia según el Número del Mes')
#plt.show()

fig1=plt.figure(figsize=(12,6))
data.Departamento.value_counts().plot(kind='bar', alpha=0.5)
plt.title('Número de Casos Totales según Departamento en Colombia')
plt.show()

fig=plt.figure(figsize=(12,6))
data.Sexo.value_counts().plot(kind='bar', alpha=0.5)
plt.title('Número de Casos totales en Colombia según el Sexo')
plt.show()

fig2=plt.figure(figsize=(12,6))
data.Recuperado[data.Recuperado == "Recuperado"].value_counts().plot(kind='bar', alpha=0.5)
plt.title('Número de Casos de Recuperados en Colombia')
plt.show()

fig3=plt.figure(figsize=(12,6))
data.Recuperado[data.Recuperado == "Fallecido"].value_counts().plot(kind='bar', alpha=0.5)
plt.title('Número de Casos de Fallecidos en Colombia')
plt.show()

#GRÁFICAS DE TORTAS

#fig1=plt.figure(figsize=(12,6))
#plt.pie(data['Fecha'].dt.month.value_counts(), autopct="%1.1f%%", shadow=True, radius= .9)
#plt.title('Porcentaje de Casos totales en Colombia según el Número del Mes', bbox={"facecolor":"0.8","pad":5})
#plt.legend( labels= data['Fecha'].dt.month.value_counts().index.unique()  , loc='upper right')
#plt.show()

fig1=plt.figure(figsize=(12,6))
plt.pie(data.Sexo.value_counts(), autopct="%1.1f%%", shadow=True, radius= .9)
plt.title('Porcentaje de Casos totales en Colombia según el Sexo', bbox={"facecolor":"0.8","pad":5})
plt.legend( labels= data.Sexo.value_counts().index.unique(), loc='upper right')
plt.show()

fig1=plt.figure(figsize=(12,6))
plt.pie(data.Recuperado[data.Recuperado != "fallecido"].value_counts(), autopct="%1.1f%%", shadow=True, radius= .999)
plt.title('Porcentaje de la situación de los contagiados en Colombia', bbox={"facecolor":"0.8","pad":5})
plt.legend( labels=data.Recuperado.value_counts().index.unique(), loc='upper right')
plt.show()

#//////////////////MAPA DE CALOR COLOMBIA//////////////////////////
repo_url = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json' #Archivo GeoJSON
mx_regions_geo = requests.get(repo_url).json()
extra=np.array(data.Departamento.value_counts())
casosDepartamentos=np.array([extra[1],extra[6],extra[0],extra[24],extra[17],extra[19],extra[21],extra[18],extra[9],extra[7],extra[3],extra[28],extra[12],extra[22],extra[25],extra[10],extra[11],extra[13],extra[23],extra[15],extra[4],extra[16],extra[14],extra[2],extra[29],extra[26],extra[27],extra[30],extra[33],extra[32],extra[34],extra[35],extra[31]])
nombresDepartamentos=np.array(["ANTIOQUIA", "ATLANTICO", "SANTAFE DE BOGOTA D.C", "BOLIVAR", "BOYACA", "CALDAS", "CAQUETA", "CAUCA", "CESAR", "CORDOBA", "CUNDINAMARCA", "CHOCO", "HUILA", "LA GUAJIRA", "MAGDALENA", "META", "NARIÑO", "NORTE DE SANTANDER", "QUINDIO", "RISARALDA", "SANTANDER", "SUCRE", "TOLIMA", "VALLE DEL CAUCA", "ARAUCA", "CASANARE", "PUTUMAYO", "AMAZONAS", "GUAINIA", "GUAVIARE", "VAUPES", "VICHADA", "ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA"])

fig = px.choropleth(data_frame=data,
                    geojson=mx_regions_geo,
                    locations=nombresDepartamentos, # nombre de la columna del Dataframe
                    featureidkey='properties.NOMBRE_DPT',  # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)

                    color=casosDepartamentos, #El color depende de las cantidades
                    color_continuous_scale="burg", #greens
                    #scope="north america"
                   )

fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")

fig.update_layout(
    title_text = 'Casos de infección en Colombia',
    font=dict(
        #family="Courier New, monospace",
        family="Ubuntu",
        size=18,
        color="#7f7f7f"
    )
)
plotly.offline.plot(fig)
'''
#///////////////////BOGOTÁ//////////////////////////////////////
#Abrir el CSV que se descargó de Bogotá y obtener la información

dato =pd.read_csv('Archivo/DataBogota.csv', delimiter=";", encoding='iso-8859-1',names=['Fecha_Sintomas', 'FechaDiagnostico', 'Ciudad', 'Localidad', 'Edad', 'Uni_Med', 'Sexo', 'Fuente_Contagio', 'Ubicacion', 'Estado'])
dato.head()
dato=dato.drop([0], axis=0) #Borrar la primera fila que tiene texto innecesario
dato.Edad=dato.Edad.astype(float) #Convertir la columna Edad a float
age_groups = pd.cut(dato.Edad, bins=[19, 40, 65, np.inf]) #Rangos de edad

'''
#GRÁFICAS DE BARRAS

fig=plt.figure(figsize=(12,6))
dato.Sexo[dato.Sexo != "SEXO"].value_counts().plot(kind='bar', alpha=0.5)
plt.title('Número de Casos totales en Bogotá según el Sexo')
plt.show()

fig2=plt.figure(figsize=(12,6))
dato.Estado[dato.Estado == "Recuperado"].value_counts().plot(kind='bar', alpha=0.5)
plt.title('Número de Casos de Recuperados en Bogotá')
plt.show()

fig3=plt.figure(figsize=(12,6))
dato.Estado[dato.Estado == "Fallecido"].value_counts().plot(kind='bar', alpha=0.5)
plt.title('Número de Casos de Fallecidos en Bogotá')
plt.show()

fig1=plt.figure(figsize=(12,6))
dato.Localidad[dato.Localidad != "Sin dato"].value_counts().plot(kind='bar', alpha=0.5)
plt.title('Número de Casos Totales según Localidad en Bogotá')
plt.show()

fig1=plt.figure(figsize=(12,6))
pd.crosstab(dato.Localidad[dato.Localidad != "Sin dato"], dato['Sexo']).plot(kind='bar', alpha=0.5)
plt.title('Número de Casos totales en Bogotá según el Sexo y la Localidad')
plt.show()

fig1=plt.figure(figsize=(12,6))
pd.crosstab(dato.Localidad[dato.Localidad != "Sin dato"], age_groups).plot(kind='bar', alpha=0.5)
plt.title('Número de Casos totales en Bogotá según el rango de edad y la Localidad')
plt.show()

#GRÁFICAS DE TORTAS
fig1=plt.figure(figsize=(12,6))
plt.pie(dato.Sexo[dato.Sexo != "SEXO"].value_counts(), autopct="%1.1f%%", shadow=True, radius= .9)
plt.title('Porcentaje de Casos totales en Bogotá según el Sexo', bbox={"facecolor":"0.8","pad":5})
plt.legend( labels= dato.Sexo.value_counts().index.unique(), loc='upper right')
plt.show()

fig1=plt.figure(figsize=(12,6))
plt.pie(dato.Estado[dato.Estado != "ESTADO"].value_counts(), autopct="%1.1f%%", shadow=True, radius= .999)
plt.title('Porcentaje de la situación de los contagiados en Bogotá', bbox={"facecolor":"0.8","pad":5})
plt.legend( labels=['%s, %1.1f%%' % (
        l, (float(s) / len(dato)) * 100) for l, s in zip(dato.Estado.value_counts().index.unique(), dato.Estado.value_counts())], loc='upper right')
plt.show()

#GRÁFICAS EXTRAS BOGOTÁ

fig1=plt.figure(figsize=(12,6))
dato.Localidad[dato.Localidad != "Sin dato"].value_counts().plot(kind='area', alpha=0.5)
plt.title('Número de Casos Totales según Localidad en Bogotá')
plt.show()

fig1=plt.figure(figsize=(12,6))
pd.crosstab(dato.Localidad[dato.Localidad != "Sin dato"], dato['Sexo']).plot(kind='area', alpha=0.5)
plt.title('Número de Casos totales en Bogotá según el Sexo y la Localidad')
plt.show()

fig1=plt.figure(figsize=(12,6))
pd.crosstab(dato.Localidad[dato.Localidad != "Sin dato"], age_groups).plot(kind='area', alpha=0.5)
plt.title('Número de Casos totales en Bogotá según el rango de edad y la Localidad')
plt.show()

#//////////////////MAPA DE CALOR BOGOTÁ//////////////////////////
repo_url2 = 'https://raw.githubusercontent.com/JessicaParrado/Localidades/main/bogota_localidades.geojson' #Archivo GeoJSON
bo_regions_geo = requests.get(repo_url2).json()
extra2=np.array(dato['Localidad'].value_counts())
casosLocalidades=np.array([extra2[4], extra2[1], extra2[7], extra2[0], extra2[11], extra2[18], extra2[16], extra2[14], extra2[9], extra2[2], extra2[20], extra2[13], extra2[5], extra2[15], 1345, extra2[8], extra2[6], extra2[12], extra2[3], extra2[10]])
nombresLocalidades=np.array(["CIUDAD BOLIVAR","SUBA", "RAFAEL URIBE URIBE", "KENNEDY", "USME", "LOS MARTIRES", "SANTA FE", "BARRIOS UNIDOS", "FONTIBON", "ENGATIVA", "CANDELARIA", "CHAPINERO", "ANTONIO", "TEUSAQUILLO", "SUMAPAZ", "SAN CRISTOBAL", "USAQUEN", "TUNJUELITO", "BOSA", "PUENTE ARANDA"])

fig = px.choropleth(data_frame=dato,
                    geojson=bo_regions_geo,
                    locations=nombresLocalidades, # nombre de la columna del Dataframe
                    featureidkey='properties.NOMBRE',  # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)

                    color=casosLocalidades, #El color depende de las cantidades
                    color_continuous_scale="Teal", #greens
                    #scope="north america"
                   )

fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")

fig.update_layout(
    title_text = 'Casos de infección en Bogotá',
    font=dict(
        #family="Courier New, monospace",
        family="Ubuntu",
        size=18,
        color="#7f7f7f"
    )
)
plotly.offline.plot(fig)

'''
#///////////////////////////////////////REGRESIÓN DE DATOS//////////////////////////////////////////////////////

#print(data.Fecha[data.Fecha.dt.month != 12.0].dt.month.value_counts())
#Graficar la información que se tiene como puntos
plt.scatter(data.Fecha[data.Fecha.dt.month != 12.0].dt.month.value_counts().index.unique(),data.Fecha[data.Fecha.dt.month != 12.0].dt.month.value_counts());
plt.xlabel('Meses');
plt.ylabel('Número de Casos')
plt.show()
#Crear el modelo
X=np.array([np.ones(len(data.Fecha[data.Fecha.dt.month != 12.0].dt.month.value_counts().index.unique())),data.Fecha[data.Fecha.dt.month != 12.0].dt.month.value_counts().index.unique()]).T
a= inv(X.T @ X ) @X.T @ data.Fecha[data.Fecha.dt.month != 12.0].dt.month.value_counts() #Fórmula Proyección

#Hacer la prediccción
x_predict=np.linspace(3,11,num=100) #Generará números del 3 al 11
subs_predict=a[0]+a[1]*x_predict #Fórmula de la recta
#Graficamos los puntos y la recta en la misma figura,
plt.scatter(data.Fecha[data.Fecha.dt.month != 12.0].dt.month.value_counts().index.unique(),data.Fecha[data.Fecha.dt.month != 12.0].dt.month.value_counts());
plt.xlabel('Meses');
plt.ylabel('Número de Casos')
plt.plot(x_predict, subs_predict,'c') #Minimiza la distancia entre los puntos
plt.show()


#Para saber número de casos al finalizar Diciembre(Mes 1 de proyección)
y= a[1]*(12)+a[0] #Fórmula de la recta, donde a[1] es la pendiente, se varia el valor de x para saber la proyección
y1=f"{y:.1f}"
#print('Al final de Diciembre del 2020, se tendrán aproximadamente '+str(y1)+' casos en Colombia')
MessageBox.showinfo("Proyección Mes 1", 'Teniendo en cuenta los resultados de los meses anteriores, se proyecta que al final de Diciembre del 2020, se tendrán aproximadamente '+str(y1)+' casos en Colombia')

#Para saber número de casos al finalizar Enero(Mes 2 de proyección)
y= a[1]*(13)+a[0] #Fórmula de la recta, donde a[1] es la pendiente, se varia el valor de x para saber la proyección
y1=f"{y:.1f}"
#print('Al final de Enero del 2021, se tendrán aproximadamente '+str(y1)+' casos en Colombia')
MessageBox.showinfo("Proyección Mes 2", 'Teniendo en cuenta los resultados de los meses anteriores, se proyecta que al final de Enero del 2021, se tendrán aproximadamente '+str(y1)+' casos en Colombia')

#Para saber número de casos al finalizar Febrero(Mes 3 de proyección)
y= a[1]*(14)+a[0] #Fórmula de la recta, donde a[1] es la pendiente, se varia el valor de x para saber la proyección
y1=f"{y:.1f}"
#print('Al final de Febrero del 2021, se tendrán aproximadamente '+str(y1)+' casos en Colombia')
MessageBox.showinfo("Proyección Mes 3", 'Teniendo en cuenta los resultados de los meses anteriores, se proyecta que al final de Febrero del 2021, se tendrán aproximadamente '+str(y1)+' casos en Colombia')

