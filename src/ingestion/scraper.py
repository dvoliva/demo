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
        self.max_pages = max_pages
        self.session = requests.Session()

        logging.info(f"initialized BookScrapper with max_pages={self.max_pages}")

if __name__ == "__main__":
    my_scraper = BookScrapper(max_pages=5)
    print(f"configured pages: {my_scraper.max_pages}")

