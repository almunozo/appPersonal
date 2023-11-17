import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
import requests
import matplotlib.pyplot as plt      

def consultaApi(country_name):
    url = f'https://restcountries.com/v3.1/translation/{country_name}'

# Realiza la solicitud a la API
    response = requests.get(url)

# Verifica si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
    # Convierte la respuesta a formato JSON
        data = response.json()
    
        nombre = data[0]["name"]["official"]
        capital = data[0]["capital"][0]
        continente= data[0]["continents"][0]
        latitud_longitud= data[0]["latlng"]
        territorio= data[0]["area"]
        poblacion=data[0]["population"] # Recordar KM2
        url_bandera = data[0]["flags"]["png"]
        descripcion_bandera= data[0]["flags"]["alt"] # Recordar hacer un else
        escudo=data[0]["coatOfArms"]["png"]
        url=data[0]["maps"]["googleMaps"]
        nombre_comun=data[0]["name"]["common"]
    else:
        print(f'Error al consultar la API. Código de estado: {response.status_code}')
    
    return capital, continente,latitud_longitud,territorio,poblacion, url_bandera, descripcion_bandera,escudo,url,nombre_comun

def obtener_expectativa_vida(nombre_pais, dataframe):
    """
    Función que toma un nombre de país y un DataFrame como entrada,
    y devuelve la expectativa de vida correspondiente al país dado.
    """
    try:
        # Filtra el DataFrame para obtener la fila correspondiente al país
        fila_pais = dataframe[dataframe['country'] == nombre_pais]
        
        # Extrae el valor de la columna 'Life expectancy' de esa fila
        expectativa_vida = fila_pais['Individuals using the Internet (per 100 inhabitants)'].values[0]
        
        return expectativa_vida
    except IndexError:
        # Manejar el caso en el que el país no se encuentre en el DataFrame
        return f"No se encontró información para {nombre_pais}"
st.title("Buscador de informacion de paises")
# Barra de búsqueda
busqueda = st.text_input("Buscar país:", "")

# Mostrar resultados
if busqueda:
    capital, continente,latitud_longitud,territorio,poblacion, url_bandera, descripcion_bandera,escudo,url,nombre_comun=consultaApi(busqueda)
    # Diseño de la página
    st.title(f"Información ")

# Crear contenedores para organizar el diseño
    container1 = st.container()
    container2 = st.container()

# Estilo para resaltar información importante
    highlight_style = "color: #006400; font-weight: bold;"

# Contenedor 1: Información detallada
    with container1:
        col1, col2 = st.columns(2)
        col1.markdown(f"**Nombre oficial:** {nombre_comun}")
        col1.markdown(f"**Capital:** {capital}")
        col1.markdown(f"**Continente:** {continente}")
        col1.markdown(f"**Coordenadas:** {latitud_longitud[0]}, {latitud_longitud[1]}")
        col1.markdown(f"**Extension de territorio:** {territorio} km²")
        col1.markdown(f"**Población:** {poblacion}")
        col1.markdown(f"**Link de Google Maps:** {url}")
        col2.image(url_bandera, caption=f"Bandera de {nombre_comun}", use_column_width=True)
        col2.image(escudo, caption=f"Escudo de {nombre_comun}", use_column_width=True)

# Contenedor 2: Imágenes
    with container2:
        st.markdown(f"<p style='{highlight_style}'>Descripción de la Bandera: {descripcion_bandera}</p>", unsafe_allow_html=True)

else:
    st.warning("No se encontraron resultados.")

import numpy as np

st.title("Comparar paises")

# Operaciones matemáticas básicas
pais1 = st.text_input("Ingrese el nombre del pais 1")
pais2 = st.text_input("Ingrese el nombre del pais 2")

operation = st.selectbox("Selecciona el item a comparar", ["Extension de territorio", "Poblacion"])

result = ""

if pais1 and pais2:  # Verifica que ambos países estén ingresados
    capital1, continente1, latitud_longitud1, territorio1, poblacion1, url_bandera1, descripcion_bandera1, escudo, url1, nombre_comun1 = consultaApi(pais1)
    capital2, continente2, latitud_longitud2, territorio2, poblacion2, url_bandera2, descripcion_bandera2, escudo, url2, nombre_comun2 = consultaApi(pais2)
    nueva_data = {
        'Country': [nombre_comun1, nombre_comun2],
        'Population': [poblacion1, poblacion2],
        'Area': [territorio1, territorio2]
    }

    df = pd.DataFrame(nueva_data)

    if operation == "Extension de territorio":
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"{nombre_comun1}")
        col1.image(url_bandera1, use_column_width=True)
        col2.image("https://static.vecteezy.com/system/resources/previews/008/891/548/non_2x/inspiring-logo-designs-from-vs-or-versus-letters-free-vector.jpg",use_column_width=True)
        col3.markdown(f"{nombre_comun2}")
        col3.image(url_bandera2, use_column_width=True)
        if np.subtract(territorio1,territorio2)>0:
            result=f"{nombre_comun1} tiene un territorio mas extenso que {nombre_comun2} con {territorio1} Km2 y {territorio2} Km2 respectivamente."
        else:
            result=f"{nombre_comun2} tiene un territorio mas extenso que {nombre_comun1} con {territorio2} Km2 y {territorio1} Km2 respectivamente."

    elif operation == "Poblacion":
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"{nombre_comun1}")
        col1.image(url_bandera1, use_column_width=True)
        col2.image("https://static.vecteezy.com/system/resources/previews/008/891/548/non_2x/inspiring-logo-designs-from-vs-or-versus-letters-free-vector.jpg",use_column_width=True)
        col3.markdown(f"{nombre_comun2}")
        col3.image(url_bandera2, use_column_width=True)
        if np.subtract(poblacion1,poblacion2)>0:
            result=f"{nombre_comun1} tiene una poblacion mas grande que {nombre_comun2} con {poblacion1} habitantes y {poblacion2} habitantes respectivamente."
        else:
            result=f"{nombre_comun2} tiene una poblacion mas grande que {nombre_comun1} con {poblacion2} habitantes y {poblacion1} habitantes respectivamente."

    st.write(f"{result}")


# Ordenar el DataFrame por población para un gráfico más claro
    df = pd.DataFrame(nueva_data)

# Ordenar el DataFrame por población para un gráfico más claro
    df = df.sort_values(by='Population', ascending=False)

# Crear un gráfico de barras comparando población y área
    fig, ax1 = plt.subplots()

# Barras para la población
    ax1.bar(df['Country'], df['Population'], color='b', alpha=0.7, label='Población')
    ax1.set_xlabel('País')
    ax1.set_ylabel('Población', color='b')
    ax1.tick_params('y', colors='b')

# Crear un segundo eje y para el área
    ax2 = ax1.twinx()
    ax2.plot(df['Country'], df['Area'], color='r', marker='o', label='Área')
    ax2.set_ylabel('Área (km²)', color='r')
    ax2.tick_params('y', colors='r')

# Añadir leyendas y título
    plt.title('Comparación de Población y Área por País')
    fig.tight_layout()

# Mostrar el gráfico en Streamlit
    st.pyplot(fig)
else:
    st.warning("Ingrese ambos países para realizar la comparación.")

