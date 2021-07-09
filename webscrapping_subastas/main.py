import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

def obtenerCards(webdriver_path, debug=debug):
    cards = []
    cards += obtenerCardsCordoba() + obtenerCardsBsAs()
    return cards

def obtenerCardsCordoba(webdriver_path, debug=debug):
    controno_cards = obtenerCardsGeneral_Cordoba(webdriver_path, debug=debug)
    consolidadas_cards = consolidarCards_Cordoba(webdriver_path, controno_cards, debug=debug)

def obtenerCardsGeneral_Cordoba(webdriver_path, debug=debug):
    cards = []
    # Vigentes Inmuebles # https://subastas.justiciacordoba.gob.ar/?status=active&cat_id=20
    vigentes_inmuebles_url = "https://subastas.justiciacordoba.gob.ar/?status=active&cat_id=20"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    #options.add_argument("--headless --log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #self.driver = webdriver.Chrome(executable_path='/Users/${userName}/Drivers/chromedriver', chrome_options=options)
    driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
    driver.get(vigentes_inmuebles_url)
    time.sleep(2)  # Allow 2 seconds for the web page to open
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    SCROLL_PAUSE_TIME = 2
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        time.sleep(SCROLL_PAUSE_TIME)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for card in soup.find_all(class_="card")[1:]:
        consolidada_card = {}
        contorno_card = {}
        referencia = "Subasta Cordoba Inmuebles Vigentes"
        url = card.find("a").get("href")
        titular = card.find_all("a")[1].find("h6").text.strip()
        contorno_card["referencia"] = referencia
        contorno_card["url"] = url
        contorno_card["titular"] = titular
        consolidada_card = consolidarCards_Cordoba(webdriver_path, contorno_card, debug=debug)
        cards.append(consolidada_card)



def consolidarCard_Cordoba(webdriver_path, contorno_card, debug=debug):
    consolidada_card = contorno_card
    card_url = consolidada_card["url"]
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    #options.add_argument("--headless --log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #self.driver = webdriver.Chrome(executable_path='/Users/${userName}/Drivers/chromedriver', chrome_options=options)
    driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
    driver.get(card_url)
    time.sleep(2)  # Allow 2 seconds for the web page to open
    soup_card = BeautifulSoup(driver.page_source, "html.parser")
    main_image = soup_card.find("meta", property="og:image").get("content")
    all_images_card = soup_card.find_all("img", {"class":"img img-responsive"})
    all_images = ""
    for image in all_images_card:
        if "storage" in image["src"]:
            if all_images == "":
                all_images = image["src"]
            else:
                all_images += ", " + image["src"]
    valores_monetarios_raw = soup_card.find("table", {"id": "costs_table"}).find_all("small")
    valor_oferta = valores_monetarios_raw[1].text.replace(u"$\xa0", "").replace(".", "")
    valor_comision_martillero = valores_monetarios_raw[3].text.replace(u"$\xa0", "").replace(".", "")
    valor_fondo_de_prevencion_para_la_violencia_familiar = valores_monetarios_raw[5].text.replace(u"$\xa0", "").replace(".", "")
    valor_servicio_de_subastas_electronicas = valores_monetarios_raw[7].text.replace(u"$\xa0", "").replace(".", "")
    total = soup_card.find("tfoot").text.replace(u"$\xa0", "").replace("Total", "").replace(".", "")
    offer = soup_card.find("div", {"id": "offer"}).text.replace("Ofertar $\xa0", "").replace(".", "")
    consolidada_card["main_image"] = main_image
    consolidada_card["all_images"] = all_images
    consolidada_card["valor_oferta"] = valor_oferta
    consolidada_card["valor_comision_martillero"] = valor_comision_martillero
    consolidada_card["valor_fondo_de_prevencion_para_la_violencia_familiar"] = valor_fondo_de_prevencion_para_la_violencia_familiar
    consolidada_card["valor_servicio_de_subastas_electronicas"] = valor_servicio_de_subastas_electronicas
    consolidada_card["valor_total"] = total
    consolidada_card["offer"] = offer
    return consolidada_card
    
def obtenerCardsBsAs(webdriver_path, debug=False):
    cards = []
    # Fijarse como es que se obtienen las cards
    # Inmuebles Publicadas # POST	https://subastas.scba.gov.ar/Auctions/QuickSearch | payload: filter=inmueble
    # 


debug = "False"
webdriver_path = 'D:\\Descargas D\chromedriver_win32\\chromedriver'