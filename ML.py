from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.webdriver.chrome.options import Options


def buscar_producto():
    palabra_clave = input(
        "Ingrese una palabra clave para buscar un producto: ")
    return palabra_clave


def formatear_palabra(palabra):
    # Convertir la palabra a minúsculas
    palabra = palabra.lower()
    # Reemplazar espacios con guiones
    palabra = palabra.replace(" ", "-")
    # Crear la cadena formateada
    resultado = f"{palabra}#D[A:{palabra}]"
    return resultado


def obtener_tabla(url, driver):
    # Abrir la página
    driver.get(url)
    # Esperar a que la tabla esté presente en la página
    tabla_presente = EC.presence_of_element_located(
        (By.CSS_SELECTOR, "li.ui-search-layout__item"))
    WebDriverWait(driver, 5).until(tabla_presente)

    # Listas para almacenar datos
    Producto = []
    Precio = []

    # Extraer el contenido HTML de la página
    contenido = driver.page_source
    soup = bs(contenido, "html.parser")

    # Buscar contenedores de tarjetas y extraer los datos de cada tarjeta
    contenedores_tarjetas = soup.find_all(
        "li", class_="ui-search-layout__item")
    for tarjeta in contenedores_tarjetas:
        # Nombre Producto
        nombre_producto_elemento = tarjeta.select_one(
            "div.ui-search-result__content-wrapper > div.ui-search-item__group.ui-search-item__group--title > a.ui-search-item__group__element.ui-search-link")
        nombre_producto = nombre_producto_elemento.text.strip(
        ) if nombre_producto_elemento else "No disponible"
        Producto.append(nombre_producto)

        # Precio
        precio_elemento = tarjeta.select_one(
            "div.ui-search-result__content-wrapper > div.ui-search-result__content-columns > div.ui-search-result__content-column.ui-search-result__content-column--left > div.ui-search-item__group.ui-search-item__group--price.ui-search-item__group--price-grid-container > div > div > div > span.andes-money-amount.ui-search-price__part.ui-search-price__part--medium.andes-money-amount--cents-superscript > span.andes-money-amount__fraction")
        precio = precio_elemento.text.strip() if precio_elemento else "No disponible"
        Precio.append(precio)

    # Crear DataFrame fuera del bucle for
    df = pd.DataFrame({"Producto": Producto, "Precio": Precio})
    print(df)


def main():
    print("Bienvenido al buscador de productos.")
    palabra = buscar_producto()
    busqueda = formatear_palabra(palabra)
    # Concatenar la palabra clave formateada a la URL base de Mercado Libre
    url = "https://listado.mercadolibre.com.mx/" + busqueda

    # Asegúrate de que la ruta al chromedriver es correcta
    chromedriver_path = r"C:\Users\Diego-lap\chromedriver-win32\chromedriver-win32\chromedriver.exe"

    # Configurar ChromeDriver para ejecutarse en modo headless
    options = Options()
    options.add_argument("--headless")
    # Añadir un tamaño de ventana
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")  # Deshabilitar GPU en modo headless
    # Deshabilitar la mayoría de los logs de la consola
    options.add_argument("--log-level=3")
    options.add_argument("--disable-logging")  # Deshabilitar logs adicionales

    # Crear una instancia del servicio con la ruta al chromedriver
    service = Service(executable_path=chromedriver_path)

    # Inicializa el controlador de Chrome con el servicio y las opciones
    driver = webdriver.Chrome(service=service, options=options)

    # Llamar a la función para abrir la URL
    obtener_tabla(url, driver)

    # Mantener el navegador abierto
    input("Presiona Enter para cerrar el navegador...")
    # Cerrar el navegador
    driver.quit()


if __name__ == "__main__":
    main()
