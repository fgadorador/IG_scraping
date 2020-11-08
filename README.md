# IG_scraping
Este proyecto consiste en la obtención de información, mediante web scraping, sobre videojuegos en la página web Instant-Gaming (https://www.instant-gaming.com/), para posteriormente compararlos con los precios en Steam (https://store.steampowered.com/) utilizando selenium.

## Autores
- Amanda Iglesias Moreno
- Fernando García Dorador

## Descripción de ficheros
En la carpeta **Scripts** se en cuenta el código del proyecto, que consta de 3 ficheros:
- **selenium_steam.py**: aquí está la clase *Steam_scraper* que utiliza selenium para consultar los precios de los juegos en steam.
- **scraper.py**: en este script se desarrolla todo el código creando la clase *Ig_scraper*, que obtiene la información de los videojuegos utilizando la clase *Steam_scraper* en el proceso y escribe los datos en un archivo csv con el nombre **IG_data_YYYY-MM-DD.csv**. También se ha definido un método para obtener la imagen de fondo si se desea.
- **main.py**: este script llama a la clase *Ig_scraper* especificando el path donde tenemos el webdriver instalado y el navegador que utilizamos. El argumento *record_images* está definido por defecto como *False*, si los especificamos como *True*, se crearía una carpeta **imagenes** donde se guardarían las portadas de los videojuegos con su id.

Fuera de la carpeta tenemos los siguientes ficheros:
- **Práctica_1_web_scraping.pdf**: este documento contiene las respuestas a las preguntas que se plantean el la práctica 1 de la asignatura.
- **IG_data_YYYY-MM-DD.csv**: este es el dataset generado en el día especificado. Contiene los siguientes campos: 'id','title', 'price_ig', 'discount', 'price_retail', 'price_steam', 'region', 'DLC', 'platform', 'link', 'availability', 'genre', 'languages', 'release_date', 'user_rating', 'number_comments', 'review' y 'rating_review'.
- **background.jpg**: imágen de fondo de la página Instant-Gaming.

## Publicación del dataset
Fernando García Dorador & Amanda Iglesias Moreno. (2020). Videogame data from Instant-Gaming [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4263349
