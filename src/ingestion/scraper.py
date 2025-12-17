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
    
    def _clean_price(self, price_str: str) -> float:
        if not price_str:
            return 0.0
        return float(price_str.replace("£", ""))    

    def _get_rating(self, article: str) -> int:
        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }
        star_element = article.find("p", class_="star-rating")
        rating_text = star_element["class"][1]
        return rating_map.get(rating_text, 0)

    def parse_books(self, html_content: str):
        soup = BeautifulSoup(html_content, "html.parser")
        books_data = []
        book_articles = soup.find_all("article", class_="product_pod")
        for article in book_articles:
            try:
                title = article.h3.a["title"]
                price_text = article.find("p", class_="price_color").text
                availability = article.find("p", class_="instock availability").text.strip()

                book = {
                    "title": title,
                    "price": self._clean_price(price_text),
                    "rating": self._get_rating(article),
                    "in_stock": "In stock" in availability
                }
                books_data.append(book)
            except Exception as e:
                logging.warning(f"error parsing book data: {e}")
                continue
        return books_data


# prueba de la clase
if __name__ == "__main__":
    scraper = BookScrapper(max_pages=1) #objeto o instancia de la clase
    html = scraper.fetch_page(1)
    if html:
        books = scraper.parse_books(html)
        print(f"found {len(books)} books on page 1")
        for book in books[:3]:
            print(book)
    else:
        print("failed to fetch page")

