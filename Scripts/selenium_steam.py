from selenium import webdriver
import time


class Steam_scraper:

    def __init__(self, path, explorer):

        if explorer == 'firefox':
            self.driver = webdriver.Firefox(executable_path = path)

        if explorer == 'chrome':
            self.driver = webdriver.Chrome(path)
            
        self.url = "https://store.steampowered.com/"
        self.driver.get(self.url)

    def price(self,item):
        
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
        
        self.driver.quit()