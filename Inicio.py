import streamlit as st
import pandas as pd
import requests

# Configura el título y el favicon de la página
st.set_page_config(
    page_title="Gamer's Companion 🎮",
    page_icon="🎮",
)


def get_character_info(personaje):
    """
    Retorna la información de un juego ingresado por el usuario.
    
    Parámetros: 
    -game_name(str): nombre del juego del cual se quiere obtener información.

    -Retorna
    -str: Información del juego.
    -imagen: Imagen de la portada del juego.
    """
    
    url = f"https://gateway.marvel.com:443/v1/public/characters?name={personaje}&limit=5&apikey=44e41c4cde4c827c390345b6cb8e48b8"

    response = requests.get(url)

    if response.status_code == 200:
             data = response.json()
    
    character = data["data"]["results"][0]
    name = character["name"]
    description = character["description"]
    image_path = character["thumbnail"]["path"]
    image_url=image_path+".jgp"
    
    # Devuelve los datos del juego
    return name, description,image_url

# Crea una barra de búsqueda en Streamlit
character_name = st.text_input('Busca un personaje')

# Si se introduce un nombre de juego, busca la información del juego
if character_name:
    nombre,descripcion,url = get_character_info(character_name)
    
    # Muestra el nombre de la pelicula como título de la página
    st.title(nombre)

        # Crea dos columnas para mostrar la imagen y la información de la pelicula
    col1, col2 = st.columns(2)

        # Muestra la imagen de la pelicula en la columna de la izquierda
            
    col1.image(url, use_column_width=True)

        # Muestra la información de la pelicula en la columna de la derecha
    col2.markdown(f"**Descripcion del personaje:** {descripcion}")
        # Muestra el nombre del juego en el centro en la parte superior
        
