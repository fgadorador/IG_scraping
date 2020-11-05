from selenium import webdriver
import time


class Steam_scraper:
    """ 
    Esta es una clase para raspar la página web de juegos steam. 
      
    Atributos: 
        path (str): directorio donde se situa el driver instalado. 
        explorer (str): navegador que se utiliza para el scraping.
    """
    def __init__(self, path, explorer):
        """ 
        Inicialización de la clase. 
  
        Input: 
            path (str): directorio donde se situa el driver instalado. 
            explorer (str): navegador que se utiliza para el scraping.
        """

        if explorer == 'firefox':
            self.driver = webdriver.Firefox(executable_path = path)

        if explorer == 'chrome':
            self.driver = webdriver.Chrome(path)
            
        self.url = "https://store.steampowered.com/"
        self.driver.get(self.url)

    def price(self,item):
        """ 
        Método para obtener el precio de un videojuego. 
        Input: 
            item (str): título del juego a consultar. 
          
        Returns: 
            price (str): precio del juego consultado en steam. 
        """
        
        searchbox = self.driver.find_element_by_id("store_nav_search_term")
        searchbox.send_keys(item)
        time.sleep(1) #necesita reposar para encontrar más info
        #caja donde se ve la imagen, título y precio del juego
        suggestion_box = self.driver.find_element_by_id("search_suggestion_contents")
        
        #hacemos try except para aquellos juegos que no se encuentren en steam o quizá estén mal escritos
        try:
            price = suggestion_box.find_element_by_class_name("match_price").text
            searchbox.clear()
        except:
            price = None
            searchbox.clear()

        
        return price
        

    def quit(self):
        """ 
        Método para cerrar el driver. 
        """
        self.driver.quit()