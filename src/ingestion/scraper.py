import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)

class BookScrapper:
    """
    clase para extraer libros de http://books.toscrape.com
    5 paginas por defecto a modo de prueba
    """
    BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

    def __init__(self, max_pages: int = 1):
        self.max_pages = max_pages        #atributo de la clase
        self.session = requests.Session() #atributo de la clase

        logging.info(f"initialized BookScrapper with max_pages={self.max_pages}")

    def fetch_page(self, page_number: int): #metodo de la clase
        """
        metodo para obtener el contenido HTML de una pagina dada
        """
        try:    
            url = self.BASE_URL.format(page_number)
            response = self.session.get(url)
            response.raise_for_status()

            logging.info(f"fetched page {page_number}")

            return response.text
        
        except requests.RequestException as e:
            logging.error(f"error fetching page {page_number}: {e}")
            return None

# prueba de la clase
if __name__ == "__main__":

    my_scraper = BookScrapper(max_pages=1) #objeto o instancia de la clase
    html = my_scraper.fetch_page(1)
    if html:
        print(html[:500])
    else:
        print("failed to fetch page")

