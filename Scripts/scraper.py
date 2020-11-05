from bs4 import BeautifulSoup
import requests
import csv
import re
import datetime
import os
from selenium import webdriver
from selenium_steam import Steam_scraper



class Ig_scraper:
    """ 
    Esta es una clase para raspar la página web de juegos ig. 
      
    Atributos: 
        base_link (str): Link base del sitio web. 
        page_link_initial (str): Link de la página a partir de la cual realizaremos el raspado.
        record_images (bool): Boolean que determina si se guardan o no las imagenes (por defecto False).
    """
    
    def __init__(self, record_images=False):
        """ 
        Inicialización de la clase. 
  
        Input: 
            base_link (str): Link base del sitio web. 
            page_link_initial (str): Link de la página a partir de la cual realizaremos el raspado.
            record_images (bool): Boolean que determina si se guardan o no las imagenes (por defecto False).
        """
            
        self.base_link = 'https://www.instant-gaming.com'
        self.page_link_initial = '/en/search/?all_types=1&all_cats=1&min_price=0&max_price=100&noprice=1&min_discount=0&max_discount=100&min_reviewsavg=10&max_reviewsavg=100&noreviews=1&available_in=ES&gametype=all&sort_by=&query=&page=1'
        self.record_images = record_images
        
    
    def download_html(self, url):
        """ 
        Funcion para descargar el codigo html de una url. 
        Input: 
            url (str): Link base del sitio web. 
          
        Returns: 
            html (str): código html de la página web. 
        """
    
        html = None
        response = requests.get(url)

        # response se evaluara como True si tiene un status code entre 200 y 400 (particularidad de la libreria request)
        if response:
            html = response.content
        else:
            print('ha ocurrido un error al realizar la peticion de la pagina' + url)

        return html

    def background_image(self):
        """ 
        Descarga la imagen de la página inicial de raspado. 
          
        Returns: 
            No retorna nada pero guardara la imagen en el directorio actual de trabajo. 
        """
        url = self.base_link + self.page_link_initial
        html = self.download_html(url)
        soup = BeautifulSoup(html)

        # get url of the background image
        background_url = re.findall('http.*?jpg', soup.find('div', {"id": "backgroundLink"})['style'])[0]
        background_imagen = self.download_html(background_url)

        # guardar la imagen en el directorio de trabajo actual 
        with open('background.jpg', 'wb') as f:
            f.write(background_imagen)
    
    def scraper(self, path, explorer):
        """ 
        Raspado de la página web. 
          
        Returns: 
            No retorna nada pero se creará un documento csv en el directorio actual con los datos raspados. 
        """
    
        # scraper selenium
        sc = Steam_scraper(path, explorer)

        # crear un archivo csv en modo escritura (denominar el archivo de acuerdo a la fecha de raspado web) 
        date_scrape = datetime.datetime.now().date() 
        file_name = 'IG_data_' + str(date_scrape) + '.csv'
        csv_file = open(file_name, 'w', encoding="utf-8")

        # escribir en primera fila del archivo csv el nombre de las columnas
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['id','title', 'price_ig', 'discount', 'price_retail', 'price_steam', 'region', 'DLC', 'platform', 'link', 'availability', 
                         'genre', 'languages', 'release_date', 'user_rating', 'number_comments', 'review', 'rating_review'])

        # crear una carpeta llamada imagenes (si esta no existe) para almacenar las portadas de los juegos
        if self.record_images:
            folder_name = 'imagenes'
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)

        # inicializar numero_id
        numero_id = 1
        num_paginas = 1

        # accedemos a la siguiente página
        url = self.base_link + self.page_link_initial
        html = self.download_html(url)
        
        # realizaremos webscraping hasta que no haya más páginas en ese caso romperemos el while loop 
        while True:
            soup = BeautifulSoup(html, features='lxml')


            #en la pag principal hay 4 mejores juegos y los demas son item mainsadow. En todas las demás paginas,
            #los item deberian ser normales        
            best_items = soup.find_all('div', class_='category-best item mainshadow')
            normal_items = soup.find_all('div', class_='item mainshadow')
            items = best_items + normal_items

            # mensajes al usuario para conocer el progreso del raspado
            print('Raspando página {}'.format(num_paginas))

            for item in items:

                # TITLE 
                titulo = item.find('div', class_='name').text

                # SAVE IMAGE
                if self.record_images:
                    imagen_url = item.find('img', class_='picture mainshadow').get('src')
                    imagen_html = self.download_html(imagen_url)
                    # el titulo de la imagen guardada sera su id_number
                    with open(folder_name + '/' + str(numero_id) +'.jpg', 'wb') as f:
                        f.write(imagen_html)


                # PRICE_IG
                # obtener precio del juego - se extrae únicamente el dato numérico (sin caracteres especiales o símbolo del euro)
                try:
                    precio = re.findall("\d+\.?\d*", item.find('div', class_='price').text)[0]
                except IndexError:
                    precio = ''

                # PRICE_STEAM
                # si el precio es un valor numerico (termina con el signo del euro) - eliminamos el simbolo y lo guardamos en el mismo
                # formato que el precio anterior (utilizando el punto como separador decimal)
                precio_steam = sc.price(titulo) #llamamos a la función del otro script
                if precio_steam:
                    if precio_steam.endswith('€'):
                        precio_steam = precio_steam.replace(',','.')[:-1]

                # DISCOUNT
                try:
                    descuento = item.find('div', class_='discount').text
                except AttributeError:
                    descuento = None

                region = item['data-region']
                dlc = item['data-dlc']
                link = item.a['href']

                #Existen algunos links que provocan muchos redirects y no puede hacer la request
                #Por eso hago que vaya al siguiente item del loop escribiendo la info de la pag principal unicamente
                try:

                    html2 = self.download_html(link)

                except:
                    plataforma = None
                    numero_id = numero_id + 1
                    precio_retail = None
                    dispo = None
                    generos = None
                    idiomas = None
                    rating = None
                    numero_comentarios = None
                    release_date = None
                    comment = None
                    comment_rating = None
                    csv_writer.writerow([numero_id, titulo, precio, descuento, precio_retail, precio_steam, region, dlc, 
                                     plataforma, link, dispo, generos, idiomas, release_date, rating, numero_comentarios, comment, comment_rating])
                    continue

                soup2 = BeautifulSoup(html2, features='lxml')

                ### RETAIL PRICE ###
                try:
                    precio_retail = re.findall("\d+\.?\d*", soup2.find('div', class_='retail').span.text)[0] 
                except (IndexError, AttributeError):
                    precio_retail = None


                subinfo = soup2.find('div', class_='subinfos')

                plataforma = subinfo.a.text

                ### DISPONIBILIDAD ###
                # dos nombres posibles download o preorder
                # .strip() eliminar espacios al principio y al final de la string
                dispo = subinfo.find('div', class_=['download', 'preorder']).text.strip()

                ### GENEROS ###
                try:
                    tags = soup2.find('div', class_='tags').text
                    generos = tags.strip().replace('\n', ' ')
                except AttributeError:
                    generos = None

                pestañas = soup2.find('div', class_='tabs')

                ### IDIOMAS DISPONIBLES ###
                try:
                    if 'Multi' in soup2.find('div', class_='languages').text:
                        idiomas = 'Multi'
                    else:
                        image_tags = soup2.find('div', class_='languages').find_all('img')
                        # extraer el texto alternativo de cada imagen - primero crear una lista con los elementos 
                        # y posteriormente unirlos todos en una string
                        idiomas_list = [image_tag['alt'] for image_tag in image_tags]
                        idiomas = ' '.join(idiomas_list)            
                except AttributeError: 
                    idiomas = None


                ### RATING ###
                try:
                    rating = pestañas.find('a', class_='tab mainshadow productreviews').span.text

                    # algunos productos no tiene rating porque los usuarios aun no han puntuado 
                    # en este caso el rating se especifica con un ?
                    if rating == '?':
                        rating = None
                # otro productos no tiene rating porque no hay opcion de puntuarlos - por ejemplo tarjetas de regalo    
                except AttributeError:
                    rating = None

                ### NUMERO DE COMENTARIOS ###
                try: 
                    numero_comentarios = re.findall(r'\d+', soup2.find('a', class_="tab mainshadow feedbacks").h2.text)[0]            
                except (IndexError, AttributeError):
                    numero_comentarios = None


                ### RELEASE DATE ###
                release_date = soup2.find('div', class_='release').span.text

                ### COMENTARIO DESTACADO DE LA PAGINA ###
                ### en el comentario remplazamos comas por espacios para evitar problemas al leer el archivo .csv
                ### ademas de eliminar new line and return elements
                try:
                    comment = soup2.find('p', itemprop='reviewBody').text.replace(',',' ').replace('\r', '').replace('\n', '')
                except Exception as e:
                    comment = None

                ### NOTA COMENTARIO DESTACADO ###
                try:    
                    comment_rating = soup2.find('span', itemprop='ratingValue').text
                except Exception as e:
                    comment_rating = None

                # escritura de los datos en el archivo .csv
                csv_writer.writerow([numero_id, titulo, precio, descuento, precio_retail, precio_steam, region, dlc, 
                                     plataforma, link, dispo, generos, idiomas, release_date, rating, numero_comentarios, comment, comment_rating])

                numero_id = numero_id + 1

            # buscar en el último boton un anchor tag asociado 
            last_element = soup.find(class_='pagination bottom').find_all('li')[-1].find('a')

            # si existe el anchor tag entonces obtendremos la página web y accederemos a ella
            # si el último elemento no tiene anchor tag significa que no hay más páginas y terminaremos el scraping 
            if last_element:
                page_link = last_element['href']
                num_paginas += 1
                url = self.base_link + page_link
                html = self.download_html(url)
                print('Siguiente página') 

            else:
                print('No hay más páginas. Fin del scraping')
                break   

        csv_file.close()
        sc.quit()